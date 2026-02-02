from datetime import datetime

from pydantic import BaseModel, field_validator


class ProductPriceCreate(BaseModel):
    sugar_amount_per_ton_kg: float
    sugar_price_per_kg: float
    pulp_amount_per_ton_kg: float
    pulp_price_per_kg: float
    crop_year_id: int

    @field_validator(
        "sugar_amount_per_ton_kg",
        "sugar_price_per_kg",
        "pulp_amount_per_ton_kg",
        "pulp_price_per_kg",
    )
    @classmethod
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError("Value must be positive")
        return v


class ProductPriceUpdate(BaseModel):
    sugar_amount_per_ton_kg: float | None = None
    sugar_price_per_kg: float | None = None
    pulp_amount_per_ton_kg: float | None = None
    pulp_price_per_kg: float | None = None
    crop_year_id: int | None = None


class ProductPriceRead(BaseModel):
    id: int
    sugar_amount_per_ton_kg: float
    sugar_price_per_kg: float
    pulp_amount_per_ton_kg: float
    pulp_price_per_kg: float
    crop_year_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
