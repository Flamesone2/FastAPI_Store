from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float
from .base import Base
from .mixins import IdIntPkMixin


class Product(IdIntPkMixin, Base):
    name: Mapped[str] = mapped_column(String, index=True)
    price: Mapped[float] = mapped_column(Float)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
