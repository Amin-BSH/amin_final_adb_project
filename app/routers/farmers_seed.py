from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.farmers_seed import FarmersSeed
from app.models.user import User
from app.schemas.farmers_seed import (
    FarmersSeedCreate,
    FarmersSeedRead,
    FarmersSeedUpdate,
)

router = APIRouter(prefix="/farmers_seed", tags=["Farmers Seeds"])


@router.post("/", response_model=FarmersSeedRead)
async def create_farmers_seed(
    data: FarmersSeedCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_seed = FarmersSeed(**data.model_dump())
    session.add(farmers_seed)
    await session.commit()
    await session.refresh(farmers_seed)
    return farmers_seed


@router.get("/", response_model=list[FarmersSeedRead])
async def get_farmers_seeds(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(FarmersSeed))
    return data.scalars().all()


@router.get("/{id}", response_model=FarmersSeedRead)
async def get_farmers_seed(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_seed = await session.get(FarmersSeed, id)
    if not farmers_seed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers seed not found",
        )
    return farmers_seed


@router.patch("/{id}", response_model=FarmersSeedRead)
async def update_farmers_seed(
    id: int,
    data: FarmersSeedUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_seed = await session.get(FarmersSeed, id)
    if not farmers_seed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers seed not found",
        )

    farmers_seed_data = data.model_dump(exclude_unset=True)
    for key, value in farmers_seed_data.items():
        setattr(farmers_seed, key, value)

    await session.commit()
    await session.refresh(farmers_seed)
    return farmers_seed


@router.delete("/{id}")
async def delete_farmers_seed(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_seed = await session.get(FarmersSeed, id)
    if not farmers_seed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers seed not found",
        )

    await session.delete(farmers_seed)
    await session.commit()
    return {"detail": "Farmers seed deleted successfully"}
