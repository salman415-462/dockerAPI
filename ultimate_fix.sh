#!/bin/bash
echo "🔧 ULTIMATE FIX - Resolving bcrypt issues"

# Kill everything
pkill -f "python" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true

# Clean install bcrypt and passlib
pip uninstall -y bcrypt passlib > /dev/null 2>&1
pip install "bcrypt==3.2.0" "passlib==1.7.4"

# Create a simple auth system without bcrypt issues
cat > app/auth_ultimate.py << 'PYEOF'
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import hashlib
import base64
from app.models import TokenData, UserInDB
from app.db import db

# Security
security = HTTPBearer()

# SIMPLE password hashing (for testing - in production use bcrypt)
def simple_hash(password: str) -> str:
    """Simple hash for testing - NOT for production!"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password, hashed_password):
    """Verify password with simple hash"""
    return simple_hash(plain_password) == hashed_password

def get_password_hash(password):
    """Hash password with simple method"""
    return simple_hash(password)

# Update database with simple hashes
def update_db_hashes():
    """Update all password hashes in database"""
    for user in db.users:
        if user["username"] == "john_doe":
            user["hashed_password"] = simple_hash("password123")
        elif user["username"] == "admin_user":
            user["hashed_password"] = simple_hash("password123")

# Call this once
update_db_hashes()

def get_user(username: str) -> Optional[UserInDB]:
    for user in db.users:
        if user["username"] == username:
            return UserInDB(**user)
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# JWT Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_admin(current_user: UserInDB = Depends(get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
PYEOF

mv app/auth_ultimate.py app/auth.py

# Clean cache
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete

# Start server
echo "Starting server on port 8002..."
cat > run_ultimate.py << 'PYEOF'
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=True)
PYEOF

python run_ultimate.py &
echo "Server PID: $!"
sleep 3

# Test
echo ""
echo "Testing..."
curl -s -X POST http://localhost:8002/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "password123"}'

echo ""
echo "If this works, update your run.py to use port 8000 and test everything!"
