from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.factory_pesticide import FactoryPesticide
from app.models.user import User
from app.schemas.factory_pesticide import (
    FactoryPesticideCreate,
    FactoryPesticideRead,
    FactoryPesticideUpdate,
)

router = APIRouter(prefix="/factory_pesticide", tags=["Factory Pesticides"])


@router.post("/", response_model=FactoryPesticideRead)
async def create_factory_pesticide(
    data: FactoryPesticideCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_pesticide = FactoryPesticide(**data.model_dump())
    session.add(factory_pesticide)
    await session.commit()
    await session.refresh(factory_pesticide)
    return factory_pesticide


@router.get("/", response_model=list[FactoryPesticideRead])
async def get_factory_pesticides(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(FactoryPesticide))
    return data.scalars().all()


@router.get("/{id}", response_model=FactoryPesticideRead)
async def get_factory_pesticide(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_pesticide = await session.get(FactoryPesticide, id)
    if not factory_pesticide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory pesticide not found",
        )
    return factory_pesticide


@router.patch("/{id}", response_model=FactoryPesticideRead)
async def update_factory_pesticide(
    id: int,
    data: FactoryPesticideUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_pesticide = await session.get(FactoryPesticide, id)
    if not factory_pesticide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory pesticide not found",
        )

    factory_pesticide_data = data.model_dump(exclude_unset=True)
    for key, value in factory_pesticide_data.items():
        setattr(factory_pesticide, key, value)

    await session.commit()
    await session.refresh(factory_pesticide)
    return factory_pesticide


@router.delete("/{id}")
async def delete_factory_pesticide(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_pesticide = await session.get(FactoryPesticide, id)
    if not factory_pesticide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory pesticide not found",
        )

    await session.delete(factory_pesticide)
    await session.commit()
    return {"detail": "Factory pesticide deleted successfully"}
