from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.farmers_waste_delivery import FarmersWasteDelivery
from app.models.user import User
from app.schemas.farmers_waste_delivery import (
    FarmersWasteDeliveryCreate,
    FarmersWasteDeliveryRead,
    FarmersWasteDeliveryUpdate,
)

router = APIRouter(prefix="/farmers_waste_delivery", tags=["Farmers Waste Delivery"])


@router.post("/", response_model=FarmersWasteDeliveryRead)
async def create_farmers_waste_delivery(
    data: FarmersWasteDeliveryCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_waste_delivery = FarmersWasteDelivery(**data.model_dump())
    session.add(farmers_waste_delivery)
    await session.commit()
    await session.refresh(farmers_waste_delivery)
    return farmers_waste_delivery


@router.get("/", response_model=list[FarmersWasteDeliveryRead])
async def get_farmers_waste_deliveries(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(FarmersWasteDelivery))
    return data.scalars().all()


@router.get("/{id}", response_model=FarmersWasteDeliveryRead)
async def get_farmers_waste_delivery(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_waste_delivery = await session.get(FarmersWasteDelivery, id)
    if not farmers_waste_delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers waste delivery not found",
        )
    return farmers_waste_delivery


@router.patch("/{id}", response_model=FarmersWasteDeliveryRead)
async def update_farmers_waste_delivery(
    id: int,
    data: FarmersWasteDeliveryUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_waste_delivery = await session.get(FarmersWasteDelivery, id)
    if not farmers_waste_delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers waste delivery not found",
        )

    farmers_waste_delivery_data = data.model_dump(exclude_unset=True)
    for key, value in farmers_waste_delivery_data.items():
        setattr(farmers_waste_delivery, key, value)

    await session.commit()
    await session.refresh(farmers_waste_delivery)
    return farmers_waste_delivery


@router.delete("/{id}")
async def delete_farmers_waste_delivery(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_waste_delivery = await session.get(FarmersWasteDelivery, id)
    if not farmers_waste_delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers waste delivery not found",
        )

    await session.delete(farmers_waste_delivery)
    await session.commit()
    return {"detail": "Farmers waste delivery deleted successfully"}
