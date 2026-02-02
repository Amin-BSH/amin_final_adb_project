from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    product_name: Mapped[str] = mapped_column(String, nullable=False, index=True)

    crop_year_id: Mapped[int] = mapped_column(
        ForeignKey("crop_year.id", ondelete="CASCADE"),
        nullable=False,
    )
    measure_unit_id: Mapped[int] = mapped_column(
        ForeignKey("measure_unit.id", ondelete="CASCADE"),
        nullable=False,
    )

    crop_year: Mapped["CropYear"] = relationship(lazy="selectin")
    measure_unit: Mapped["MeasureUnit"] = relationship(lazy="selectin")
