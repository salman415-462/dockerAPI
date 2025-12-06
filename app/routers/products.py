from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from app.auth import require_admin
from app.db import db
from app.models import Product, ProductCreate, ProductUpdate
from app.schemas import PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse)
async def get_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    is_active: Optional[bool] = True,
    sort_by: str = "id",
    sort_order: str = "asc",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    products = db.products.copy()

    # Filtering
    if category:
        products = [p for p in products if p["category"].lower() == category.lower()]
    if min_price is not None:
        products = [p for p in products if p["price"] >= min_price]
    if max_price is not None:
        products = [p for p in products if p["price"] <= max_price]
    if tag:
        products = [p for p in products if tag.lower() in [t.lower() for t in p.get("tags", [])]]
    if search:
        search_lower = search.lower()
        products = [p for p in products if search_lower in p["name"].lower() or search_lower in p.get("description", "").lower()]
    if is_active is not None:
        products = [p for p in products if p["isActive"] == is_active]

    # Sorting
    reverse = sort_order.lower() == "desc"
    if sort_by == "price":
        products.sort(key=lambda x: x["price"], reverse=reverse)
    elif sort_by == "rating":
        products.sort(key=lambda x: x.get("rating", 0), reverse=reverse)
    elif sort_by == "name":
        products.sort(key=lambda x: x["name"].lower(), reverse=reverse)
    else:
        products.sort(key=lambda x: x["id"], reverse=reverse)

    # Pagination
    total = len(products)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_products = products[start_idx:end_idx] if start_idx < total else []
    total_pages = (total + limit - 1) // limit if total > 0 else 1

    return PaginatedResponse(
        items=paginated_products,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages
    )


@router.get("/categories")
async def get_categories():
    categories = {p["category"] for p in db.products if p["isActive"]}
    return {"categories": list(categories)}


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int):
    for product in db.products:
        if product["id"] == product_id:
            if not product["isActive"]:
                raise HTTPException(status_code=404, detail="Product not found")
            return Product(**product)
    raise HTTPException(status_code=404, detail="Product not found")


# Fixed POST route
# AFTER
@router.post("/", response_model=Product, dependencies=[Depends(require_admin)], status_code=201)
async def create_product(product_data: ProductCreate):
    new_product = {
        "id": db.get_next_product_id(),
        **product_data.dict(),
        "createdAt": "2024-01-15"
    }
    db.products.append(new_product)
    return Product(**new_product)




@router.put("/{product_id}", response_model=Product, dependencies=[Depends(require_admin)])
async def update_product(product_id: int, product_update: ProductUpdate):
    for i, product in enumerate(db.products):
        if product["id"] == product_id:
            update_data = product_update.dict(exclude_unset=True)
            db.products[i].update(update_data)
            return Product(**db.products[i])
    raise HTTPException(status_code=404, detail="Product not found")


@router.delete("/{product_id}", dependencies=[Depends(require_admin)])
async def delete_product(product_id: int):
    for i, product in enumerate(db.products):
        if product["id"] == product_id:

            db.products[i]["isActive"] = False
            return {"message": "Product deactivated successfully"}
    raise HTTPException(status_code=404, detail="Product not found")
