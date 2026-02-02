from sqlalchemy import BigInteger, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.database import Base
from app.models.base import TimestampMixin


class Commitment(Base, TimestampMixin):
    __tablename__ = "commitment"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    commitment_number: Mapped[str] = mapped_column(String(50), nullable=False)
    amount_of_land: Mapped[float] = mapped_column(Float, nullable=False)
    withdrawal_amount: Mapped[float] = mapped_column(Float, nullable=False)
    date_set: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    crop_year_id: Mapped[int] = mapped_column(
        ForeignKey("crop_year.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    farmer_id: Mapped[int] = mapped_column(
        ForeignKey("farmer.id", ondelete="CASCADE"),
        nullable=False,
    )
    village_id: Mapped[int] = mapped_column(
        ForeignKey("village.id", ondelete="CASCADE"),
        nullable=False,
    )

    crop_year: Mapped["CropYear"] = relationship(lazy="selectin")
    user: Mapped["User"] = relationship(lazy="selectin")
    farmer: Mapped["Farmer"] = relationship(lazy="selectin")
    village: Mapped["Village"] = relationship(lazy="selectin")
