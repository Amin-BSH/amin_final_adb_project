from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, model_validator


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    fullname: str
    phone_number: str
    role: str = "user"

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not v or len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        if not v or not v.isdigit() or len(v) != 11 or not v.startswith("0"):
            raise ValueError(
                "Phone number must be 11 digits starting with 0 (Iranian format)"
            )
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v not in ["user", "admin"]:
            raise ValueError("Role must be either 'user' or 'admin'")
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    fullname: Optional[str] = None
    phone_number: Optional[str] = None
    role: Optional[str] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        if v is not None and (
            not v or not v.isdigit() or len(v) != 11 or not v.startswith("0")
        ):
            raise ValueError(
                "Phone number must be 11 digits starting with 0 (Iranian format)"
            )
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v is not None and v not in ["user", "admin"]:
            raise ValueError("Role must be either 'user' or 'admin'")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not v or len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserRead(BaseModel):
    user_id: int
    username: str
    email: str
    fullname: str
    phone_number: str
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    user: UserRead


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v):
        if not v or len(v) < 8:
            raise ValueError("New password must be at least 8 characters long")
        return v

    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, v):
        if not v or len(v) < 8:
            raise ValueError("Password confirmation must be at least 8 characters long")
        return v

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("New password and confirmation password do not match")
        return self
