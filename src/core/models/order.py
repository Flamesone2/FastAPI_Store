from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, String, Float
from typing import TYPE_CHECKING
from .base import Base
from .mixins import IdIntPkMixin

if TYPE_CHECKING:
    from user_profile import UserProfile


class Order(IdIntPkMixin, Base):
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("user_profiles.user_id"), index=True
    )
    status: Mapped[str] = mapped_column(String, default="pending")

    profile: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="orders"
    )
    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")


class OrderItem(IdIntPkMixin, Base):
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    order: Mapped["Order"] = relationship("Order", back_populates="items")
