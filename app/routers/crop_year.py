from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.dependencies import get_session
from app.models.crop_year import CropYear
from app.models.user import User
from app.schemas.crop_year import CropYearCreate, CropYearRead, CropYearUpdate

router = APIRouter(prefix="/crop_years", tags=["Crop Years"])


@router.post(path="/", response_model=CropYearRead)
async def create_crop_year(
    data: CropYearCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data_validate = CropYear(crop_year_name=data.crop_year_name)

    session.add(data_validate)
    await session.commit()
    await session.refresh(data_validate)
    return data_validate


@router.get(path="/", response_model=list[CropYearRead])
async def get_crop_years(
    session: Session = Depends(get_session), user: User = Depends(get_current_user)
):
    data = await session.execute(select(CropYear))

    return data.scalars().all()


@router.get(path="/{id}", response_model=CropYearRead)
async def get_crop_year(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    crop_year = await session.get(CropYear, id)

    if not crop_year:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Crop year not found"
        )

    return crop_year


@router.patch(path="/{id}", response_model=CropYearRead)
async def update_crop_year(
    id: int,
    data: CropYearUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    crop_year = await session.get(CropYear, id)

    if not crop_year:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Crop year not found"
        )

    data_validate = data.model_dump(exclude_unset=True)

    for key, value in data_validate.items():
        setattr(crop_year, key, value)

    await session.commit()
    await session.refresh(crop_year)
    return crop_year


@router.delete(path="/{id}")
async def delete_crop_year(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    crop_year = await session.get(CropYear, id)

    if not crop_year:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Crop year not found"
        )

    await session.delete(crop_year)
    await session.commit()
    return {"detail": "Crop year deleted successfully"}
