from datetime import datetime

from pydantic import BaseModel


class FactorySeedCreate(BaseModel):
    amount: float | None = None
    farmer_price: float | None = None
    factory_price: float | None = None
    factory_id: int
    crop_year_id: int
    seed_id: int


class FactorySeedUpdate(BaseModel):
    amount: float | None = None
    farmer_price: float | None = None
    factory_price: float | None = None
    factory_id: int | None = None
    crop_year_id: int | None = None
    seed_id: int | None = None


class FactorySeedRead(BaseModel):
    id: int
    amount: float | None
    farmer_price: float | None
    factory_price: float | None
    factory_id: int
    crop_year_id: int
    seed_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
