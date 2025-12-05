# app/db.py
from typing import Dict, List, Any
import datetime


# In-memory database
class Database:
    def __init__(self):
        self.reset_database()

    def reset_database(self):
        self.products = [
            {
                "id": 1,
                "name": "iPhone 15",
                "price": 999,
                "category": "electronics",
                "stock": 50,
                "description": "Latest iPhone with A16 chip",
                "imageUrl": "https://example.com/iphone.jpg",
                "isActive": True,
                "tags": ["smartphone", "apple", "premium"],
                "rating": 4.8,
                "createdAt": "2024-01-15"
            },
            {
                "id": 2,
                "name": "MacBook Pro 16",
                "price": 2399,
                "category": "electronics",
                "stock": 25,
                "description": "Professional laptop with M3 chip",
                "imageUrl": "https://example.com/macbook.jpg",
                "isActive": True,
                "tags": ["laptop", "apple", "premium"],
                "rating": 4.9,
                "createdAt": "2024-01-20"
            },
            {
                "id": 3,
                "name": "Nike Air Max",
                "price": 129,
                "category": "shoes",
                "stock": 100,
                "description": "Comfortable running shoes",
                "imageUrl": "https://example.com/nike.jpg",
                "isActive": True,
                "tags": ["shoes", "sports", "nike"],
                "rating": 4.5,
                "createdAt": "2024-01-10"
            },
            {
                "id": 4,
                "name": "Coffee Maker",
                "price": 89,
                "category": "home",
                "stock": 40,
                "description": "Automatic coffee maker",
                "imageUrl": "https://example.com/coffee.jpg",
                "isActive": True,
                "tags": ["kitchen", "appliance", "coffee"],
                "rating": 4.3,
                "createdAt": "2024-01-05"
            },
            {
                "id": 5,
                "name": "Test Product",
                "price": 99.99,
                "category": "test",
                "stock": 1000,
                "description": "Test product for demonstration",
                "imageUrl": "https://example.com/test.jpg",
                "isActive": True,
                "tags": ["test"],
                "rating": 3.5,
                "createdAt": "2024-01-01"
            }
        ]

        self.users = [
            {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password123"
                "role": "customer",
                "is_active": True,
                "created_at": "2024-01-01"
            },
            {
                "id": 2,
                "username": "admin_user",
                "email": "admin@example.com",
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password123"
                "role": "admin",
                "is_active": True,
                "created_at": "2024-01-01"
            }
        ]

        self.carts = [
            {
                "id": 1,
                "user_id": 1,
                "items": [
                    {
                        "product_id": 1,
                        "quantity": 2,
                        "price": 999
                    },
                    {
                        "product_id": 3,
                        "quantity": 1,
                        "price": 129
                    }
                ],
                "total_amount": 2127,
                "status": "active",
                "created_at": "2024-01-15"
            }
        ]

        self.orders = [
            {
                "id": 1,
                "user_id": 1,
                "cart_id": 1,
                "items": [
                    {
                        "product_id": 1,
                        "quantity": 2,
                        "price_at_purchase": 999
                    }
                ],
                "total": 1998,
                "status": "pending",
                "shipping_address": "123 Main St, City",
                "payment_method": "credit_card",
                "created_at": "2024-01-16"
            }
        ]

        self.product_counter = len(self.products)
        self.user_counter = len(self.users)
        self.cart_counter = len(self.carts)
        self.order_counter = len(self.orders)

    def get_next_product_id(self):
        self.product_counter += 1
        return self.product_counter

    def get_next_user_id(self):
        self.user_counter += 1
        return self.user_counter

    def get_next_cart_id(self):
        self.cart_counter += 1
        return self.cart_counter

    def get_next_order_id(self):
        self.order_counter += 1
        return self.order_counter


db = Database()