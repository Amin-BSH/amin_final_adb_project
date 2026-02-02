from sqlalchemy import BigInteger, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class Driver(Base, TimestampMixin):
    __tablename__ = "driver"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    national_code: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    phone_number: Mapped[str] = mapped_column(String(11), nullable=False, index=True)
    license_plate: Mapped[str] = mapped_column(String, nullable=True)
    capacity_ton: Mapped[float] = mapped_column(Float, nullable=True)

    car_id: Mapped[int] = mapped_column(
        ForeignKey("car.id", ondelete="CASCADE"), nullable=False
    )

    car: Mapped["Car"] = relationship(back_populates="drivers", lazy="selectin")  # noqa: F821
