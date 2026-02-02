from sqlalchemy import BigInteger, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class FarmersPayment(Base, TimestampMixin):
    __tablename__ = "farmers_payment"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    payment_type: Mapped[int] = mapped_column(BigInteger, nullable=False)

    farmer_id: Mapped[int] = mapped_column(
        ForeignKey("farmer.id", ondelete="CASCADE"),
        nullable=False,
    )

    farmer: Mapped["Farmer"] = relationship(lazy="selectin")
