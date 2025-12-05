#!/bin/bash
echo "=== Testing E-Commerce API ==="

echo "1. Testing root endpoint..."
curl -s http://localhost:8000/ | python3 -m json.tool

echo -e "\n2. Getting product categories..."
curl -s http://localhost:8000/products/categories | python3 -m json.tool

echo -e "\n3. Getting products with filters..."
curl -s "http://localhost:8000/products/?category=electronics&limit=2" | python3 -m json.tool

echo -e "\n4. Getting specific product..."
curl -s http://localhost:8000/products/1 | python3 -m json.tool

echo -e "\n=== API is working! Visit http://localhost:8000/docs for full documentation ==="
