from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.farmers_load import FarmersLoad
from app.models.user import User
from app.schemas.farmers_load import (
    FarmersLoadCreate,
    FarmersLoadRead,
    FarmersLoadUpdate,
)

router = APIRouter(prefix="/farmers_load", tags=["Farmers Load"])


@router.post("/", response_model=FarmersLoadRead)
async def create_farmers_load(
    data: FarmersLoadCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_load = FarmersLoad(**data.model_dump())
    session.add(farmers_load)
    await session.commit()
    await session.refresh(farmers_load)
    return farmers_load


@router.get("/", response_model=list[FarmersLoadRead])
async def get_farmers_loads(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(FarmersLoad))
    return data.scalars().all()


@router.get("/{id}", response_model=FarmersLoadRead)
async def get_farmers_load(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_load = await session.get(FarmersLoad, id)
    if not farmers_load:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers load not found",
        )
    return farmers_load


@router.patch("/{id}", response_model=FarmersLoadRead)
async def update_farmers_load(
    id: int,
    data: FarmersLoadUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_load = await session.get(FarmersLoad, id)
    if not farmers_load:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers load not found",
        )

    farmers_load_data = data.model_dump(exclude_unset=True)
    for key, value in farmers_load_data.items():
        setattr(farmers_load, key, value)

    await session.commit()
    await session.refresh(farmers_load)
    return farmers_load


@router.delete("/{id}")
async def delete_farmers_load(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_load = await session.get(FarmersLoad, id)
    if not farmers_load:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers load not found",
        )

    await session.delete(farmers_load)
    await session.commit()
    return {"detail": "Farmers load deleted successfully"}
