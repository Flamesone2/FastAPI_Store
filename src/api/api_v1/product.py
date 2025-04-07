from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models.db_helper import db_helper
from core.schemas.product import ProductCreate, ProductRead
from crud.product import create_product, get_all_products

router = APIRouter(prefix=settings.api.v1.product, tags=["Products"])


@router.post("/", response_model=ProductRead)
async def create_new_product(
    product_create: ProductCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await create_product(session, product_create)


@router.get("/", response_model=list[ProductRead])
async def get_products(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await get_all_products(session)
