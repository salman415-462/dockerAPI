"""
Simple load test for API
"""
import concurrent.futures
import requests
import time

BASE_URL = "http://localhost:8000"

def test_get_products():
    """Test getting products"""
    try:
        response = requests.get(f"{BASE_URL}/products/?limit=5", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_get_categories():
    """Test getting categories"""
    try:
        response = requests.get(f"{BASE_URL}/products/categories", timeout=5)
        return response.status_code == 200
    except:
        return False

def run_load_test(concurrent_requests=10, duration=10):
    """Run load test for specified duration"""
    print(f"🚀 Starting load test: {concurrent_requests} concurrent requests for {duration} seconds")
    
    end_time = time.time() + duration
    successful = 0
    failed = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        futures = []
        while time.time() < end_time:
            # Submit both types of requests
            futures.append(executor.submit(test_get_products))
            futures.append(executor.submit(test_get_categories))
            time.sleep(0.1)  # Small delay to avoid overwhelming
        
        # Wait for all futures to complete
        concurrent.futures.wait(futures)
        
        # Count results
        for future in futures:
            if future.result():
                successful += 1
            else:
                failed += 1
    
    total = successful + failed
    success_rate = (successful / total * 100) if total > 0 else 0
    
    print(f"\n📊 LOAD TEST RESULTS:")
    print(f"   Total requests: {total}")
    print(f"   Successful: {successful}")
    print(f"   Failed: {failed}")
    print(f"   Success rate: {success_rate:.1f}%")
    
    if success_rate > 95:
        print("   ✅ Excellent! API handles load well.")
    elif success_rate > 80:
        print("   ⚠️  Good, but some requests failed.")
    else:
        print("   ❌ API may have performance issues.")

if __name__ == "__main__":
    print("Load testing the API...")
    run_load_test(concurrent_requests=5, duration=5)  # Light load test
    print("\nFor heavier load testing, adjust the parameters in the script.")
