#!/bin/bash
echo "🚀 QUICK API TEST"
echo "================"

# Check if server is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Server is not running!"
    echo "   Start it with: python run.py"
    exit 1
fi

echo "✅ Server is running"

# Test key endpoints
echo ""
echo "Testing endpoints:"

test_endpoint() {
    local name=$1
    local url=$2
    local method=${3:-GET}
    local data=${4:-}
    
    if [ "$method" = "POST" ] && [ -n "$data" ]; then
        response=$(curl -s -X $method -H "Content-Type: application/json" -d "$data" "$url" -w " %{http_code}")
    else
        response=$(curl -s -X $method "$url" -w " %{http_code}")
    fi
    
    http_code=$(echo "$response" | awk '{print $NF}')
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
        echo "  ✅ $name: HTTP $http_code"
        return 0
    else
        echo "  ❌ $name: HTTP $http_code"
        return 1
    fi
}

# Test basic endpoints
test_endpoint "Root" "http://localhost:8000/"
test_endpoint "Health" "http://localhost:8000/health"
test_endpoint "Categories" "http://localhost:8000/products/categories"
test_endpoint "Products" "http://localhost:8000/products/?limit=1"

# Test authentication
echo ""
echo "Testing authentication:"
test_endpoint "Login" "http://localhost:8000/auth/login" "POST" '{"username": "john_doe", "password": "password123"}'

echo ""
echo "📊 Quick test complete!"
echo ""
echo "For comprehensive testing, run: python test_api_comprehensive.py"
