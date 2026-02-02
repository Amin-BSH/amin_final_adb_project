from datetime import datetime

from pydantic import BaseModel


class CityCreate(BaseModel):
    city: str
    province_id: int


class CityUpdate(BaseModel):
    city: str


class CityRead(BaseModel):
    id: int
    city: str
    province_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
