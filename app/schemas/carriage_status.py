from datetime import datetime

from pydantic import BaseModel


class CarriageStatusCreate(BaseModel):
    carried: bool | None = None
    carriage_id: int
    driver_id: int


class CarriageStatusUpdate(BaseModel):
    carried: bool | None = None
    carriage_id: int | None = None
    driver_id: int | None = None


class CarriageStatusRead(BaseModel):
    id: int
    carried: bool | None
    carriage_id: int
    driver_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
