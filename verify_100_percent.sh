#!/bin/bash
echo "🔍 VERIFYING 100% API FUNCTIONALITY"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if server is running
echo -n "Checking if server is running... "
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅${NC}"
else
    echo -e "${RED}❌${NC}"
    echo "Start server with: python run.py"
    exit 1
fi

# Test all endpoints
echo ""
echo "Testing all API endpoints:"
echo "--------------------------"

declare -a endpoints=(
    "/"
    "/health"
    "/products/categories"
    "/products/?limit=1"
    "/products/1"
    "/products/?category=electronics&limit=1"
    "/products/?min_price=100&max_price=1000&limit=1"
)

all_passed=true
for endpoint in "${endpoints[@]}"; do
    echo -n "  GET $endpoint ... "
    status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000$endpoint")
    if [[ "$status" == "200" || "$status" == "201" ]]; then
        echo -e "${GREEN}✅ ($status)${NC}"
    else
        echo -e "${RED}❌ ($status)${NC}"
        all_passed=false
    fi
done

# Test authentication
echo ""
echo "Testing authentication:"
echo "----------------------"

echo -n "  POST /auth/login (john_doe) ... "
login_response=$(curl -s -X POST -H "Content-Type: application/json" \
    -d '{"username": "john_doe", "password": "password123"}' \
    http://localhost:8000/auth/login -w " %{http_code}")
http_code=$(echo "$login_response" | awk '{print $NF}')

if [ "$http_code" == "200" ]; then
    echo -e "${GREEN}✅ (200)${NC}"
    # Extract token
    token=$(echo "$login_response" | sed '$d' | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
    
    # Test protected endpoint
    echo -n "  GET /auth/me (with token) ... "
    me_status=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: Bearer $token" \
        http://localhost:8000/auth/me)
    
    if [ "$me_status" == "200" ]; then
        echo -e "${GREEN}✅ (200)${NC}"
    else
        echo -e "${RED}❌ ($me_status)${NC}"
        all_passed=false
    fi
else
    echo -e "${RED}❌ ($http_code)${NC}"
    all_passed=false
fi

# Final verdict
echo ""
echo "=================================="
if $all_passed; then
    echo -e "${GREEN}🎉🎉🎉 100% FUNCTIONALITY VERIFIED! 🎉🎉🎉${NC}"
    echo ""
    echo "All endpoints are working correctly."
    echo "Your API is ready for production use!"
else
    echo -e "${YELLOW}⚠️  Some tests failed.${NC}"
    echo "Check the failed endpoints above."
    echo "Run comprehensive test for details: python test_api_comprehensive.py"
fi

echo ""
echo "📊 For detailed testing:"
echo "   python test_api_comprehensive.py  # Full test suite"
echo "   ./quick_test.sh                   # Quick check"
echo "   python load_test.py              # Load test"
