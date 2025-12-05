#!/bin/bash

echo "=== Testing E-Commerce API ==="
echo "API URL: http://localhost:8000"
echo ""

# Test basic endpoints
endpoints=(
    "/"
    "/health"
    "/docs"
    "/redoc"
    "/openapi.json"
)

for endpoint in "${endpoints[@]}"; do
    echo -n "Testing $endpoint... "
    if curl -s -f "http://localhost:8000$endpoint" > /dev/null; then
        echo "✅"
    else
        echo "❌"
    fi
done

echo ""
echo "Testing API endpoints..."

# Try common e-commerce endpoints
api_endpoints=(
    "/api/products"
    "/api/users"
    "/api/categories"
    "/api/auth/login"
    "/api/orders"
    "/api/cart"
)

for endpoint in "${api_endpoints[@]}"; do
    echo -n "$endpoint: "
    response=$(curl -s -w "%{http_code}" "http://localhost:8000$endpoint" -o /dev/null)
    if [ "$response" = "200" ]; then
        echo "✅ (200 OK)"
        # Show sample data for products
        if [ "$endpoint" = "/api/products" ]; then
            echo "   Sample:"
            curl -s "http://localhost:8000$endpoint" | python3 -m json.tool | head -10
        fi
    elif [ "$response" = "404" ]; then
        echo "⚠️  (404 Not Found - might need different path)"
    else
        echo "❌ ($response)"
    fi
done

echo ""
echo "=== Quick Access ==="
echo "API Documentation: http://localhost:8000/docs"
echo "Alternative Docs:   http://localhost:8000/redoc"
echo "Health Check:       http://localhost:8000/health"
