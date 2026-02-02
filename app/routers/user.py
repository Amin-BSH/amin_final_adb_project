from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.dependencies import Hasher
from app.jwt_auth import sign_jwt
from app.models.user import User
from app.schemas.user import (
    ChangePasswordRequest,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserRead,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=TokenResponse)
async def register(data: UserCreate, session: Session = Depends(get_session)):
    existing_user = await session.execute(select(User).where(User.email == data.email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_password = Hasher.get_password_hash(data.password)

    new_user = User(
        username=data.username,
        email=data.email,
        password=hashed_password,
        fullname=data.fullname,
        phone_number=data.phone_number,
        role=data.role if data.role in ["user", "admin"] else "user",
    )
    similar_username = await session.execute(
        select(User).where(User.username == new_user.username)
    )
    similar_email = await session.execute(
        select(User).where(User.email == new_user.email)
    )

    if similar_username.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    if similar_email.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    token = sign_jwt(new_user.email)

    return TokenResponse(
        access_token=token["access token"], user=UserRead.model_validate(new_user)
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, session: Session = Depends(get_session)):
    result = await session.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    if not Hasher.verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    token = sign_jwt(user.email)

    return TokenResponse(
        access_token=token["access token"], user=UserRead.model_validate(user)
    )


@router.post("/logout")
async def logout(user: User = Depends(get_current_user)):
    return {
        "detail": "Successfully logged out",
        "message": "Please discard your token on the client side",
    }


@router.get("/me", response_model=UserRead)
async def get_current_user_info(user: User = Depends(get_current_user)):
    return user


@router.post("/change-password", response_model=dict)
async def change_password(
    data: ChangePasswordRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data.validate_passwords_match()

    db_user = await session.get(User, user.user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not Hasher.verify_password(data.current_password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect",
        )

    db_user.password = Hasher.get_password_hash(data.new_password)
    await session.commit()

    return {"detail": "Password changed successfully"}


@router.get("/", response_model=list[UserRead])
async def get_all_users(
    session: Session = Depends(get_session), user: User = Depends(get_current_user)
):
    result = await session.execute(select(User))
    return result.scalars().all()


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    user = await session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    data: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.user_id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile or be an admin",
        )

    user = await session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if data.email and data.email != user.email:
        existing = await session.execute(select(User).where(User.email == data.email))
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    if data.role is not None:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admin can change user roles",
            )

    user_data = data.model_dump(exclude_unset=True)

    for key, value in user_data.items():
        if value is not None:
            setattr(user, key, value)

    await session.commit()
    await session.refresh(user)

    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    admin: User = Depends(get_current_user),
):
    if admin.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can delete users"
        )

    user = await session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    await session.delete(user)
    await session.commit()

    return {"detail": "User deleted successfully"}
