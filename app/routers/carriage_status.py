from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.carriage_status import CarriageStatus
from app.models.user import User
from app.schemas.carriage_status import (
    CarriageStatusCreate,
    CarriageStatusRead,
    CarriageStatusUpdate,
)

router = APIRouter(prefix="/carriage_status", tags=["Carriage Status"])


@router.post("/", response_model=CarriageStatusRead)
async def create_carriage_status(
    data: CarriageStatusCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    carriage_status = CarriageStatus(**data.model_dump())
    session.add(carriage_status)
    await session.commit()
    await session.refresh(carriage_status)
    return carriage_status


@router.get("/", response_model=list[CarriageStatusRead])
async def get_carriage_statuses(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(CarriageStatus))
    return data.scalars().all()


@router.get("/{id}", response_model=CarriageStatusRead)
async def get_carriage_status(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    carriage_status = await session.get(CarriageStatus, id)
    if not carriage_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carriage status not found",
        )
    return carriage_status


@router.patch("/{id}", response_model=CarriageStatusRead)
async def update_carriage_status(
    id: int,
    data: CarriageStatusUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    carriage_status = await session.get(CarriageStatus, id)
    if not carriage_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carriage status not found",
        )

    carriage_status_data = data.model_dump(exclude_unset=True)
    for key, value in carriage_status_data.items():
        setattr(carriage_status, key, value)

    await session.commit()
    await session.refresh(carriage_status)
    return carriage_status


@router.delete("/{id}")
async def delete_carriage_status(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    carriage_status = await session.get(CarriageStatus, id)
    if not carriage_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carriage status not found",
        )

    await session.delete(carriage_status)
    await session.commit()
    return {"detail": "Carriage status deleted successfully"}
