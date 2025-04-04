from pydantic import BaseModel
from pydantic import ConfigDict


class ProductBase(BaseModel):
    name: str
    price: int
    description: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
