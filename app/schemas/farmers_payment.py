from datetime import datetime

from pydantic import BaseModel


class FarmersPaymentCreate(BaseModel):
    price: float
    payment_type: int
    farmer_id: int


class FarmersPaymentUpdate(BaseModel):
    price: float | None = None
    payment_type: int | None = None
    farmer_id: int | None = None


class FarmersPaymentRead(BaseModel):
    id: int
    price: float
    payment_type: int
    farmer_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
