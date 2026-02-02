from datetime import datetime

from pydantic import BaseModel


class VillageCreate(BaseModel):
    village: str
    city_id: int


class VillageUpdate(BaseModel):
    village: str


class VillageRead(BaseModel):
    id: int
    village: str
    city_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
