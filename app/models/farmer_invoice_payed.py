from sqlalchemy import BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class FarmerInvoicePayed(Base, TimestampMixin):
    __tablename__ = "farmer_invoice_payed"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    payed: Mapped[bool] = mapped_column(Boolean, nullable=True)

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
