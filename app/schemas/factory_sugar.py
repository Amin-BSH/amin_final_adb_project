from datetime import datetime

from pydantic import BaseModel


class FactorySugarCreate(BaseModel):
    amount: float | None = None
    sugar_weight_received_factory: float | None = None
    sugar_price_received_factory: float | None = None
    factory_id: int
    crop_year_id: int


class FactorySugarUpdate(BaseModel):
    amount: float | None = None
    sugar_weight_received_factory: float | None = None
    sugar_price_received_factory: float | None = None
    factory_id: int | None = None
    crop_year_id: int | None = None


class FactorySugarRead(BaseModel):
    id: int
    amount: float | None
    sugar_weight_received_factory: float | None
    sugar_price_received_factory: float | None
    factory_id: int
    crop_year_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
