from typing import List, Optional
from pydantic import BaseModel, Field

# Product Models
class ProductBase(BaseModel):
    name: str
    price: float = Field(gt=0)
    category: str
    stock: int = Field(ge=0)
    description: Optional[str] = None
    imageUrl: Optional[str] = None
    isActive: bool = True
    tags: List[str] = []
    rating: float = Field(ge=0, le=5, default=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    stock: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    imageUrl: Optional[str] = None
    isActive: Optional[bool] = None
    tags: Optional[List[str]] = None
    rating: Optional[float] = Field(None, ge=0, le=5)

class Product(ProductBase):
    id: int
    createdAt: str

# User Models - Using str instead of EmailStr to avoid email-validator issues
class UserBase(BaseModel):
    username: str
    email: str  # Changed from EmailStr
    role: str = "customer"

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)

class User(UserBase):
    id: int
    is_active: bool
    created_at: str

class UserInDB(User):
    hashed_password: str

# Auth Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# Cart Models
class CartItemBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    price: float

class CartBase(BaseModel):
    status: str = "active"

class CartCreate(CartBase):
    items: List[CartItemCreate]

class Cart(CartBase):
    id: int
    user_id: int
    items: List[CartItem]
    total_amount: float
    created_at: str

# Order Models
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItem(OrderItemBase):
    price_at_purchase: float

class OrderBase(BaseModel):
    shipping_address: str
    payment_method: str = "credit_card"

class OrderCreate(OrderBase):
    cart_id: int

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    shipping_address: Optional[str] = None

class Order(OrderBase):
    id: int
    user_id: int
    cart_id: int
    items: List[OrderItem]
    total: float
    status: str
    created_at: str
