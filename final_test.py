import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("FINAL API TEST - E-COMMERCE API")
print("=" * 60)

# 1. Test basic endpoints
print("\n1. 📍 BASIC ENDPOINTS:")
print("-" * 40)

endpoints = [
    ("GET", "/", "Root endpoint"),
    ("GET", "/products/categories", "Product categories"),
    ("GET", "/products/?limit=2", "Products list"),
    ("GET", "/products/1", "Single product"),
    ("GET", "/health", "Health check"),
]

for method, path, description in endpoints:
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{path}")
        else:
            response = requests.post(f"{BASE_URL}{path}")
        
        print(f"✅ {description}")
        print(f"   URL: {path}")
        print(f"   Status: {response.status_code}")
        if path == "/products/categories":
            data = response.json()
            print(f"   Categories: {', '.join(data['categories'])}")
        elif path == "/":
            data = response.json()
            print(f"   Message: {data['message']}")
        print()
    except Exception as e:
        print(f"❌ {description}: {e}")
        print()

# 2. Test authentication
print("\n2. 🔐 AUTHENTICATION:")
print("-" * 40)

# Login as customer
print("Testing login as customer (john_doe)...")
try:
    login_data = {"username": "john_doe", "password": "password123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Login successful!")
        print(f"   Token received: {token[:30]}...")
        
        # Test protected endpoint
        headers = {"Authorization": f"Bearer {token}"}
        me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if me_response.status_code == 200:
            user_data = me_response.json()
            print(f"✅ User info retrieved: {user_data['username']} ({user_data['role']})")
        else:
            print(f"❌ Failed to get user info: {me_response.status_code}")
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"❌ Error during auth test: {e}")

# 3. Test admin functionality
print("\n3. 👑 ADMIN FUNCTIONALITY:")
print("-" * 40)

print("Testing admin login...")
try:
    admin_login = {"username": "admin_user", "password": "password123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=admin_login)
    
    if response.status_code == 200:
        admin_token = response.json()["access_token"]
        print(f"✅ Admin login successful!")
        
        # Test admin-only endpoint
        headers = {"Authorization": f"Bearer {admin_token}"}
        users_response = requests.get(f"{BASE_URL}/users/", headers=headers)
        
        if users_response.status_code == 200:
            users = users_response.json()
            print(f"✅ Admin endpoint accessed successfully")
            print(f"   Found {len(users)} users")
        else:
            print(f"❌ Failed to access admin endpoint: {users_response.status_code}")
    else:
        print(f"❌ Admin login failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error during admin test: {e}")

print("\n" + "=" * 60)
print("🎉 API TEST COMPLETE!")
print("=" * 60)
print("\n📚 Available at:")
print(f"   • Swagger UI:      {BASE_URL}/docs")
print(f"   • ReDoc:           {BASE_URL}/redoc")
print(f"   • OpenAPI JSON:    {BASE_URL}/openapi.json")
print(f"   • Health check:    {BASE_URL}/health")
print("\n👤 Default users:")
print("   • Customer: john_doe / password123")
print("   • Admin:    admin_user / password123")
print("\n🛍️  Sample products available in categories:")
print("   • electronics, shoes, home, test")
