from sqlalchemy import BigInteger, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class FactorySeed(Base, TimestampMixin):
    __tablename__ = "factory_seed"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    amount: Mapped[float] = mapped_column(Float, nullable=True)
    farmer_price: Mapped[float] = mapped_column(Float, nullable=True)
    factory_price: Mapped[float] = mapped_column(Float, nullable=True)

    factory_id: Mapped[int] = mapped_column(
        ForeignKey("factory.id", ondelete="CASCADE"),
        nullable=False,
    )
    crop_year_id: Mapped[int] = mapped_column(
        ForeignKey("crop_year.id", ondelete="CASCADE"),
        nullable=False,
    )
    seed_id: Mapped[int] = mapped_column(
        ForeignKey("seed.id", ondelete="CASCADE"),
        nullable=False,
    )

    factory: Mapped["Factory"] = relationship(lazy="selectin")
    crop_year: Mapped["CropYear"] = relationship(lazy="selectin")
    seed: Mapped["Seed"] = relationship(lazy="selectin")
