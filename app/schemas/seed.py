from datetime import datetime

from pydantic import BaseModel


class SeedCreate(BaseModel):
    seed_name: str
    measure_unit_id: int


class SeedRead(BaseModel):
    id: int
    seed_name: str
    measure_unit_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SeedUpdate(BaseModel):
    seed_name: str | None = None
    measure_unit_id: int | None = None
