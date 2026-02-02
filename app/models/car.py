from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class Car(Base, TimestampMixin):
    __tablename__ = "car"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    drivers: Mapped[list["Driver"]] = relationship(
        back_populates="car", cascade="all, delete"
    )
