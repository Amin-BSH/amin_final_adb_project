from sqlalchemy import BigInteger, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class FarmersWasteDelivery(Base, TimestampMixin):
    __tablename__ = "farmers_waste_delivery"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    waste_delivered: Mapped[float] = mapped_column(Float, nullable=False)
    waste_deposit_amount: Mapped[float] = mapped_column(Float, nullable=False)

    farmer_id: Mapped[int] = mapped_column(
        ForeignKey("farmer.id", ondelete="CASCADE"),
        nullable=False,
    )
    crop_year_id: Mapped[int] = mapped_column(
        ForeignKey("crop_year.id", ondelete="CASCADE"),
        nullable=False,
    )

    farmer: Mapped["Farmer"] = relationship(lazy="selectin")
    crop_year: Mapped["CropYear"] = relationship(lazy="selectin")
