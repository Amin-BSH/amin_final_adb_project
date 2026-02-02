from datetime import datetime

from pydantic import BaseModel, field_validator


class FarmerCreate(BaseModel):
    full_name: str
    father_name: str
    national_id: str
    phone_number: str
    sheba_number_1: str
    sheba_number_2: str
    card_number: str
    address: str

    @field_validator("national_id")
    @classmethod
    def validate_national_code(cls, v):
        """Validate that the national id is Iranian (10 digits)"""
        if not v or not v.isdigit() or len(v) != 10:
            raise ValueError("National id must be exactly 10 digits (Iranian format)")
        return v

    @field_validator("card_number")
    @classmethod
    def validate_card_number(cls, v):
        """Validate card number. The card number must contain 16 character"""

        if not v or not v.isdigit() or len(v) != 16:
            raise ValueError("Card number must be exactly 10 digits")

        return v

    @field_validator("sheba_number_1")
    @classmethod
    def validate_sheba_number_1(cls, v):
        """Validate sheba number. The sheba number must contain 24 characters"""

        if not v or not v.isdigit() or len(v) != 24:
            raise ValueError(
                "Sheba number must be exactly 24 characters and IR not be concluded."
            )
        return v

    @field_validator("sheba_number_2")
    @classmethod
    def validate_sheba_number_2(cls, v):
        """Validate sheba number. The sheba number must contain 24 characters"""

        if not v or not v.isdigit() or len(v) != 24:
            raise ValueError(
                "Sheba number must be exactly 24 characters and IR not be concluded."
            )
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


class FarmerUpdate(BaseModel):
    full_name: str | None = None
    father_name: str | None = None
    national_id: str | None = None
    phone_number: str | None = None
    sheba_number_1: str | None = None
    sheba_number_2: str | None = None
    card_number: str | None = None
    address: str | None = None

    @field_validator("national_id")
    @classmethod
    def validate_national_code(cls, v):
        """Validate that the national id is Iranian (10 digits)"""
        if not v or not v.isdigit() or len(v) != 10:
            raise ValueError("National id must be exactly 10 digits (Iranian format)")
        return v

    @field_validator("card_number")
    @classmethod
    def validate_card_number(cls, v):
        """Validate card number. The card number must contain 16 character"""

        if not v or not v.isdigit() or len(v) != 16:
            raise ValueError("Card number must be exactly 10 digits")

        return v

    @field_validator("sheba_number_1")
    @classmethod
    def validate_sheba_number_1(cls, v):
        """Validate sheba number. The sheba number must contain 24 characters"""

        if not v or not v.isdigit() or len(v) != 24:
            raise ValueError(
                "Sheba number must be exactly 24 characters and IR not be concluded."
            )

        return v

    @field_validator("sheba_number_2")
    @classmethod
    def validate_sheba_number_2(cls, v):
        """Validate sheba number. The sheba number must contain 24 characters"""

        if not v or not v.isdigit() or len(v) != 24:
            raise ValueError(
                "Sheba number must be exactly 24 characters and IR not be concluded."
            )

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


class FarmRead(BaseModel):
    id: int
    full_name: str
    father_name: str
    national_id: str
    phone_number: str
    sheba_number_1: str
    sheba_number_2: str
    card_number: str
    address: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
