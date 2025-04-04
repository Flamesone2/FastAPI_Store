from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Order, OrderItem
from core.schemas.order import OrderCreate, OrderRead


async def create_order(session: AsyncSession, order_create: OrderCreate) -> OrderRead:
    order = Order(user_id=order_create.user_id, status="pending")
    session.add(order)

    for item in order_create.items:
        order_item = OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price,
        )
        order.items.append(order_item)

    await session.commit()
    await session.refresh(order)
    return OrderRead.model_validate(order)
