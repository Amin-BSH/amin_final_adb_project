from datetime import datetime

from pydantic import BaseModel


class CropYearCreate(BaseModel):
    crop_year_name: str


class CropYearRead(BaseModel):
    id: int
    crop_year_name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CropYearUpdate(BaseModel):
    crop_year_name: str | None = None
