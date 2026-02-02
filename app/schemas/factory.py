from datetime import datetime

from pydantic import BaseModel


class FactoryCreate(BaseModel):
    factory_name: str


class FactoryRead(BaseModel):
    id: int
    factory_name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class FactoryUpdate(BaseModel):
    factory_name: str | None = None
