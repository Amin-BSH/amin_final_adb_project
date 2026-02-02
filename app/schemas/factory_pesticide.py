from datetime import datetime

from pydantic import BaseModel


class FactoryPesticideCreate(BaseModel):
    amount: float | None = None
    farmer_price: float | None = None
    factory_price: float | None = None
    factory_id: int
    crop_year_id: int
    pesticide_id: int


class FactoryPesticideUpdate(BaseModel):
    amount: float | None = None
    farmer_price: float | None = None
    factory_price: float | None = None
    factory_id: int | None = None
    crop_year_id: int | None = None
    pesticide_id: int | None = None


class FactoryPesticideRead(BaseModel):
    id: int
    amount: float | None
    farmer_price: float | None
    factory_price: float | None
    factory_id: int
    crop_year_id: int
    pesticide_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
