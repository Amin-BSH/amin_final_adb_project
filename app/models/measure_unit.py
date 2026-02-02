from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class MeasureUnit(Base, TimestampMixin):
    __tablename__ = "measure_unit"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    unit_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
