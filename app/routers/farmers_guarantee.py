from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.farmers_guarantee import FarmersGuarantee
from app.models.user import User
from app.schemas.farmers_guarantee import (
    FarmersGuaranteeCreate,
    FarmersGuaranteeRead,
    FarmersGuaranteeUpdate,
)

router = APIRouter(prefix="/farmers_guarantee", tags=["Farmers Guarantee"])


@router.post("/", response_model=FarmersGuaranteeRead)
async def create_farmers_guarantee(
    data: FarmersGuaranteeCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_guarantee = FarmersGuarantee(**data.model_dump())
    session.add(farmers_guarantee)
    await session.commit()
    await session.refresh(farmers_guarantee)
    return farmers_guarantee


@router.get("/", response_model=list[FarmersGuaranteeRead])
async def get_farmers_guarantees(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(FarmersGuarantee))
    return data.scalars().all()


@router.get("/{id}", response_model=FarmersGuaranteeRead)
async def get_farmers_guarantee(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_guarantee = await session.get(FarmersGuarantee, id)
    if not farmers_guarantee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers guarantee not found",
        )
    return farmers_guarantee


@router.patch("/{id}", response_model=FarmersGuaranteeRead)
async def update_farmers_guarantee(
    id: int,
    data: FarmersGuaranteeUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_guarantee = await session.get(FarmersGuarantee, id)
    if not farmers_guarantee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers guarantee not found",
        )

    farmers_guarantee_data = data.model_dump(exclude_unset=True)
    for key, value in farmers_guarantee_data.items():
        setattr(farmers_guarantee, key, value)

    await session.commit()
    await session.refresh(farmers_guarantee)
    return farmers_guarantee


@router.delete("/{id}")
async def delete_farmers_guarantee(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    farmers_guarantee = await session.get(FarmersGuarantee, id)
    if not farmers_guarantee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmers guarantee not found",
        )

    await session.delete(farmers_guarantee)
    await session.commit()
    return {"detail": "Farmers guarantee deleted successfully"}
