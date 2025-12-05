# app/routers/carts.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.auth import get_current_active_user
from app.db import db
from app.models import Cart, CartCreate, CartItemCreate, User

router = APIRouter()


@router.get("/", response_model=List[Cart])
async def get_user_carts(current_user: User = Depends(get_current_active_user)):
    user_carts = []
    for cart in db.carts:
        if cart["user_id"] == current_user.id:
            user_carts.append(cart)
    return user_carts


@router.get("/{cart_id}", response_model=Cart)
async def get_cart(cart_id: int, current_user: User = Depends(get_current_active_user)):
    for cart in db.carts:
        if cart["id"] == cart_id:
            if cart["user_id"] != current_user.id and current_user.role != "admin":
                raise HTTPException(status_code=403, detail="Not enough permissions")
            return Cart(**cart)

    raise HTTPException(status_code=404, detail="Cart not found")


@router.post("/", response_model=Cart)
async def create_cart(cart_data: CartCreate, current_user: User = Depends(get_current_active_user)):
    # Validate products exist and are active
    items = []
    total_amount = 0

    for item in cart_data.items:
        product = None
        for p in db.products:
            if p["id"] == item.product_id and p["isActive"]:
                product = p
                break

        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found or inactive")

        if product["stock"] < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product['name']}")

        item_total = product["price"] * item.quantity
        items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": product["price"]
        })
        total_amount += item_total

    new_cart = {
        "id": db.get_next_cart_id(),
        "user_id": current_user.id,
        "items": items,
        "total_amount": total_amount,
        "status": cart_data.status,
        "created_at": "2024-01-15"
    }

    db.carts.append(new_cart)
    return Cart(**new_cart)


@router.post("/{cart_id}/items", response_model=Cart)
async def add_to_cart(
        cart_id: int,
        item_data: CartItemCreate,
        current_user: User = Depends(get_current_active_user)
):
    # Find cart
    cart = None
    cart_index = -1
    for i, c in enumerate(db.carts):
        if c["id"] == cart_id:
            if c["user_id"] != current_user.id:
                raise HTTPException(status_code=403, detail="Not enough permissions")
            cart = c
            cart_index = i
            break

    if not cart or cart["status"] != "active":
        raise HTTPException(status_code=404, detail="Cart not found or inactive")

    # Find product
    product = None
    for p in db.products:
        if p["id"] == item_data.product_id and p["isActive"]:
            product = p
            break

    if not product:
        raise HTTPException(status_code=404, detail="Product not found or inactive")

    if product["stock"] < item_data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Check if product already in cart
    item_exists = False
    for i, item in enumerate(cart["items"]):
        if item["product_id"] == item_data.product_id:
            cart["items"][i]["quantity"] += item_data.quantity
            item_exists = True
            break

    if not item_exists:
        cart["items"].append({
            "product_id": item_data.product_id,
            "quantity": item_data.quantity,
            "price": product["price"]
        })

    # Recalculate total
    total_amount = 0
    for item in cart["items"]:
        total_amount += item["price"] * item["quantity"]

    cart["total_amount"] = total_amount

    # Update cart in database
    db.carts[cart_index] = cart

    return Cart(**cart)


@router.delete("/{cart_id}", response_model=dict)
async def delete_cart(cart_id: int, current_user: User = Depends(get_current_active_user)):
    for i, cart in enumerate(db.carts):
        if cart["id"] == cart_id:
            if cart["user_id"] != current_user.id and current_user.role != "admin":
                raise HTTPException(status_code=403, detail="Not enough permissions")

            # Mark cart as cancelled
            db.carts[i]["status"] = "cancelled"
            return {"message": "Cart cancelled successfully"}

    raise HTTPException(status_code=404, detail="Cart not found")