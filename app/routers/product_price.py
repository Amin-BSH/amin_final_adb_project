from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.product_price import ProductPrice
from app.models.user import User
from app.schemas.product_price import (
    ProductPriceCreate,
    ProductPriceRead,
    ProductPriceUpdate,
)

router = APIRouter(prefix="/product_price", tags=["Product Prices"])


@router.post("/", response_model=ProductPriceRead)
async def create_product_price(
    data: ProductPriceCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    product_price = ProductPrice(**data.model_dump())
    session.add(product_price)
    await session.commit()
    await session.refresh(product_price)
    return product_price


@router.get("/", response_model=list[ProductPriceRead])
async def get_product_prices(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(ProductPrice))
    return data.scalars().all()


@router.get("/{id}", response_model=ProductPriceRead)
async def get_product_price(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    product_price = await session.get(ProductPrice, id)
    if not product_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product price not found",
        )
    return product_price


@router.patch("/{id}", response_model=ProductPriceRead)
async def update_product_price(
    id: int,
    data: ProductPriceUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    product_price = await session.get(ProductPrice, id)
    if not product_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product price not found",
        )

    product_price_data = data.model_dump(exclude_unset=True)
    for key, value in product_price_data.items():
        setattr(product_price, key, value)

    await session.commit()
    await session.refresh(product_price)
    return product_price


@router.delete("/{id}")
async def delete_product_price(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    product_price = await session.get(ProductPrice, id)
    if not product_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product price not found",
        )

    await session.delete(product_price)
    await session.commit()
    return {"detail": "Product price deleted successfully"}
