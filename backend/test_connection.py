#!/usr/bin/env python
"""
Test script to verify Django API endpoints are working
"""
import requests
import json

def test_api_endpoints():
    base_url = "http://localhost:8000/api"
    
    print("Testing Django API endpoints...")
    print("=" * 50)
    
    # Test endpoints
    endpoints = [
        "/customers/customers/",
        "/events/special-dates/",
        "/offers/offers/",
        "/spin-wheel/prizes/"
    ]
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=5)
            print(f"✅ {endpoint}")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Response: {len(data)} items")
            else:
                print(f"   Error: {response.text}")
            print()
        except requests.exceptions.ConnectionError:
            print(f"❌ {endpoint}")
            print("   Error: Connection refused - Django server not running")
            print()
        except Exception as e:
            print(f"❌ {endpoint}")
            print(f"   Error: {str(e)}")
            print()
    
    print("=" * 50)
    print("API testing completed!")

if __name__ == "__main__":
    test_api_endpoints()
