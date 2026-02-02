from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(prefix="/product", tags=["Products"])


@router.post("/", response_model=ProductRead)
async def create_product(
    data: ProductCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    product = Product(**data.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@router.get("/", response_model=list[ProductRead])
async def get_products(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(Product))
    return data.scalars().all()


@router.get("/{id}", response_model=ProductRead)
async def get_product(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    product = await session.get(Product, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.patch("/{id}", response_model=ProductRead)
async def update_product(
    id: int,
    data: ProductUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    product = await session.get(Product, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    product_data = data.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(product, key, value)

    await session.commit()
    await session.refresh(product)
    return product


@router.delete("/{id}")
async def delete_product(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    product = await session.get(Product, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    await session.delete(product)
    await session.commit()
    return {"detail": "Product deleted successfully"}
