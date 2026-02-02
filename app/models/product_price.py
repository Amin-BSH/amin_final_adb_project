from sqlalchemy import BigInteger, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class ProductPrice(Base, TimestampMixin):
    __tablename__ = "product_price"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sugar_amount_per_ton_kg: Mapped[float] = mapped_column(Float, nullable=False)
    sugar_price_per_kg: Mapped[float] = mapped_column(Float, nullable=False)
    pulp_amount_per_ton_kg: Mapped[float] = mapped_column(Float, nullable=False)
    pulp_price_per_kg: Mapped[float] = mapped_column(Float, nullable=False)

    crop_year_id: Mapped[int] = mapped_column(
        ForeignKey("crop_year.id", ondelete="CASCADE"),
        nullable=False,
    )

    crop_year: Mapped["CropYear"] = relationship(lazy="selectin")
