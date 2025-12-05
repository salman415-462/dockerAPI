# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.auth import get_current_active_user, require_admin
from app.db import db
from app.models import User, UserUpdate, UserCreate

router = APIRouter()


@router.get("/", response_model=List[User], dependencies=[Depends(require_admin)])
async def get_all_users(
        skip: int = 0,
        limit: int = 100,
        role: Optional[str] = None,
        is_active: Optional[bool] = None
):
    users = db.users

    # Filter by role
    if role:
        users = [u for u in users if u["role"] == role]

    # Filter by active status
    if is_active is not None:
        users = [u for u in users if u["is_active"] == is_active]

    # Apply pagination
    users = users[skip:skip + limit]

    # Remove hashed_password from response
    return [{k: v for k, v in u.items() if k != "hashed_password"} for u in users]


@router.get("/{user_id}", response_model=User)
async def get_user(
        user_id: int,
        current_user: User = Depends(get_current_active_user)
):
    # Users can only view their own profile unless they're admin
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    for user in db.users:
        if user["id"] == user_id:
            return User(**{k: v for k, v in user.items() if k != "hashed_password"})

    raise HTTPException(status_code=404, detail="User not found")


@router.put("/{user_id}", response_model=User)
async def update_user(
        user_id: int,
        user_update: UserUpdate,
        current_user: User = Depends(get_current_active_user)
):
    # Users can only update their own profile unless they're admin
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    for i, user in enumerate(db.users):
        if user["id"] == user_id:
            update_data = user_update.dict(exclude_unset=True)

            # Check for duplicate username/email
            if "username" in update_data:
                for u in db.users:
                    if u["id"] != user_id and u["username"] == update_data["username"]:
                        raise HTTPException(status_code=400, detail="Username already exists")

            if "email" in update_data:
                for u in db.users:
                    if u["id"] != user_id and u["email"] == update_data["email"]:
                        raise HTTPException(status_code=400, detail="Email already exists")

            # Hash password if provided
            if "password" in update_data:
                from app.auth import get_password_hash
                update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

            # Update user
            db.users[i].update(update_data)

            return User(**{k: v for k, v in db.users[i].items() if k != "hashed_password"})

    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}", dependencies=[Depends(require_admin)])
async def delete_user(user_id: int):
    for i, user in enumerate(db.users):
        if user["id"] == user_id:
            # Soft delete - set is_active to False
            db.users[i]["is_active"] = False
            return {"message": "User deactivated successfully"}

    raise HTTPException(status_code=404, detail="User not found")