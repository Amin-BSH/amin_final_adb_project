from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class Village(Base, TimestampMixin):
    __tablename__ = "village"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    village: Mapped[str] = mapped_column(String, nullable=False, index=True)

    city_id: Mapped[int] = mapped_column(
        ForeignKey("city.id", ondelete="CASCADE"),
        nullable=False,
    )

    city: Mapped["City"] = relationship(back_populates="villages", lazy="selectin")
