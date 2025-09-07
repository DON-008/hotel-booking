#!/usr/bin/env python
"""
Simple test script to verify Django API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoints():
    """Test basic API endpoints"""
    
    print("Testing Django API endpoints...")
    
    # Test customer endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/customers/customers/")
        print(f"✅ Customers endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {len(response.json())} customers")
    except Exception as e:
        print(f"❌ Customers endpoint failed: {e}")
    
    # Test events endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/events/special-dates/")
        print(f"✅ Special dates endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {len(response.json())} special dates")
    except Exception as e:
        print(f"❌ Special dates endpoint failed: {e}")
    
    # Test offers endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/offers/offers/")
        print(f"✅ Offers endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {len(response.json())} offers")
    except Exception as e:
        print(f"❌ Offers endpoint failed: {e}")
    
    # Test spin wheel endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/spin-wheel/prizes/")
        print(f"✅ Prizes endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {len(response.json())} prizes")
    except Exception as e:
        print(f"❌ Prizes endpoint failed: {e}")
    
    print("\nAPI testing completed!")

if __name__ == "__main__":
    test_endpoints()
