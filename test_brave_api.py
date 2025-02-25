#!/usr/bin/env python3
import os
import sys
import json
import requests
from dotenv import load_dotenv

def test_brave_api():
    """Test the Brave Search API with the provided API key."""
    print("=== Brave Search API Test ===")
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("BRAVE_SEARCH_API_KEY")
    if not api_key:
        api_key = input("Enter your Brave Search API key: ").strip()
    
    if not api_key:
        print("Error: No API key provided.")
        return
    
    # API endpoint
    url = "https://api.search.brave.com/res/v1/web/search"
    
    # Headers
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key
    }
    
    # Query parameters
    params = {
        "q": "Brave Search API test",
        "count": 3
    }
    
    print("\nSending test request to Brave Search API...")
    
    try:
        # Make the request
        response = requests.get(url, headers=headers, params=params)
        
        # Check response
        if response.status_code == 200:
            data = response.json()
            
            print("\n✅ API test successful!")
            print(f"Status code: {response.status_code}")
            
            # Print some results
            if "web" in data and "results" in data["web"]:
                print("\nSample results:")
                for i, result in enumerate(data["web"]["results"][:3]):
                    print(f"\n[{i+1}] {result.get('title', 'No title')}")
                    print(f"URL: {result.get('url', 'No URL')}")
                    print(f"Description: {result.get('description', 'No description')[:100]}...")
            
            # Ask if user wants to see full response
            show_full = input("\nShow full API response? (y/n): ").lower()
            if show_full == "y":
                print("\nFull API response:")
                print(json.dumps(data, indent=2))
        else:
            print(f"\n❌ API test failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    test_brave_api() 