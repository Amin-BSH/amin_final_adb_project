from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.farmers_sugar_delivery import FarmersSugarDelivery
from app.models.user import User
from app.schemas.farmers_sugar_delivery import (
    FarmersSugarDeliveryCreate,
    FarmersSugarDeliveryRead,
    FarmersSugarDeliveryUpdate,
)

router = APIRouter(prefix="/farmers_sugar_delivery", tags=["Farmers Sugar Delivery"])


@router.post("/", response_model=FarmersSugarDeliveryRead)
async def create_farmers_sugar_delivery(
    data: FarmersSugarDeliveryCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_sugar_delivery = FarmersSugarDelivery(**data.model_dump())
    session.add(farmers_sugar_delivery)
    await session.commit()
    await session.refresh(farmers_sugar_delivery)
    return farmers_sugar_delivery


@router.get("/", response_model=list[FarmersSugarDeliveryRead])
async def get_farmers_sugar_deliveries(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(FarmersSugarDelivery))
    return data.scalars().all()


@router.get("/{id}", response_model=FarmersSugarDeliveryRead)
async def get_farmers_sugar_delivery(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_sugar_delivery = await session.get(FarmersSugarDelivery, id)
    if not farmers_sugar_delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers sugar delivery not found",
        )
    return farmers_sugar_delivery


@router.patch("/{id}", response_model=FarmersSugarDeliveryRead)
async def update_farmers_sugar_delivery(
    id: int,
    data: FarmersSugarDeliveryUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_sugar_delivery = await session.get(FarmersSugarDelivery, id)
    if not farmers_sugar_delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers sugar delivery not found",
        )

    farmers_sugar_delivery_data = data.model_dump(exclude_unset=True)
    for key, value in farmers_sugar_delivery_data.items():
        setattr(farmers_sugar_delivery, key, value)

    await session.commit()
    await session.refresh(farmers_sugar_delivery)
    return farmers_sugar_delivery


@router.delete("/{id}")
async def delete_farmers_sugar_delivery(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_sugar_delivery = await session.get(FarmersSugarDelivery, id)
    if not farmers_sugar_delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers sugar delivery not found",
        )

    await session.delete(farmers_sugar_delivery)
    await session.commit()
    return {"detail": "Farmers sugar delivery deleted successfully"}
