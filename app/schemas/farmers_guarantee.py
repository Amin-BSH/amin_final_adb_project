from datetime import datetime

from pydantic import BaseModel


class FarmersGuaranteeCreate(BaseModel):
    guarantee_price: float | None = None
    guarantor_farmer_id: int
    guaranteed_farmer_id: int
    crop_year_id: int


class FarmersGuaranteeUpdate(BaseModel):
    guarantee_price: float | None = None
    guarantor_farmer_id: int | None = None
    guaranteed_farmer_id: int | None = None
    crop_year_id: int | None = None


class FarmersGuaranteeRead(BaseModel):
    id: int
    guarantee_price: float | None
    guarantor_farmer_id: int
    guaranteed_farmer_id: int
    crop_year_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
