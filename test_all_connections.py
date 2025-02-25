#!/usr/bin/env python3
import os
import sys
import json
import requests
import importlib.util
from dotenv import load_dotenv

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 50)
    print(f" {title} ".center(50, "="))
    print("=" * 50 + "\n")

def check_module(module_name):
    """Check if a module is installed."""
    return importlib.util.find_spec(module_name) is not None

def main():
    """Run all connection tests."""
    print_header("Company Analyzer Connection Tests")
    
    # Load environment variables
    load_dotenv()
    
    # Check for required modules
    required_modules = {
        "openai": "OpenAI API",
        "supabase": "Supabase",
        "requests": "Brave Search API",
        "streamlit": "Streamlit App"
    }
    
    print("Checking required modules:")
    all_modules_installed = True
    
    for module, description in required_modules.items():
        if check_module(module):
            print(f"✅ {description} module installed")
        else:
            print(f"❌ {description} module NOT installed")
            all_modules_installed = False
    
    if not all_modules_installed:
        print("\n⚠️ Some required modules are missing. Please run:")
        print("pip install -r requirements.txt")
        return
    
    # Check for environment variables
    print("\nChecking environment variables:")
    
    env_vars = {
        "OPENAI_API_KEY": "OpenAI API Key",
        "BRAVE_SEARCH_API_KEY": "Brave Search API Key",
        "SUPABASE_URL": "Supabase URL",
        "SUPABASE_KEY": "Supabase Key",
        "LLM_MODEL": "LLM Model (optional, defaults to gpt-4o)"
    }
    
    all_env_vars_set = True
    
    for var, description in env_vars.items():
        if var == "LLM_MODEL" and not os.getenv(var):
            print(f"ℹ️ {description} not set, will use default")
        elif os.getenv(var):
            # Mask the key for security
            value = os.getenv(var)
            masked_value = value[:4] + "*" * (len(value) - 8) + value[-4:] if len(value) > 8 else "****"
            print(f"✅ {description} set: {masked_value}")
        else:
            print(f"❌ {description} NOT set")
            all_env_vars_set = False
    
    if not all_env_vars_set:
        print("\n⚠️ Some required environment variables are missing. Please run:")
        print("python setup_env.py")
        return
    
    # Ask user which tests to run
    print("\nWhich connections would you like to test?")
    print("1. All connections")
    print("2. OpenAI API only")
    print("3. Brave Search API only")
    print("4. Supabase only")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "5":
        print("Exiting...")
        return
    
    # Import and run the selected tests
    if choice in ["1", "2"]:
        print_header("Testing OpenAI API")
        from test_openai_api import test_openai_api
        test_openai_api()
    
    if choice in ["1", "3"]:
        print_header("Testing Brave Search API")
        from test_brave_api import test_brave_api
        test_brave_api()
    
    if choice in ["1", "4"]:
        print_header("Testing Supabase Connection")
        from test_supabase import test_supabase
        test_supabase()
    
    print_header("Test Summary")
    print("All selected tests completed.")
    print("\nIf all tests passed, your environment is ready to use the Company Analyzer!")
    print("If any tests failed, please check the error messages and fix the issues.")
    
    print("\nNext steps:")
    print("1. Run the demo script: python src/demo.py")
    print("2. Start the Streamlit app: streamlit run streamlit_app.py")
    print("3. Run both services together: python run_app.py")

if __name__ == "__main__":
    main() 