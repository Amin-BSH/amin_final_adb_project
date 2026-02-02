from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.factory import Factory
from app.models.user import User
from app.schemas.factory import FactoryRead, FactoryUpdate, FactoryCreate

router = APIRouter(prefix="/factories", tags=["Factories"])


@router.post("/", response_model=FactoryRead)
async def create_factory(
    data: FactoryCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data_validate = Factory(factory_name=data.factory_name)

    session.add(data_validate)
    await session.commit()
    await session.refresh(data_validate)
    return data_validate


@router.get("/", response_model=list[FactoryRead])
async def get_factories(
    session: Session = Depends(get_session), user: User = Depends(get_current_user)
):
    data = await session.execute(select(Factory))
    return data.scalars().all()


@router.get("/{id}", response_model=FactoryRead)
async def get_factory(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory = await session.get(Factory, id)

    if not factory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Factory not found"
        )
    return factory


@router.patch("/{id}", response_model=FactoryRead)
async def update_factory(
    id: int,
    data: FactoryUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory = await session.get(Factory, id)

    if not factory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Factory not found"
        )

    factory_data = data.model_dump(exclude_unset=True)

    for key, value in factory_data.items():
        setattr(factory, key, value)

    await session.commit()
    await session.refresh(factory)
    return factory


@router.delete("/{id}")
async def delete_factory(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    factory = await session.get(Factory, id)

    if not factory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Factory not found"
        )
    await session.delete(factory)
    await session.commit()
    return {"detail": "Factory deleted successfully"}
