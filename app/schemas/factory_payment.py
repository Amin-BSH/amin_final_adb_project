from datetime import datetime

from pydantic import BaseModel


class FactoryPaymentCreate(BaseModel):
    title: str | None = None
    date: datetime | None = None
    price: float | None = None
    factory_id: int
    crop_year_id: int
    user_id: int


class FactoryPaymentUpdate(BaseModel):
    title: str | None = None
    date: datetime | None = None
    price: float | None = None
    factory_id: int | None = None
    crop_year_id: int | None = None
    user_id: int | None = None


class FactoryPaymentRead(BaseModel):
    id: int
    title: str | None
    date: datetime | None
    price: float | None
    factory_id: int
    crop_year_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
