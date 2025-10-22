"""Define os esquemas (schemas) Pydantic para a entidade Produto."""

from pydantic import BaseModel, ConfigDict
from typing import Optional
import uuid
from datetime import datetime


class ProductBase(BaseModel):
    """Esquema base para a entidade Produto."""

    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True


class ProductCreate(ProductBase):
    """Esquema para criação de um novo produto."""
    pass


class ProductUpdate(BaseModel):
    """Esquema para atualização de um produto existente."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None


class ProductInDBBase(ProductBase):
    """Esquema base para produtos armazenados no banco de dados, incluindo campos gerados pelo DB."""
    id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Product(ProductInDBBase):
    """Esquema completo para um produto, incluindo todos os detalhes do banco de dados."""
    pass
