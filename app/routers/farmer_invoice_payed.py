from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.farmer_invoice_payed import FarmerInvoicePayed
from app.models.user import User
from app.schemas.farmer_invoice_payed import (
    FarmerInvoicePayedCreate,
    FarmerInvoicePayedRead,
    FarmerInvoicePayedUpdate,
)

router = APIRouter(prefix="/farmer_invoice_payed", tags=["Farmer Invoice Payed"])


@router.post("/", response_model=FarmerInvoicePayedRead)
async def create_farmer_invoice_payed(
    data: FarmerInvoicePayedCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmer_invoice_payed = FarmerInvoicePayed(**data.model_dump())
    session.add(farmer_invoice_payed)
    await session.commit()
    await session.refresh(farmer_invoice_payed)
    return farmer_invoice_payed


@router.get("/", response_model=list[FarmerInvoicePayedRead])
async def get_farmer_invoices_payed(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(FarmerInvoicePayed))
    return data.scalars().all()


@router.get("/{id}", response_model=FarmerInvoicePayedRead)
async def get_farmer_invoice_payed(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmer_invoice_payed = await session.get(FarmerInvoicePayed, id)
    if not farmer_invoice_payed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer invoice payed not found",
        )
    return farmer_invoice_payed


@router.patch("/{id}", response_model=FarmerInvoicePayedRead)
async def update_farmer_invoice_payed(
    id: int,
    data: FarmerInvoicePayedUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmer_invoice_payed = await session.get(FarmerInvoicePayed, id)
    if not farmer_invoice_payed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer invoice payed not found",
        )

    farmer_invoice_payed_data = data.model_dump(exclude_unset=True)
    for key, value in farmer_invoice_payed_data.items():
        setattr(farmer_invoice_payed, key, value)

    await session.commit()
    await session.refresh(farmer_invoice_payed)
    return farmer_invoice_payed


@router.delete("/{id}")
async def delete_farmer_invoice_payed(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmer_invoice_payed = await session.get(FarmerInvoicePayed, id)
    if not farmer_invoice_payed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer invoice payed not found",
        )

    await session.delete(farmer_invoice_payed)
    await session.commit()
    return {"detail": "Farmer invoice payed deleted successfully"}
