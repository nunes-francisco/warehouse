from pydantic import BaseModel, ConfigDict
from typing import Optional
import uuid
from datetime import datetime


class ProductBase(BaseModel):
    """ Base schema for Product entity. """
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None


class ProductInDBBase(ProductBase):
    id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Product(ProductInDBBase):
    pass
