from sqlalchemy import BigInteger, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class FarmersGuarantee(Base, TimestampMixin):
    __tablename__ = "farmers_guarantee"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    guarantee_price: Mapped[float] = mapped_column(Float, nullable=True)

    guarantor_farmer_id: Mapped[int] = mapped_column(
        ForeignKey("farmer.id", ondelete="CASCADE"),
        nullable=False,
    )
    guaranteed_farmer_id: Mapped[int] = mapped_column(
        ForeignKey("farmer.id", ondelete="CASCADE"),
        nullable=False,
    )
    crop_year_id: Mapped[int] = mapped_column(
        ForeignKey("crop_year.id", ondelete="CASCADE"),
        nullable=False,
    )

    guarantor_farmer: Mapped["Farmer"] = relationship(
        foreign_keys=[guarantor_farmer_id],
        lazy="selectin",
    )
    guaranteed_farmer: Mapped["Farmer"] = relationship(
        foreign_keys=[guaranteed_farmer_id],
        lazy="selectin",
    )
    crop_year: Mapped["CropYear"] = relationship(lazy="selectin")
