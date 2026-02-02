from datetime import datetime

from pydantic import BaseModel


class FarmersSeedCreate(BaseModel):
    seed_amount: float
    price: float
    price_for_all_farmers_checkbox: bool | None = None
    commitment_id: int
    seed_id: int
    crop_year_id: int
    factory_id: int


class FarmersSeedUpdate(BaseModel):
    seed_amount: float | None = None
    price: float | None = None
    price_for_all_farmers_checkbox: bool | None = None
    commitment_id: int | None = None
    seed_id: int | None = None
    crop_year_id: int | None = None
    factory_id: int | None = None


class FarmersSeedRead(BaseModel):
    id: int
    seed_amount: float
    price: float
    price_for_all_farmers_checkbox: bool | None
    commitment_id: int
    seed_id: int
    crop_year_id: int
    factory_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
