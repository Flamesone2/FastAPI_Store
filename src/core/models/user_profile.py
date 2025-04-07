from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from .base import Base
from .mixins import IdIntPkMixin

if TYPE_CHECKING:
    from core.models import Order


class UserProfile(IdIntPkMixin, Base):
    user_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    address: Mapped[str | None] = mapped_column(String, nullable=True)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="profile")
