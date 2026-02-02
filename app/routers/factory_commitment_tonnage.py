from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.factory_commitment_tonnage import FactoryCommitmentTonnage
from app.models.user import User
from app.schemas.factory_commitment_tonnage import (
    FactoryCommitmentTonnageCreate,
    FactoryCommitmentTonnageRead,
    FactoryCommitmentTonnageUpdate,
)

router = APIRouter(
    prefix="/factory_commitment_tonnage", tags=["Factory Commitment Tonnage"]
)


@router.post("/", response_model=FactoryCommitmentTonnageRead)
async def create_factory_commitment_tonnage(
    data: FactoryCommitmentTonnageCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_commitment_tonnage = FactoryCommitmentTonnage(**data.model_dump())
    session.add(factory_commitment_tonnage)
    await session.commit()
    await session.refresh(factory_commitment_tonnage)
    return factory_commitment_tonnage


@router.get("/", response_model=list[FactoryCommitmentTonnageRead])
async def get_factory_commitment_tonnages(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(FactoryCommitmentTonnage))
    return data.scalars().all()


@router.get("/{id}", response_model=FactoryCommitmentTonnageRead)
async def get_factory_commitment_tonnage(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_commitment_tonnage = await session.get(FactoryCommitmentTonnage, id)
    if not factory_commitment_tonnage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory commitment tonnage not found",
        )
    return factory_commitment_tonnage


@router.patch("/{id}", response_model=FactoryCommitmentTonnageRead)
async def update_factory_commitment_tonnage(
    id: int,
    data: FactoryCommitmentTonnageUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_commitment_tonnage = await session.get(FactoryCommitmentTonnage, id)
    if not factory_commitment_tonnage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory commitment tonnage not found",
        )

    factory_commitment_tonnage_data = data.model_dump(exclude_unset=True)
    for key, value in factory_commitment_tonnage_data.items():
        setattr(factory_commitment_tonnage, key, value)

    await session.commit()
    await session.refresh(factory_commitment_tonnage)
    return factory_commitment_tonnage


@router.delete("/{id}")
async def delete_factory_commitment_tonnage(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory_commitment_tonnage = await session.get(FactoryCommitmentTonnage, id)
    if not factory_commitment_tonnage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factory commitment tonnage not found",
        )

    await session.delete(factory_commitment_tonnage)
    await session.commit()
    return {"detail": "Factory commitment tonnage deleted successfully"}
