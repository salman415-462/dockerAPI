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
- 🐳 Docker containerized - runs anywhere!

## Quick Start (5 Minutes)

### Method 1: Using Docker (Recommended)

#### A. If you have Docker installed:
```bash
# 1. Clone the repository
git clone https://github.com/salman415-462/dockerAPI
cd dockerAPI

# 2. Build the Docker image
docker build -t ecommerce-api .

# 3. Run the container
docker run -d -p 9000:8000 --name ecommerce_container ecommerce-api

# 4. Access the API
#    Main URL: http://localhost:9000
#    API Docs: http://localhost:9000/docs
#    Products: http://localhost:9000/products/
