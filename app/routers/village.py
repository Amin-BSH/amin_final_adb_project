from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.user import User
from app.models.village import Village
from app.schemas.village import VillageCreate, VillageRead, VillageUpdate

router = APIRouter(prefix="/villages", tags=["Villages"])


@router.post("/", response_model=VillageRead)
async def create_village(
    data: VillageCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    village = Village(**data.model_dump())
    session.add(village)
    await session.commit()
    await session.refresh(village)
    return village


@router.get("/", response_model=list[VillageRead])
async def get_villages(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(Village))
    return data.scalars().all()


@router.get("/{village_id}", response_model=VillageRead)
async def get_village(
    village_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    village = await session.get(Village, village_id)
    if not village:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Village not found"
        )
    return village


@router.patch("/{village_id}", response_model=VillageRead)
async def update_village(
    village_id: int,
    data: VillageUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    village = await session.get(Village, village_id)
    if not village:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Village not found"
        )

    village_data = data.model_dump(exclude_unset=True)
    for key, value in village_data.items():
        setattr(village, key, value)
    await session.commit()
    await session.refresh(village)
    return village


@router.delete("/{village_id}")
async def delete_village(
    village_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    village = await session.get(Village, village_id)
    if not village:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Village not found"
        )

    await session.delete(village)
    await session.commit()
    return {"detail": "Village deleted successfully"}
