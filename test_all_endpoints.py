import json
import subprocess
import sys

def run_curl(url, method="GET", data=None, token=None):
    cmd = ["curl", "-s", "-X", method, url]
    if data:
        cmd.extend(["-H", "Content-Type: application/json", "-d", json.dumps(data)])
    if token:
        cmd.extend(["-H", f"Authorization: Bearer {token}"])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

print("=== Testing all API endpoints ===\n")

# 1. Test public endpoints
print("1. Testing public endpoints:")
print("-" * 40)

# Root
print("GET /")
result = run_curl("http://localhost:8000/")
print(json.dumps(json.loads(result), indent=2))

# Categories
print("\nGET /products/categories")
result = run_curl("http://localhost:8000/products/categories")
print(json.dumps(json.loads(result), indent=2))

# Products with filters
print("\nGET /products/?category=electronics&limit=2")
result = run_curl("http://localhost:8000/products/?category=electronics&limit=2")
print(json.dumps(json.loads(result), indent=2))

# Single product
print("\nGET /products/1")
result = run_curl("http://localhost:8000/products/1")
print(json.dumps(json.loads(result), indent=2))

# 2. Test authentication
print("\n2. Testing authentication:")
print("-" * 40)

# Login
print("POST /auth/login (john_doe)")
login_data = {"username": "john_doe", "password": "password123"}
result = run_curl("http://localhost:8000/auth/login", "POST", login_data)
try:
    login_result = json.loads(result)
    token = login_result.get("access_token")
    print(f"Login successful! Token: {token[:50]}...")
    
    # Test protected endpoint
    print("\nGET /auth/me (with token)")
    result = run_curl("http://localhost:8000/auth/me", token=token)
    print(json.dumps(json.loads(result), indent=2))
    
except json.JSONDecodeError as e:
    print(f"Error: {e}")
    print(f"Response: {result}")

# 3. Test admin endpoints
print("\n3. Testing admin login:")
print("-" * 40)

# Admin login
print("POST /auth/login (admin_user)")
admin_login = {"username": "admin_user", "password": "password123"}
result = run_curl("http://localhost:8000/auth/login", "POST", admin_login)
try:
    admin_result = json.loads(result)
    admin_token = admin_result.get("access_token")
    print(f"Admin login successful! Token: {admin_token[:50]}...")
    
    # Test admin-only endpoint
    print("\nGET /users/ (admin only)")
    result = run_curl("http://localhost:8000/users/", token=admin_token)
    print(json.dumps(json.loads(result), indent=2))
    
except json.JSONDecodeError as e:
    print(f"Error: {e}")
    print(f"Response: {result}")

print("\n" + "=" * 50)
print("✅ All tests completed!")
print("Visit http://localhost:8000/docs for interactive API testing")
