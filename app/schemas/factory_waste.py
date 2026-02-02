from datetime import datetime

from pydantic import BaseModel


class FactoryWasteCreate(BaseModel):
    amount: float | None = None
    waste_weight_received_factory: float | None = None
    waste_price_received_factory: float | None = None
    factory_id: int
    crop_year_id: int


class FactoryWasteUpdate(BaseModel):
    amount: float | None = None
    waste_weight_received_factory: float | None = None
    waste_price_received_factory: float | None = None
    factory_id: int | None = None
    crop_year_id: int | None = None


class FactoryWasteRead(BaseModel):
    id: int
    amount: float | None
    waste_weight_received_factory: float | None
    waste_price_received_factory: float | None
    factory_id: int
    crop_year_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
