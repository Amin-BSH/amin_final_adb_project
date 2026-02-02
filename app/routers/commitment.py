from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.commitment import Commitment
from app.models.user import User
from app.schemas.commitment import CommitmentCreate, CommitmentRead, CommitmentUpdate

router = APIRouter(prefix="/commitment", tags=["Commitments"])


@router.post("/", response_model=CommitmentRead)
async def create_commitment(
    data: CommitmentCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    commitment = Commitment(**data.model_dump())
    session.add(commitment)
    await session.commit()
    await session.refresh(commitment)
    return commitment


@router.get("/", response_model=list[CommitmentRead])
async def get_commitments(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = await session.execute(select(Commitment))
    return data.scalars().all()


@router.get("/{id}", response_model=CommitmentRead)
async def get_commitment(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    commitment = await session.get(Commitment, id)
    if not commitment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Commitment not found"
        )
    return commitment


@router.patch("/{id}", response_model=CommitmentRead)
async def update_commitment(
    id: int,
    data: CommitmentUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    commitment = await session.get(Commitment, id)
    if not commitment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Commitment not found"
        )

    commitment_data = data.model_dump(exclude_unset=True)
    for key, value in commitment_data.items():
        setattr(commitment, key, value)

    await session.commit()
    await session.refresh(commitment)
    return commitment


@router.delete("/{id}")
async def delete_commitment(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    commitment = await session.get(Commitment, id)
    if not commitment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Commitment not found"
        )

    await session.delete(commitment)
    await session.commit()
    return {"detail": "Commitment deleted successfully"}
