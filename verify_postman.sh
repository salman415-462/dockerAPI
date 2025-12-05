echo "=== POSTMAN VERIFICATION SCRIPT ==="

# Test 1: Server running
echo "1. Server health..."
curl -s http://localhost:8000/health | python3 -m json.tool

echo -e "\n2. Customer login..."
curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "password123"}' | \
  python3 -c "
import sys,json
try:
    data = json.load(sys.stdin)
    print('✅ Customer token obtained')
    print(f'   Token (first 30 chars): {data[\"access_token\"][:30]}...')
except:
    print('❌ Customer login failed')
"

echo -e "\n3. Admin login..."
curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin_user", "password": "password123"}' | \
  python3 -c "
import sys,json
try:
    data = json.load(sys.stdin)
    print('✅ Admin token obtained')
    print(f'   Token (first 30 chars): {data[\"access_token\"][:30]}...')
except:
    print('❌ Admin login failed')
"

echo -e "\n=== COPY THESE TO POSTMAN ==="
echo "Customer Token: Run POST /auth/login with john_doe credentials"
echo "Admin Token: Run POST /auth/login with admin_user credentials"
echo "Base URL: http://localhost:8000"
