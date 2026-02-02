from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.dependencies import get_session
from app.models.user import User
from app.models.pesticide import Pesticide
from app.schemas.pesticide import PesticideCreate, PesticideRead, PesticideUpdate


router = APIRouter(prefix="/pesticides", tags=["Pesticides"])


@router.post("/", response_model=PesticideRead)
async def create_pesticide(
    data: PesticideCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = Pesticide(
        pesticide_name=data.pesticide_name, measure_unit_id=data.measure_unit_id
    )

    session.add(data)
    await session.commit()
    await session.refresh(data)
    return data


@router.get("/", response_model=list[PesticideRead])
async def get_pesticides(
    session: Session = Depends(get_session), user: User = Depends(get_current_user)
):
    data = await session.execute(select(Pesticide))

    return data.scalars().all()


@router.get("/{id}", response_model=PesticideRead)
async def get_pesticide(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    pesticide = await session.get(Pesticide, id)

    if not pesticide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pesticide not found"
        )

    return pesticide


@router.patch("/{id}", response_model=PesticideRead)
async def update_pesticide(
    id: int,
    data: PesticideUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    pesticide = await session.get(Pesticide, id)

    if not pesticide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pesticide not found"
        )
    data_validate = data.model_dump(exclude_unset=True)

    for key, value in data_validate.items():
        setattr(pesticide, key, value)

    await session.commit()
    await session.refresh(pesticide)
    return pesticide


@router.delete(path="/{id}")
async def delete_pesticide(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    pesticide = await session.get(Pesticide, id)

    if not pesticide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pesticide not found"
        )

    await session.delete(pesticide)
    await session.commit()
    return {"detail": "Pesticide deleted successfully"}
