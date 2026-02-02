from sqlalchemy import BigInteger, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class PurityPrice(Base, TimestampMixin):
    __tablename__ = "purity_price"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    base_purity: Mapped[float] = mapped_column(Float, nullable=False)
    base_purity_price: Mapped[float] = mapped_column(Float, nullable=False)
    price_difference: Mapped[float] = mapped_column(Float, nullable=False)

    crop_year_id: Mapped[int] = mapped_column(
        ForeignKey("crop_year.id", ondelete="CASCADE"),
        nullable=False,
    )

    crop_year: Mapped["CropYear"] = relationship(lazy="selectin")
