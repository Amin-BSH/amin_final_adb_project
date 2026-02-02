from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.city import City
from app.models.user import User
from app.schemas.city import CityCreate, CityRead, CityUpdate

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("/", response_model=CityRead)
async def create_city(
    data: CityCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    city = City(**data.model_dump())
    session.add(city)
    await session.commit()
    await session.refresh(city)
    return city


@router.get("/", response_model=list[CityRead])
async def get_cities(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(City))
    return data.scalars().all()


@router.get("/{city_id}", response_model=CityRead)
async def get_city(
    city_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    city = await session.get(City, city_id)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return city


@router.patch("/{city_id}", response_model=CityRead)
async def update_city(
    city_id: int,
    data: CityUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    city = await session.get(City, city_id)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )

    city_data = data.model_dump(exclude_unset=True)

    for key, value in city_data.items():
        setattr(city, key, value)

    await session.commit()
    await session.refresh(city)
    return city


@router.delete("/{city_id}")
async def delete_city(
    city_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    city = await session.get(City, city_id)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )

    await session.delete(city)
    await session.commit()
    return {"detail": "City deleted successfully"}
