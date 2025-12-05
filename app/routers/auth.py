from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import (
    authenticate_user, create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash,
    get_current_active_user, require_admin
)
from app.db import db
from app.models import UserCreate, User, Token, LoginRequest

router = APIRouter()

@router.post("/signup", response_model=User)
async def signup(user_data: UserCreate):
    # Check if user already exists
    for user in db.users:
        if user["username"] == user_data.username:
            raise HTTPException(
                status_code=400,
                detail="Username already registered"
            )
        if user["email"] == user_data.email:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
    
    # Create new user
    new_user = {
        "id": db.get_next_user_id(),
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": get_password_hash(user_data.password),
        "role": user_data.role,
        "is_active": True,
        "created_at": "2024-01-15"
    }
    
    db.users.append(new_user)
    return User(**{k: v for k, v in new_user.items() if k != "hashed_password"})

@router.post("/login", response_model=Token)
async def login(form_data: LoginRequest):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.post("/admin-test")
async def admin_test(current_user: User = Depends(require_admin)):
    return {"message": "Admin access granted", "user": current_user.username}
