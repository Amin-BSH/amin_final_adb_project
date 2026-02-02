from datetime import datetime

from pydantic import BaseModel


class PesticideCreate(BaseModel):
    pesticide_name: str
    measure_unit_id: int


class PesticideRead(BaseModel):
    id: int
    pesticide_name: str
    measure_unit_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PesticideUpdate(BaseModel):
    pesticide_name: str | None = None
    measure_unit_id: int | None = None
