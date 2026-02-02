from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.farmers_pesticide import FarmersPesticide
from app.models.user import User
from app.schemas.farmers_pesticide import (
    FarmersPesticideCreate,
    FarmersPesticideRead,
    FarmersPesticideUpdate,
)

router = APIRouter(prefix="/farmers_pesticide", tags=["Farmers Pesticides"])


@router.post("/", response_model=FarmersPesticideRead)
async def create_farmers_pesticide(
    data: FarmersPesticideCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_pesticide = FarmersPesticide(**data.model_dump())
    session.add(farmers_pesticide)
    await session.commit()
    await session.refresh(farmers_pesticide)
    return farmers_pesticide


@router.get("/", response_model=list[FarmersPesticideRead])
async def get_farmers_pesticides(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(FarmersPesticide))
    return data.scalars().all()


@router.get("/{id}", response_model=FarmersPesticideRead)
async def get_farmers_pesticide(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_pesticide = await session.get(FarmersPesticide, id)
    if not farmers_pesticide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers pesticide not found",
        )
    return farmers_pesticide


@router.patch("/{id}", response_model=FarmersPesticideRead)
async def update_farmers_pesticide(
    id: int,
    data: FarmersPesticideUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_pesticide = await session.get(FarmersPesticide, id)
    if not farmers_pesticide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers pesticide not found",
        )

    farmers_pesticide_data = data.model_dump(exclude_unset=True)
    for key, value in farmers_pesticide_data.items():
        setattr(farmers_pesticide, key, value)

    await session.commit()
    await session.refresh(farmers_pesticide)
    return farmers_pesticide


@router.delete("/{id}")
async def delete_farmers_pesticide(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_pesticide = await session.get(FarmersPesticide, id)
    if not farmers_pesticide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers pesticide not found",
        )

    await session.delete(farmers_pesticide)
    await session.commit()
    return {"detail": "Farmers pesticide deleted successfully"}
