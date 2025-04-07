from fastapi import APIRouter


from core.config import settings

from .auth_keycloak import router as auth_router
from .product import router as product_router
from .order import router as order_router

router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(auth_router)
router.include_router(product_router)
router.include_router(order_router)
