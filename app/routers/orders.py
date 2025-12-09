# app/routers/orders.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.auth import get_current_active_user, require_admin
from app.db import db
from app.models import Order, OrderCreate, OrderUpdate, User
from app.schemas import OrderQueryParams, PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse)
async def get_orders(
        status: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        page: int = 1,
        limit: int = 10,
        current_user: User = Depends(get_current_active_user)
):
    # Filter orders based on user role
    if current_user.role == "admin":
        orders = db.orders.copy()
    else:
        orders = [o for o in db.orders if o["user_id"] == current_user.id]

    # Apply status filter
    if status:
        orders = [o for o in orders if o["status"] == status]

    # Apply sorting
    reverse = sort_order.lower() == "desc"
    orders.sort(key=lambda x: x.get(sort_by, ""), reverse=reverse)

    # Apply pagination
    total = len(orders)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_orders = orders[start_idx:end_idx]

    total_pages = (total + limit - 1) // limit

    return PaginatedResponse(
        items=paginated_orders,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages
    )


@router.get("/{order_id}", response_model=Order)
async def get_order(
        order_id: int,
        current_user: User = Depends(get_current_active_user)
):
    for order in db.orders:
        if order["id"] == order_id:
            if order["user_id"] != current_user.id and current_user.role != "admin":
                raise HTTPException(status_code=403, detail="Not enough permissions")
            return Order(**order)

    raise HTTPException(status_code=404, detail="Order not found")


@router.post("/", response_model=Order)
async def create_order(
        order_data: OrderCreate,
        current_user: User = Depends(get_current_active_user)
):
    # Find cart
    cart = None
    for c in db.carts:
        if c["id"] == order_data.cart_id and c["user_id"] == current_user.id:
            cart = c
            break

    if not cart or cart["status"] != "active":
        raise HTTPException(status_code=404, detail="Cart not found or inactive")

    # Validate stock
    for item in cart["items"]:
        for product in db.products:
            if product["id"] == item["product_id"]:
                if product["stock"] < item["quantity"]:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Insufficient stock for product {product['name']}"
                    )
                break

    # Reduce stock
    for item in cart["items"]:
        for i, product in enumerate(db.products):
            if product["id"] == item["product_id"]:
                db.products[i]["stock"] -= item["quantity"]
                break

    # Create order items with price at purchase
    order_items = []
    for item in cart["items"]:
        # Find current price
        current_price = item["price"]
        for product in db.products:
            if product["id"] == item["product_id"]:
                current_price = product["price"]
                break

        order_items.append({
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "price_at_purchase": current_price
        })

    new_order = {
        "id": db.get_next_order_id(),
        "user_id": current_user.id,
        "cart_id": order_data.cart_id,
        "items": order_items,
        "total": cart["total_amount"],
        "status": "pending",
        "shipping_address": order_data.shipping_address,
        "payment_method": order_data.payment_method,
        "created_at": "2024-01-15"
    }

    # Update cart status
    for i, c in enumerate(db.carts):
        if c["id"] == order_data.cart_id:
            db.carts[i]["status"] = "completed"
            break

    db.orders.append(new_order)
    return Order(**new_order)


@router.put("/{order_id}/status", response_model=Order)
async def update_order_status(
        order_id: int,
        status_update: OrderUpdate,
        current_user: User = Depends(require_admin)
):
    update_data = status_update.dict(exclude_unset=True)

    for i, order in enumerate(db.orders):
        if order["id"] == order_id:

            # Update all fields dynamically
            for key, value in update_data.items():
                db.orders[i][key] = value

            return Order(**db.orders[i])

    raise HTTPException(status_code=404, detail="Order not found")



@router.get("/stats/summary")
async def get_order_stats(current_user: User = Depends(require_admin)):
    total_orders = len(db.orders)
    total_revenue = sum(order["total"] for order in db.orders)

    status_counts = {}
    for order in db.orders:
        status = order["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "status_counts": status_counts
    }