from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.purity_price import PurityPrice
from app.models.user import User
from app.schemas.purity_price import (
    PurityPriceCreate,
    PurityPriceRead,
    PurityPriceUpdate,
)

router = APIRouter(prefix="/purity_price", tags=["Purity Prices"])


@router.post("/", response_model=PurityPriceRead)
async def create_purity_price(
    data: PurityPriceCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    purity_price = PurityPrice(**data.model_dump())
    session.add(purity_price)
    await session.commit()
    await session.refresh(purity_price)
    return purity_price


@router.get("/", response_model=list[PurityPriceRead])
async def get_purity_prices(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(PurityPrice))
    return data.scalars().all()


@router.get("/{id}", response_model=PurityPriceRead)
async def get_purity_price(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    purity_price = await session.get(PurityPrice, id)
    if not purity_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purity price not found",
        )
    return purity_price


@router.patch("/{id}", response_model=PurityPriceRead)
async def update_purity_price(
    id: int,
    data: PurityPriceUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    purity_price = await session.get(PurityPrice, id)
    if not purity_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purity price not found",
        )

    purity_price_data = data.model_dump(exclude_unset=True)
    for key, value in purity_price_data.items():
        setattr(purity_price, key, value)

    await session.commit()
    await session.refresh(purity_price)
    return purity_price


@router.delete("/{id}")
async def delete_purity_price(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    purity_price = await session.get(PurityPrice, id)
    if not purity_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purity price not found",
        )

    await session.delete(purity_price)
    await session.commit()
    return {"detail": "Purity price deleted successfully"}
