from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.factory_sugar import FactorySugar
from app.models.user import User
from app.schemas.factory_sugar import (
    FactorySugarCreate,
    FactorySugarRead,
    FactorySugarUpdate,
)

router = APIRouter(prefix="/factory_sugar", tags=["Factory Sugar"])


@router.post("/", response_model=FactorySugarRead)
async def create_factory_sugar(
    data: FactorySugarCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_sugar = FactorySugar(**data.model_dump())
    session.add(factory_sugar)
    await session.commit()
    await session.refresh(factory_sugar)
    return factory_sugar


@router.get("/", response_model=list[FactorySugarRead])
async def get_factory_sugars(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(FactorySugar))
    return data.scalars().all()


@router.get("/{id}", response_model=FactorySugarRead)
async def get_factory_sugar(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_sugar = await session.get(FactorySugar, id)
    if not factory_sugar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory sugar not found",
        )
    return factory_sugar


@router.patch("/{id}", response_model=FactorySugarRead)
async def update_factory_sugar(
    id: int,
    data: FactorySugarUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_sugar = await session.get(FactorySugar, id)
    if not factory_sugar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory sugar not found",
        )

    factory_sugar_data = data.model_dump(exclude_unset=True)
    for key, value in factory_sugar_data.items():
        setattr(factory_sugar, key, value)

    await session.commit()
    await session.refresh(factory_sugar)
    return factory_sugar


@router.delete("/{id}")
async def delete_factory_sugar(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_sugar = await session.get(FactorySugar, id)
    if not factory_sugar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory sugar not found",
        )

    await session.delete(factory_sugar)
    await session.commit()
    return {"detail": "Factory sugar deleted successfully"}
