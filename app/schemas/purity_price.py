from datetime import datetime

from pydantic import BaseModel, field_validator


class PurityPriceCreate(BaseModel):
    base_purity: float
    base_purity_price: float
    price_difference: float
    crop_year_id: int

    @field_validator("base_purity", "base_purity_price", "price_difference")
    @classmethod
    def validate_not_negative(cls, v):
        if v < 0:
            raise ValueError("Value must not be negative")
        return v


class PurityPriceUpdate(BaseModel):
    base_purity: float | None = None
    base_purity_price: float | None = None
    price_difference: float | None = None
    crop_year_id: int | None = None


class PurityPriceRead(BaseModel):
    id: int
    base_purity: float
    base_purity_price: float
    price_difference: float
    crop_year_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
