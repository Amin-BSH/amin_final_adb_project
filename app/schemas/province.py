from datetime import datetime

from pydantic import BaseModel, field_validator


class ProvinceCreate(BaseModel):
    province: str

    @field_validator("province")
    @classmethod
    def capitalize_province(cls, v):
        return v.title()


class ProvinceUpdate(BaseModel):
    province: str

    @field_validator("province")
    @classmethod
    def capitalize_province(cls, v):
        return v.title()


class ProvinceRead(BaseModel):
    id: int
    province: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
