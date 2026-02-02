from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class Pesticide(Base, TimestampMixin):
    __tablename__ = "pesticide"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    pesticide_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    measure_unit_id: Mapped[int] = mapped_column(
        ForeignKey("measure_unit.id", ondelete="CASCADE"),
        nullable=False,
    )

    measure_unit: Mapped["MeasureUnit"] = relationship(lazy="selectin")  # type: ignore # noqa: F821
