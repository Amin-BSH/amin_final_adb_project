from datetime import datetime

from pydantic import BaseModel


class FarmersWasteDeliveryCreate(BaseModel):
    waste_delivered: float
    waste_deposit_amount: float
    farmer_id: int
    crop_year_id: int


class FarmersWasteDeliveryUpdate(BaseModel):
    waste_delivered: float | None = None
    waste_deposit_amount: float | None = None
    farmer_id: int | None = None
    crop_year_id: int | None = None


class FarmersWasteDeliveryRead(BaseModel):
    id: int
    waste_delivered: float
    waste_deposit_amount: float
    farmer_id: int
    crop_year_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
