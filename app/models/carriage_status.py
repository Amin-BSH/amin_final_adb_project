from sqlalchemy import BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class CarriageStatus(Base, TimestampMixin):
    __tablename__ = "carriage_status"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    carried: Mapped[bool] = mapped_column(Boolean, nullable=True)

    carriage_id: Mapped[int] = mapped_column(
        ForeignKey("carriage.id", ondelete="CASCADE"),
        nullable=False,
    )
    driver_id: Mapped[int] = mapped_column(
        ForeignKey("driver.id", ondelete="CASCADE"),
        nullable=False,
    )

    carriage: Mapped["Carriage"] = relationship(lazy="selectin")
    driver: Mapped["Driver"] = relationship(lazy="selectin")
