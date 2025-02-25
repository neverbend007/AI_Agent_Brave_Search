#!/usr/bin/env python3
import os
import sys
import json
from dotenv import load_dotenv
import supabase
from supabase import create_client, Client

def test_supabase():
    """Test the Supabase connection with the provided credentials."""
    print("=== Supabase Connection Test ===")
    
    # Load environment variables
    load_dotenv()
    
    # Get Supabase credentials
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    # Prompt for credentials if not found in environment
    if not supabase_url:
        supabase_url = input("Enter your Supabase URL: ").strip()
    
    if not supabase_key:
        supabase_key = input("Enter your Supabase API key: ").strip()
    
    if not supabase_url or not supabase_key:
        print("Error: Supabase URL and API key are required.")
        return
    
    print("\nTesting Supabase connection...")
    
    try:
        # Initialize Supabase client
        supabase_client: Client = create_client(supabase_url, supabase_key)
        
        # Test connection by fetching table information
        print("\nChecking for 'site_pages' table...")
        
        # Try to get table info
        response = supabase_client.table('site_pages').select('count(*)', count='exact').execute()
        
        # Check if the table exists
        if hasattr(response, 'data'):
            print("\n✅ Supabase connection successful!")
            
            # Check if the table has records
            count = response.count if hasattr(response, 'count') else 0
            print(f"\nTable 'site_pages' exists with {count} records.")
            
            # Check if vector extension is enabled
            print("\nChecking for vector extension...")
            try:
                # Try a simple vector query to see if the extension is enabled
                test_vector = [0.1] * 1536  # Simple test vector
                vector_query = supabase_client.rpc(
                    'match_page_sections',
                    {'query_embedding': test_vector, 'match_threshold': 0.5, 'match_count': 1}
                ).execute()
                
                if hasattr(vector_query, 'data'):
                    print("✅ Vector extension is enabled and functioning.")
                else:
                    print("❌ Vector extension test failed.")
            except Exception as e:
                print(f"❌ Vector extension test failed: {str(e)}")
                print("\nTip: Make sure you've run the SQL setup script from src/utils/site_pages.sql")
        else:
            print("\n❓ Supabase connection succeeded, but 'site_pages' table not found.")
            print("\nTip: Make sure you've run the SQL setup script from src/utils/site_pages.sql")
    
    except Exception as e:
        print(f"\n❌ Supabase connection failed: {str(e)}")
        
        # Provide more helpful error messages for common issues
        if "Invalid API key" in str(e) or "JWT" in str(e):
            print("\nTip: Check that your Supabase API key is correct.")
            print("You need to use the 'anon' key or 'service_role' key from your Supabase project settings.")
        elif "not found" in str(e) or "does not exist" in str(e):
            print("\nTip: Make sure your Supabase URL is correct and the project is running.")
        elif "Connection" in str(e) or "connect" in str(e).lower():
            print("\nTip: Check your internet connection and verify that the Supabase project is online.")

if __name__ == "__main__":
    test_supabase() 