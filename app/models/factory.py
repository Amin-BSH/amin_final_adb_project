from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin


class Factory(Base, TimestampMixin):
    __tablename__ = "factory"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    factory_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
