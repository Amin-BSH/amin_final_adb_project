from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.driver import Driver
from app.models.user import User
from app.schemas.driver import DriverCreate, DriverRead, DriverUpdate

router = APIRouter(prefix="/drivers", tags=["Drivers"])


@router.post("/", response_model=DriverRead)
async def create_driver(
    data: DriverCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data_validate = Driver(
        name=data.name,
        last_name=data.last_name,
        national_code=data.national_code,
        phone_number=data.phone_number,
        license_plate=data.license_plate,
        capacity_ton=data.capacity_ton,
        car_id=data.car_id,
    )
    session.add(data_validate)
    await session.commit()
    await session.refresh(data_validate)
    return data_validate


@router.get("/", response_model=list[DriverRead])
async def get_drivers(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(Driver))
    return data.scalars().all()


@router.get("/{id}", response_model=DriverRead)
async def get_driver(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    driver = await session.get(Driver, id)
    if not driver:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Driver not found")
    return driver


@router.patch("/{id}", response_model=DriverRead)
async def update_driver(
    id: int,
    data: DriverUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    driver = await session.get(Driver, id)

    if not driver:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Driver not found")

    driver_data = data.model_dump(exclude_unset=True)

    for key, value in driver_data.items():
        setattr(driver, key, value)

    await session.commit()
    await session.refresh(driver)
    return driver


@router.delete("/{id}")
async def delete_driver(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    driver = await session.get(Driver, id)

    if not driver:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Driver not found")

    await session.delete(driver)
    await session.commit()
    return {"detail": "Driver deleted successfully"}
