from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.jwt_auth import JWTBearer, decode_jwt
from app.models.user import User

jwt_bearer = JWTBearer()


async def get_current_user(
    token: str = Depends(jwt_bearer), session: Session = Depends(get_session)
):
    payload = decode_jwt(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )

    email = payload.get("user-identifier")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    # Get user from database
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user


# async def require_admin(user: User = Depends(get_current_user)):
#     """
#     Dependency to require admin role.
#     """
#     if user.role != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
#         )
#     return user


# async def require_user(user: User = Depends(get_current_user)):
#     """
#     Dependency to require user role (user or admin).
#     """
#     if user.role not in ["user", "admin"]:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="User access required"
#         )
#     return user
