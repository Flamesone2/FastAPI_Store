from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models.db_helper import db_helper
from core.schemas.order import OrderCreate, OrderRead
from crud.order import create_order

router = APIRouter(prefix=settings.api.v1.order, tags=["Orders"])


@router.post("/", response_model=OrderRead)
async def create_new_order(
    order_create: OrderCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await create_order(session, order_create)
