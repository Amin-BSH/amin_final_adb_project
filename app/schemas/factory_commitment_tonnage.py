from datetime import datetime

from pydantic import BaseModel


class FactoryCommitmentTonnageCreate(BaseModel):
    committed_tonnage_amount: float | None = None
    factory_id: int
    crop_year_id: int


class FactoryCommitmentTonnageUpdate(BaseModel):
    committed_tonnage_amount: float | None = None
    factory_id: int | None = None
    crop_year_id: int | None = None


class FactoryCommitmentTonnageRead(BaseModel):
    id: int
    committed_tonnage_amount: float | None
    factory_id: int
    crop_year_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
