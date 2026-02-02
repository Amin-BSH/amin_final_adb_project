from datetime import datetime

from pydantic import BaseModel, field_validator


class FarmersLoadCreate(BaseModel):
    date: str
    load_number: str
    driver_name: str
    phone_number: str
    total_weight: float | None = None
    dirt_weight: float | None = None
    pest_weight: float | None = None
    pure_weight: float | None = None
    sugar_beet_polarity: float | None = None
    price_per_kilo: float | None = None
    rent_help: float | None = None
    transportation_cost: float | None = None
    quota_sugar_price: float | None = None
    quota_pulp_price: float | None = None
    pure_payable: float | None = None
    farmer_id: int
    crop_year_id: int
    factory_id: int

    @field_validator("date")
    @classmethod
    def validate_date(cls, v):
        if not v or not v.strip():
            raise ValueError("Date must not be empty")
        return v


class FarmersLoadUpdate(BaseModel):
    date: str | None = None
    load_number: str | None = None
    driver_name: str | None = None
    phone_number: str | None = None
    total_weight: float | None = None
    dirt_weight: float | None = None
    pest_weight: float | None = None
    pure_weight: float | None = None
    sugar_beet_polarity: float | None = None
    price_per_kilo: float | None = None
    rent_help: float | None = None
    transportation_cost: float | None = None
    quota_sugar_price: float | None = None
    quota_pulp_price: float | None = None
    pure_payable: float | None = None
    farmer_id: int | None = None
    crop_year_id: int | None = None
    factory_id: int | None = None


class FarmersLoadRead(BaseModel):
    id: int
    date: str
    load_number: str
    driver_name: str
    phone_number: str
    total_weight: float | None
    dirt_weight: float | None
    pest_weight: float | None
    pure_weight: float | None
    sugar_beet_polarity: float | None
    price_per_kilo: float | None
    rent_help: float | None
    transportation_cost: float | None
    quota_sugar_price: float | None
    quota_pulp_price: float | None
    pure_payable: float | None
    farmer_id: int
    crop_year_id: int
    factory_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
