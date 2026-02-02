from datetime import datetime

from pydantic import BaseModel, field_validator


class CommitmentCreate(BaseModel):
    commitment_number: str
    amount_of_land: float
    withdrawal_amount: float
    date_set: datetime | None = None
    crop_year_id: int
    user_id: int
    farmer_id: int
    village_id: int

    @field_validator("amount_of_land", "withdrawal_amount")
    @classmethod
    def validate_positive(cls, v):
        if v < 0:
            raise ValueError("Value must not be negative")
        return v


class CommitmentUpdate(BaseModel):
    commitment_number: str | None = None
    amount_of_land: float | None = None
    withdrawal_amount: float | None = None
    date_set: datetime | None = None
    crop_year_id: int | None = None
    user_id: int | None = None
    farmer_id: int | None = None
    village_id: int | None = None


class CommitmentRead(BaseModel):
    id: int
    commitment_number: str
    amount_of_land: float
    withdrawal_amount: float
    date_set: datetime | None
    crop_year_id: int
    user_id: int
    farmer_id: int
    village_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
