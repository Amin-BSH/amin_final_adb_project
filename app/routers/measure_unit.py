from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.dependencies import get_session
from app.models.measure_unit import MeasureUnit
from app.models.user import User
from app.schemas.measure_unit import UnitCreate, UnitRead, UnitUpdate

router = APIRouter(prefix="/measure_units", tags=["Measure Units"])


@router.post("/", response_model=UnitRead)
async def create_measure_unit(
    data: UnitCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data_validate = MeasureUnit(unit_name=data.unit_name)

    session.add(data_validate)
    await session.commit()
    await session.refresh(data_validate)
    return data_validate


@router.get("/", response_model=list[UnitRead])
async def get_measure_units(
    session: Session = Depends(get_session), user: User = Depends(get_current_user)
):
    data = await session.execute(select(MeasureUnit))
    return data.scalars().all()


@router.get("/{id}", response_model=UnitRead)
async def get_measure_unit(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    unit = await session.get(MeasureUnit, id)

    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Measure unit not found"
        )
    return unit


@router.patch("/{id}", response_model=UnitRead)
async def update_measure_unit(
    id: int,
    data: UnitUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    unit = await session.get(MeasureUnit, id)

    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Measure unit not found"
        )

    data_validate = data.model_dump(exclude_unset=True)

    for key, value in data_validate.items():
        setattr(unit, key, value)

    await session.commit()
    await session.refresh(unit)
    return unit


@router.delete("/{id}")
async def delete_measure_unit(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    unit = await session.get(MeasureUnit, id)

    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Measure unit not found"
        )

    await session.delete(unit)
    await session.commit()
    return {"detail": "Measure unit deleted successfully"}
