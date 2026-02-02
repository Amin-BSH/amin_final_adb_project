from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class City(Base, TimestampMixin):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    city: Mapped[str] = mapped_column(String, nullable=False, index=True)

    province_id: Mapped[int] = mapped_column(
        ForeignKey("province.id", ondelete="CASCADE"),
        nullable=False,
    )

    province: Mapped["Province"] = relationship(
        back_populates="cities", lazy="selectin"
    )

    villages: Mapped[list["Village"]] = relationship(
        back_populates="city",
        cascade="all, delete",
    )
