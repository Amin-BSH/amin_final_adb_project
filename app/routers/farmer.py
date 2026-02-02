from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.farmer import Farmer
from app.models.user import User
from app.schemas.farmer import FarmRead, FarmerUpdate, FarmerCreate

router = APIRouter(prefix="/farmers", tags=["Farmers"])


@router.post("/", response_model=FarmRead)
async def create_farmer(
    data: FarmerCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data_validate = Farmer(
        national_id=data.national_id,
        full_name=data.full_name,
        father_name=data.father_name,
        card_number=data.card_number,
        sheba_number_1=data.sheba_number_1,
        sheba_number_2=data.sheba_number_2,
        address=data.address,
        phone_number=data.phone_number,
    )

    session.add(data_validate)
    await session.commit()
    await session.refresh(data_validate)
    return data_validate


@router.get("/", response_model=list[FarmRead])
async def get_farmers(
    session: Session = Depends(get_session), user: User = Depends(get_current_user)
):
    data = await session.execute(select(Farmer))
    return data.scalars().all()


@router.get("/{id}", response_model=FarmRead)
async def get_farmer(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmer = await session.get(Farmer, id)
    if not farmer:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Farmer not found")

    return farmer


@router.patch("/{id}", response_model=FarmRead)
async def update_farmer(
    id: int,
    data: FarmerUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmer = await session.get(Farmer, id)

    if not farmer:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Farmer not found")

    farmer_data = data.model_dump(exclude_unset=True)

    for key, value in farmer_data.items():
        setattr(farmer, key, value)

    await session.commit()
    await session.refresh(farmer)
    return farmer


@router.delete("/{id}")
async def delete_farmer(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmer = await session.get(Farmer, id)

    if not farmer:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Farmer not found")

    await session.delete(farmer)
    await session.commit()
    return {"detail": "Farmer deleted successfully"}
