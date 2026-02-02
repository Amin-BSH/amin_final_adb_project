from datetime import datetime

from pydantic import BaseModel


class FarmerInvoicePayedCreate(BaseModel):
    payed: bool | None = None
    farmer_id: int
    crop_year_id: int


class FarmerInvoicePayedUpdate(BaseModel):
    payed: bool | None = None
    farmer_id: int | None = None
    crop_year_id: int | None = None


class FarmerInvoicePayedRead(BaseModel):
    id: int
    payed: bool | None
    farmer_id: int
    crop_year_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
