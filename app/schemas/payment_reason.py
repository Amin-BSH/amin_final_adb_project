from datetime import datetime

from pydantic import BaseModel

class PaymentReasonCreate(BaseModel):
    reason_name: str


class PaymentReasonRead(BaseModel):
    id: int
    reason_name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaymentReasonUpdate(BaseModel):
    reason_name: str | None = None
