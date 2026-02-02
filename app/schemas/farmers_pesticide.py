from datetime import datetime

from pydantic import BaseModel


class FarmersPesticideCreate(BaseModel):
    pesticide_amount: float
    price: float
    price_for_all_farmers_checkbox: bool | None = None
    commitment_id: int
    pesticide_id: int
    crop_year_id: int
    factory_id: int


class FarmersPesticideUpdate(BaseModel):
    pesticide_amount: float | None = None
    price: float | None = None
    price_for_all_farmers_checkbox: bool | None = None
    commitment_id: int | None = None
    pesticide_id: int | None = None
    crop_year_id: int | None = None
    factory_id: int | None = None


class FarmersPesticideRead(BaseModel):
    id: int
    pesticide_amount: float
    price: float
    price_for_all_farmers_checkbox: bool | None
    commitment_id: int
    pesticide_id: int
    crop_year_id: int
    factory_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
