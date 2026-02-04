from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.car import Car
from app.models.user import User
from app.schemas.car import CarCreate, CarRead, CarUpdate

router = APIRouter(prefix="/car", tags=["Cars"])


@router.post("/", response_model=CarRead)
async def create_car(
    data: CarCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data_validate = Car(name=data.name)
    similar_car = await session.execute(
        select(Car).where(Car.name == data_validate.name)
    )
    if similar_car.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Car with this name already exists",
        )
    session.add(data_validate)
    await session.commit()
    await session.refresh(data_validate)
    return data_validate


@router.get("/", response_model=list[CarRead])
async def get_cars(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(Car))
    return data.scalars().all()


@router.get("/{id}", response_model=CarRead)
async def get_car(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    car = await session.get(Car, id)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
        )
    return car


@router.patch("/{id}", response_model=CarRead)
async def update_car(
    id: int,
    data: CarUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    car = await session.get(Car, id)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
        )

    car_data = data.model_dump(exclude_unset=True)

    for key, value in car_data.items():
        setattr(car, key, value)

    await session.commit()
    await session.refresh(car)
    return car


#@router.delete("/{id}")
#async def delete_car(
        #id: int,
    #session: Session = Depends(get_session),
    #user: User = Depends(get_current_user),
    #):
    #    car = await session.get(Car, id)
#    if not car:
        #raise HTTPException(
                #status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
            #                    )
#
#    await session.delete(car)
#    await session.commit()
#    return {"detail": "Car deleted successfully"}
