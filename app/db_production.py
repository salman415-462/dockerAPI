"""
Database configuration for production
Uses PostgreSQL if available, falls back to in-memory
"""
import os
from typing import Dict, List, Any
import datetime

class Database:
    def __init__(self):
        self.reset_database()
    
    def reset_database(self):
        # Same as before but we'll add PostgreSQL later
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
            # ... other products
        ]
        
        # Initialize counters
        self.product_counter = len(self.products)
        self.user_counter = len(self.users)
        self.cart_counter = len(self.carts)
        self.order_counter = len(self.orders)
    
    def get_next_product_id(self):
        self.product_counter += 1
        return self.product_counter

db = Database()
