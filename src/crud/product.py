from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Product
from core.schemas.product import ProductCreate, ProductRead


async def get_all_products(session: AsyncSession) -> list[ProductRead]:
    stmt = select(Product).order_by(Product.id)
    result = await session.scalars(stmt)
    return [ProductRead.model_validate(product) for product in result.all()]


async def create_product(
    session: AsyncSession, product_create: ProductCreate
) -> ProductRead:
    product = Product(**product_create.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return ProductRead.model_validate(product)
