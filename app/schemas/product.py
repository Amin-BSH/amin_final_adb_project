from datetime import datetime

from pydantic import BaseModel, field_validator


class ProductCreate(BaseModel):
    product_name: str
    crop_year_id: int
    measure_unit_id: int

    @field_validator("product_name")
    @classmethod
    def validate_product_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Product name must not be empty")
        return v


class ProductUpdate(BaseModel):
    product_name: str | None = None
    crop_year_id: int | None = None
    measure_unit_id: int | None = None


class ProductRead(BaseModel):
    id: int
    product_name: str
    crop_year_id: int
    measure_unit_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
