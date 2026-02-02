from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.factory_seed import FactorySeed
from app.models.user import User
from app.schemas.factory_seed import (
    FactorySeedCreate,
    FactorySeedRead,
    FactorySeedUpdate,
)

router = APIRouter(prefix="/factory_seed", tags=["Factory Seeds"])


@router.post("/", response_model=FactorySeedRead)
async def create_factory_seed(
    data: FactorySeedCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_seed = FactorySeed(**data.model_dump())
    session.add(factory_seed)
    await session.commit()
    await session.refresh(factory_seed)
    return factory_seed


@router.get("/", response_model=list[FactorySeedRead])
async def get_factory_seeds(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(FactorySeed))
    return data.scalars().all()


@router.get("/{id}", response_model=FactorySeedRead)
async def get_factory_seed(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_seed = await session.get(FactorySeed, id)
    if not factory_seed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory seed not found",
        )
    return factory_seed


@router.patch("/{id}", response_model=FactorySeedRead)
async def update_factory_seed(
    id: int,
    data: FactorySeedUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_seed = await session.get(FactorySeed, id)
    if not factory_seed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory seed not found",
        )

    factory_seed_data = data.model_dump(exclude_unset=True)
    for key, value in factory_seed_data.items():
        setattr(factory_seed, key, value)

    await session.commit()
    await session.refresh(factory_seed)
    return factory_seed


@router.delete("/{id}")
async def delete_factory_seed(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_seed = await session.get(FactorySeed, id)
    if not factory_seed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory seed not found",
        )

    await session.delete(factory_seed)
    await session.commit()
    return {"detail": "Factory seed deleted successfully"}
