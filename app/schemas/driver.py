from datetime import datetime

from pydantic import BaseModel, field_validator


class DriverCreate(BaseModel):
    name: str
    last_name: str
    national_code: str
    phone_number: str
    license_plate: str
    capacity_ton: float
    car_id: int

    @field_validator("national_code")
    @classmethod
    def validate_national_code(cls, v):
        """Validate that the national code is Iranian (10 digits)"""
        if not v or not v.isdigit() or len(v) != 10:
            raise ValueError("National code must be exactly 10 digits (Iranian format)")
        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        """Validate that the phone number is Iranian (11 digits, starting with 0)"""
        if not v or not v.isdigit() or len(v) != 11 or not v.startswith("0"):
            raise ValueError(
                "Phone number must be 11 digits starting with 0 (Iranian format)"
            )
        return v


class DriverUpdate(BaseModel):
    name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    license_plate: str | None = None
    capacity_ton: float | None = None

    @field_validator("phone_number", mode="before")
    @classmethod
    def validate_phone_number(cls, v):
        """Validate that the phone number is Iranian (11 digits, starting with 0)"""
        # Convert empty strings to None
        if v == "":
            return None
        if v is not None and (not v.isdigit() or len(v) != 11 or not v.startswith("0")):
            raise ValueError(
                "Phone number must be 11 digits starting with 0 (Iranian format)"
            )
        return v


class DriverRead(BaseModel):
    id: int
    name: str
    last_name: str
    national_code: str
    phone_number: str
    license_plate: str | None
    capacity_ton: float | None
    car_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
