from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.factory_payment import FactoryPayment
from app.models.user import User
from app.schemas.factory_payment import (
    FactoryPaymentCreate,
    FactoryPaymentRead,
    FactoryPaymentUpdate,
)

router = APIRouter(prefix="/factory_payment", tags=["Factory Payments"])


@router.post("/", response_model=FactoryPaymentRead)
async def create_factory_payment(
    data: FactoryPaymentCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_payment = FactoryPayment(**data.model_dump())
    session.add(factory_payment)
    await session.commit()
    await session.refresh(factory_payment)
    return factory_payment


@router.get("/", response_model=list[FactoryPaymentRead])
async def get_factory_payments(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(FactoryPayment))
    return data.scalars().all()


@router.get("/{id}", response_model=FactoryPaymentRead)
async def get_factory_payment(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_payment = await session.get(FactoryPayment, id)
    if not factory_payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory payment not found",
        )
    return factory_payment


@router.patch("/{id}", response_model=FactoryPaymentRead)
async def update_factory_payment(
    id: int,
    data: FactoryPaymentUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_payment = await session.get(FactoryPayment, id)
    if not factory_payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory payment not found",
        )

    factory_payment_data = data.model_dump(exclude_unset=True)
    for key, value in factory_payment_data.items():
        setattr(factory_payment, key, value)

    await session.commit()
    await session.refresh(factory_payment)
    return factory_payment


@router.delete("/{id}")
async def delete_factory_payment(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_payment = await session.get(FactoryPayment, id)
    if not factory_payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory payment not found",
        )

    await session.delete(factory_payment)
    await session.commit()
    return {"detail": "Factory payment deleted successfully"}
