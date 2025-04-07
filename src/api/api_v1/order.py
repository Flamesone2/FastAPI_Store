from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from core.models.db_helper import db_helper
from core.schemas.order import OrderCreate, OrderRead
from crud.order import create_order, get_orders_by_user
from api.api_v1.dependencies.user import get_current_user


router = APIRouter(prefix=settings.api.v1.order, tags=["Orders"])


@router.post("/", response_model=OrderRead)
async def create_new_order(
    order_create: OrderCreate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    order_create.user_id = user_id
    return await create_order(session, order_create)


@router.get("/user_orders", response_model=list[OrderRead])
async def get_user_orders(
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await get_orders_by_user(session, user_id)
