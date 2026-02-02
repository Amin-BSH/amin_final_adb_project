from sqlalchemy import BigInteger, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class Carriage(Base, TimestampMixin):
    __tablename__ = "carriage"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    loading_date: Mapped[str] = mapped_column(String(10), nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    carriage_fee_per_ton: Mapped[float] = mapped_column(Float, nullable=False)

    origin_id: Mapped[int] = mapped_column(
        ForeignKey("city.id", ondelete="CASCADE"),
        nullable=False,
    )
    destination_id: Mapped[int] = mapped_column(
        ForeignKey("city.id", ondelete="CASCADE"),
        nullable=False,
    )
    farmer_id: Mapped[int] = mapped_column(
        ForeignKey("farmer.id", ondelete="CASCADE"),
        nullable=False,
    )
    village_id: Mapped[int] = mapped_column(
        ForeignKey("village.id", ondelete="CASCADE"),
        nullable=False,
    )

    origin: Mapped["City"] = relationship(
        foreign_keys=[origin_id],
        lazy="selectin",
    )
    destination: Mapped["City"] = relationship(
        foreign_keys=[destination_id],
        lazy="selectin",
    )
    farmer: Mapped["Farmer"] = relationship(lazy="selectin")
    village: Mapped["Village"] = relationship(lazy="selectin")
