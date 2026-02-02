from datetime import datetime

from pydantic import BaseModel


class FarmersSugarDeliveryCreate(BaseModel):
    sugar_delivered: float
    sugar_deposit_amount: float
    farmer_id: int
    crop_year_id: int


class FarmersSugarDeliveryUpdate(BaseModel):
    sugar_delivered: float | None = None
    sugar_deposit_amount: float | None = None
    farmer_id: int | None = None
    crop_year_id: int | None = None


class FarmersSugarDeliveryRead(BaseModel):
    id: int
    sugar_delivered: float
    sugar_deposit_amount: float
    farmer_id: int
    crop_year_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
