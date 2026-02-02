from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.carriage import Carriage
from app.models.user import User
from app.schemas.carriage import CarriageCreate, CarriageRead, CarriageUpdate

router = APIRouter(prefix="/carriage", tags=["Carriages"])


@router.post("/", response_model=CarriageRead)
async def create_carriage(
    data: CarriageCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    carriage = Carriage(**data.model_dump())
    session.add(carriage)
    await session.commit()
    await session.refresh(carriage)
    return carriage


@router.get("/", response_model=list[CarriageRead])
async def get_carriages(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(Carriage))
    return data.scalars().all()


@router.get("/{id}", response_model=CarriageRead)
async def get_carriage(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    carriage = await session.get(Carriage, id)
    if not carriage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Carriage not found"
        )
    return carriage


@router.patch("/{id}", response_model=CarriageRead)
async def update_carriage(
    id: int,
    data: CarriageUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    carriage = await session.get(Carriage, id)
    if not carriage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Carriage not found"
        )

    carriage_data = data.model_dump(exclude_unset=True)
    for key, value in carriage_data.items():
        setattr(carriage, key, value)

    await session.commit()
    await session.refresh(carriage)
    return carriage


@router.delete("/{id}")
async def delete_carriage(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    carriage = await session.get(Carriage, id)
    if not carriage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Carriage not found"
        )

    await session.delete(carriage)
    await session.commit()
    return {"detail": "Carriage deleted successfully"}
