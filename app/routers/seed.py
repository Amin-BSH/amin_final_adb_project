from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.dependencies import get_session
from app.models.seed import Seed
from app.models.user import User
from app.schemas.seed import SeedCreate, SeedRead, SeedUpdate

router = APIRouter(prefix="/seeds", tags=["Seeds"])


@router.post(path="/", response_model=SeedRead)
async def create_seed(
    data: SeedCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data_validate = Seed(seed_name=data.seed_name, measure_unit_id=data.measure_unit_id)

    session.add(data_validate)
    await session.commit()
    await session.refresh(data_validate)
    return data_validate


@router.get(path="/", response_model=list[SeedRead])
async def get_seeds(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(Seed))

    return data.scalars().all()


@router.get(path="/{id}", response_model=SeedRead)
async def get_seed(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    seed = await session.get(Seed, id)

    if not seed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Seed not found"
        )

    return seed


@router.patch(path="/{id}", response_model=SeedRead)
async def update_seed(
    id: int,
    data: SeedUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    seed = await session.get(Seed, id)

    if not seed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Seed not found"
        )

    data_validate = data.model_dump(exclude_unset=True)

    for key, value in data_validate.items():
        setattr(seed, key, value)

    await session.commit()
    await session.refresh(seed)

    return seed


@router.delete(path="/{id}")
async def delete_seed(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    seed = await session.get(Seed, id)

    if not seed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Seed not found"
        )

    await session.delete(seed)
    await session.commit()

    return {"detail": "Seed removed successfully"}
