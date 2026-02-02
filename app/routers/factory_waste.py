from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.factory_waste import FactoryWaste
from app.models.user import User
from app.schemas.factory_waste import (
    FactoryWasteCreate,
    FactoryWasteRead,
    FactoryWasteUpdate,
)

router = APIRouter(prefix="/factory_waste", tags=["Factory Waste"])


@router.post("/", response_model=FactoryWasteRead)
async def create_factory_waste(
    data: FactoryWasteCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_waste = FactoryWaste(**data.model_dump())
    session.add(factory_waste)
    await session.commit()
    await session.refresh(factory_waste)
    return factory_waste


@router.get("/", response_model=list[FactoryWasteRead])
async def get_factory_wastes(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(FactoryWaste))
    return data.scalars().all()


@router.get("/{id}", response_model=FactoryWasteRead)
async def get_factory_waste(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_waste = await session.get(FactoryWaste, id)
    if not factory_waste:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory waste not found",
        )
    return factory_waste


@router.patch("/{id}", response_model=FactoryWasteRead)
async def update_factory_waste(
    id: int,
    data: FactoryWasteUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_waste = await session.get(FactoryWaste, id)
    if not factory_waste:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory waste not found",
        )

    factory_waste_data = data.model_dump(exclude_unset=True)
    for key, value in factory_waste_data.items():
        setattr(factory_waste, key, value)

    await session.commit()
    await session.refresh(factory_waste)
    return factory_waste


@router.delete("/{id}")
async def delete_factory_waste(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_waste = await session.get(FactoryWaste, id)
    if not factory_waste:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory waste not found",
        )

    await session.delete(factory_waste)
    await session.commit()
    return {"detail": "Factory waste deleted successfully"}
