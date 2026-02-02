from datetime import datetime

from pydantic import BaseModel, field_validator


class CarriageCreate(BaseModel):
    loading_date: str
    weight: float
    carriage_fee_per_ton: float
    origin_id: int
    destination_id: int
    farmer_id: int
    village_id: int

    @field_validator("weight", "carriage_fee_per_ton")
    @classmethod
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError("Value must be positive")
        return v


class CarriageUpdate(BaseModel):
    loading_date: str | None = None
    weight: float | None = None
    carriage_fee_per_ton: float | None = None
    origin_id: int | None = None
    destination_id: int | None = None
    farmer_id: int | None = None
    village_id: int | None = None


class CarriageRead(BaseModel):
    id: int
    loading_date: str
    weight: float
    carriage_fee_per_ton: float
    origin_id: int
    destination_id: int
    farmer_id: int
    village_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
