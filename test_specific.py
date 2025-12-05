"""
Run specific test categories
"""
import requests

BASE_URL = "http://localhost:8000"

def test_authentication_only():
    """Test only authentication endpoints"""
    print("Testing authentication...")
    
    # Login
    response = requests.post(f"{BASE_URL}/auth/login", 
                            json={"username": "john_doe", "password": "password123"})
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Login successful: {token[:30]}...")
        
        # Test protected endpoint
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            print(f"✅ Protected endpoint accessed: {response.json()['username']}")
        else:
            print(f"❌ Protected endpoint failed: {response.status_code}")
    else:
        print(f"❌ Login failed: {response.status_code}")

def test_products_only():
    """Test only product endpoints"""
    print("Testing products...")
    
    # Get categories
    response = requests.get(f"{BASE_URL}/products/categories")
    if response.status_code == 200:
        cats = response.json()["categories"]
        print(f"✅ Categories: {', '.join(cats)}")
    
    # Get products with filters
    response = requests.get(f"{BASE_URL}/products/?category=electronics&limit=2")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Products: {len(data['items'])} items, total: {data['total']}")
        
        for product in data["items"]:
            print(f"   • {product['name']} - ${product['price']}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "auth":
            test_authentication_only()
        elif sys.argv[1] == "products":
            test_products_only()
        else:
            print("Usage: python test_specific.py [auth|products]")
    else:
        test_authentication_only()
        print()
        test_products_only()
