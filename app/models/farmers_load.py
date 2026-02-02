from sqlalchemy import BigInteger, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class FarmersLoad(Base, TimestampMixin):
    __tablename__ = "farmers_load"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    date: Mapped[str] = mapped_column(String, nullable=False)
    load_number: Mapped[str] = mapped_column(String, nullable=False)
    driver_name: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    total_weight: Mapped[float] = mapped_column(Float, nullable=True)
    dirt_weight: Mapped[float] = mapped_column(Float, nullable=True)
    pest_weight: Mapped[float] = mapped_column(Float, nullable=True)
    pure_weight: Mapped[float] = mapped_column(Float, nullable=True)
    sugar_beet_polarity: Mapped[float] = mapped_column(Float, nullable=True)
    price_per_kilo: Mapped[float] = mapped_column(Float, nullable=True)
    rent_help: Mapped[float] = mapped_column(Float, nullable=True)
    transportation_cost: Mapped[float] = mapped_column(Float, nullable=True)
    quota_sugar_price: Mapped[float] = mapped_column(Float, nullable=True)
    quota_pulp_price: Mapped[float] = mapped_column(Float, nullable=True)
    pure_payable: Mapped[float] = mapped_column(Float, nullable=True)

    farmer_id: Mapped[int] = mapped_column(
        ForeignKey("farmer.id", ondelete="CASCADE"),
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

    farmer: Mapped["Farmer"] = relationship(lazy="selectin")
    crop_year: Mapped["CropYear"] = relationship(lazy="selectin")
    factory: Mapped["Factory"] = relationship(lazy="selectin")
