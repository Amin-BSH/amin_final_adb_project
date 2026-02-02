from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.farmers_payment import FarmersPayment
from app.models.user import User
from app.schemas.farmers_payment import (
    FarmersPaymentCreate,
    FarmersPaymentRead,
    FarmersPaymentUpdate,
)

router = APIRouter(prefix="/farmers_payment", tags=["Farmers Payments"])


@router.post("/", response_model=FarmersPaymentRead)
async def create_farmers_payment(
    data: FarmersPaymentCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_payment = FarmersPayment(**data.model_dump())
    session.add(farmers_payment)
    await session.commit()
    await session.refresh(farmers_payment)
    return farmers_payment


@router.get("/", response_model=list[FarmersPaymentRead])
async def get_farmers_payments(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(FarmersPayment))
    return data.scalars().all()


@router.get("/{id}", response_model=FarmersPaymentRead)
async def get_farmers_payment(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_payment = await session.get(FarmersPayment, id)
    if not farmers_payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers payment not found",
        )
    return farmers_payment


@router.patch("/{id}", response_model=FarmersPaymentRead)
async def update_farmers_payment(
    id: int,
    data: FarmersPaymentUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_payment = await session.get(FarmersPayment, id)
    if not farmers_payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers payment not found",
        )

    farmers_payment_data = data.model_dump(exclude_unset=True)
    for key, value in farmers_payment_data.items():
        setattr(farmers_payment, key, value)

    await session.commit()
    await session.refresh(farmers_payment)
    return farmers_payment


@router.delete("/{id}")
async def delete_farmers_payment(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_payment = await session.get(FarmersPayment, id)
    if not farmers_payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers payment not found",
        )

    await session.delete(farmers_payment)
    await session.commit()
    return {"detail": "Farmers payment deleted successfully"}
