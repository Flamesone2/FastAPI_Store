from typing import List
from pydantic import BaseModel
from pydantic import ConfigDict


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int


class OrderBase(BaseModel):
    user_id: str
    status: str = "pending"


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderRead(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    items: List[OrderItemRead]
