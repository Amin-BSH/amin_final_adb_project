from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.province import Province
from app.models.user import User
from app.schemas.province import ProvinceCreate, ProvinceRead, ProvinceUpdate

router = APIRouter(prefix="/provinces", tags=["Provinces"])


@router.post("/", response_model=ProvinceRead)
async def create_province(
    data: ProvinceCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data_validate = Province(province=data.province)
    province_similar = await session.execute(
        select(Province).where(Province.province == data_validate.province)
    )
    if province_similar.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The {data_validate.province} province already exits...",
        )
    session.add(data_validate)
    await session.commit()
    await session.refresh(data_validate)
    return data_validate


@router.get("/", response_model=list[ProvinceRead])
async def get_provinces(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(Province))
    return data.scalars().all()


@router.get("/{province_id}", response_model=ProvinceRead)
async def get_province(
    province_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    province = await session.get(Province, province_id)
    if not province:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Province not found"
        )
    return province


@router.patch("/{province_id}", response_model=ProvinceRead)
async def update_province(
    province_id: int,
    data: ProvinceUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    province = await session.get(Province, province_id)
    if not province:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Province not found"
        )

    province_data = data.model_dump(exclude_unset=True)

    for key, value in province_data.items():
        setattr(province, key, value)

    await session.commit()
    await session.refresh(province)
    return province


@router.delete("/{province_id}")
async def delete_province(
    province_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    province = await session.get(Province, province_id)
    if not province:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Province not found"
        )

    await session.delete(province)
    await session.commit()
    return {"detail": "Province deleted successfully"}
