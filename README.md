# README.md
# FastAPI E-Commerce API

A complete e-commerce API built with FastAPI featuring JWT authentication, products, carts, orders, and user management.

## Features

- 🔐 JWT Authentication with user roles (admin/customer)
- 🛍️ Products with filtering, sorting, and pagination
- 🛒 Shopping carts
- 📦 Orders management
- 👤 User management
- 🎯 Query parameters for filtering
- ✅ Input validation with Pydantic
- 🛡️ Role-based access control

## Installation


git clone https://github.com/salman415-462/dockerAPI
cd dockerAPI
docker build -t ecommerce-api .
docker run -d -p 9000:8000 --name ecommerce_container ecommerce-api

