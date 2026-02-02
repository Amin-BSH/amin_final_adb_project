from datetime import datetime

from pydantic import BaseModel


class UnitCreate(BaseModel):
    unit_name: str


class UnitRead(BaseModel):
    id: int
    unit_name: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class UnitUpdate(BaseModel):
    unit_name: str | None = None
