from sqlalchemy import BigInteger, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class FarmersPesticide(Base, TimestampMixin):
    __tablename__ = "farmers_pesticide"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    pesticide_amount: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    price_for_all_farmers_checkbox: Mapped[bool] = mapped_column(Boolean, nullable=True)

    commitment_id: Mapped[int] = mapped_column(
        ForeignKey("commitment.id", ondelete="CASCADE"),
        nullable=False,
    )
    pesticide_id: Mapped[int] = mapped_column(
        ForeignKey("pesticide.id", ondelete="CASCADE"),
        nullable=False,
    )
    crop_year_id: Mapped[int] = mapped_column(
        ForeignKey("crop_year.id", ondelete="CASCADE"),
        nullable=False,
    )
    factory_id: Mapped[int] = mapped_column(
        ForeignKey("factory.id", ondelete="CASCADE"),
        nullable=False,
    )

    commitment: Mapped["Commitment"] = relationship(lazy="selectin")
    pesticide: Mapped["Pesticide"] = relationship(lazy="selectin")
    crop_year: Mapped["CropYear"] = relationship(lazy="selectin")
    factory: Mapped["Factory"] = relationship(lazy="selectin")
