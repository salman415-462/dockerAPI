"""
E-Commerce API Client Example
Usage: python api_client_example.py [command]
"""
import requests
import json
import sys

BASE_URL = "http://localhost:9000"

class ECommerceClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.token = None
    
    def login(self, username, password):
        """Login and get JWT token"""
        response = requests.post(
            f"{self.base_url}/auth/login",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            print(f"✅ Logged in as {username}")
            return True
        else:
            print(f"❌ Login failed: {response.text}")
            return False
    
    def get_products(self, category=None, min_price=None, max_price=None, limit=10):
        """Get products with optional filters"""
        params = {"limit": limit}
        if category:
            params["category"] = category
        if min_price:
            params["min_price"] = min_price
        if max_price:
            params["max_price"] = max_price
        
        response = requests.get(f"{self.base_url}/products/", params=params)
        return response.json()
    
    def get_categories(self):
        """Get all product categories"""
        response = requests.get(f"{self.base_url}/products/categories")
        return response.json()
    
    def create_cart(self, items):
        """Create a shopping cart (requires authentication)"""
        if not self.token:
            print("❌ Not authenticated. Please login first.")
            return None
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(
            f"{self.base_url}/carts/",
            json={"items": items},
            headers=headers
        )
        return response.json()
    
    def make_request(self, method, endpoint, data=None):
        """Make authenticated request"""
        if not self.token:
            print("❌ Not authenticated")
            return None
        
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.base_url}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        
        return response.json()

def main():
    client = ECommerceClient()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "categories":
            print("📦 Product Categories:")
            categories = client.get_categories()
            for cat in categories["categories"]:
                print(f"  • {cat}")
        
        elif command == "products":
            print("🛍️  Products:")
            products = client.get_products(limit=3)
            for item in products["items"]:
                print(f"  • {item['name']} - ${item['price']} ({item['category']})")
        
        elif command == "login":
            if len(sys.argv) > 3:
                username = sys.argv[2]
                password = sys.argv[3]
                client.login(username, password)
            else:
                print("Usage: python api_client_example.py login [username] [password]")
        
        elif command == "demo":
            print("🚀 Running demo...")
            print("\n1. Getting categories:")
            print(json.dumps(client.get_categories(), indent=2))
            
            print("\n2. Getting electronics products:")
            print(json.dumps(client.get_products(category="electronics", limit=2), indent=2))
            
            print("\n3. Login as customer:")
            client.login("john_doe", "password123")
            
        else:
            print(f"Unknown command: {command}")
    else:
        print("E-Commerce API Client")
        print("\nCommands:")
        print("  categories          - List product categories")
        print("  products            - List products")
        print("  login [user] [pass] - Login to API")
        print("  demo                - Run demo")
        print("\nExample: python api_client_example.py demo")

if __name__ == "__main__":
    main()
