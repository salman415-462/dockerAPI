import requests
import json

BASE_URL = "http://localhost:8000"

print("Minimal API Test")
print("=" * 40)

# Test 1: Basic connectivity
print("1. Testing basic connectivity...")
try:
    response = requests.get(f"{BASE_URL}/", timeout=5)
    print(f"   Root: ✅ {response.status_code}")
except:
    print("   Root: ❌ Failed")

# Test 2: Health endpoint
print("\n2. Testing health endpoint...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"   Health: ✅ {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Health: ❌ {e}")

# Test 3: Login
print("\n3. Testing login...")
try:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "john_doe", "password": "password123"},
        timeout=5
    )
    print(f"   Login: ✅ {response.status_code}")
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"   Token received: {token[:30]}...")
except Exception as e:
    print(f"   Login: ❌ {e}")
    print(f"   Response text: {response.text if 'response' in locals() else 'N/A'}")

print("\n" + "=" * 40)
print("Minimal test complete")
