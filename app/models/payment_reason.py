from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin


class PaymentReason(Base, TimestampMixin):
    __tablename__ = "payment_reason"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    reason_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
