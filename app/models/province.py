from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class Province(Base, TimestampMixin):
    __tablename__ = "province"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    province: Mapped[str] = mapped_column(String, nullable=False, index=True)

    cities: Mapped[list["City"]] = relationship(
        back_populates="province",
        cascade="all, delete",
    )
