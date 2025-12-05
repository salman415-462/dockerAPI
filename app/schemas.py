from typing import Optional, List
from pydantic import BaseModel

# Query parameter schemas
class ProductQueryParams(BaseModel):
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    tag: Optional[str] = None
    search: Optional[str] = None
    is_active: Optional[bool] = True
    sort_by: Optional[str] = "id"
    sort_order: Optional[str] = "asc"
    page: Optional[int] = 1
    limit: Optional[int] = 10

class OrderQueryParams(BaseModel):
    status: Optional[str] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"
    page: Optional[int] = 1
    limit: Optional[int] = 10

# Response schemas
class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    limit: int
    total_pages: int
