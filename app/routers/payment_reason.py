from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.payment_reason import PaymentReason
from app.models.user import User
from app.schemas.payment_reason import (
    PaymentReasonCreate,
    PaymentReasonRead,
    PaymentReasonUpdate,
)

router = APIRouter(prefix="/payment_reason", tags=["Payment Reasons"])


@router.post(path="/", response_model=PaymentReasonRead)
async def create_payment_reason(
    data: PaymentReasonCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data_validate = PaymentReason(reason_name=data.reason_name)

    session.add(data_validate)
    await session.commit()
    await session.refresh(data_validate)
    return data_validate


@router.get(path="/", response_model=list[PaymentReasonRead])
async def get_payment_reasons(
    session: Session = Depends(get_session), user: User = Depends(get_current_user)
):
    data = await session.execute(select(PaymentReason))

    return data.scalars().all()


@router.get(path="/{data}", response_model=PaymentReasonRead)
async def get_payment_reason(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    payment_reason = await session.get(PaymentReason, id)

    if not payment_reason:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment reason not found"
        )

    return payment_reason


@router.patch(path="/{id}", response_model=PaymentReasonRead)
async def update_payment_reason(
    id: int,
    data: PaymentReasonUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    payment_reason = await session.get(PaymentReason, id)

    if not payment_reason:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment reason not found"
        )

    data_validate = data.model_dump(exclude_unset=True)

    for key, value in data_validate.items():
        setattr(payment_reason, key, value)

    await session.commit()
    await session.refresh(payment_reason)
    return payment_reason


@router.delete(path="/{id}")
async def delete_payment_reason(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    payment_reason = await session.get(PaymentReason, id)

    if not payment_reason:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment reason not found"
        )

    await session.delete(payment_reason)
    await session.commit()

    return {"detail": "Payment reason deleted successfully"}
