#!/usr/bin/env python3
import os
import sys
import shutil

def setup_env():
    """Set up environment variables for the application."""
    print("=== Company Analyzer Environment Setup ===")
    
    # Check if .env file already exists
    if os.path.exists(".env"):
        overwrite = input(".env file already exists. Overwrite? (y/n): ").lower()
        if overwrite != "y":
            print("Setup cancelled.")
            return
    
    # Get API keys
    openai_api_key = input("Enter your OpenAI API key: ").strip()
    brave_search_api_key = input("Enter your Brave Search API key: ").strip()
    
    # Get Supabase credentials
    supabase_url = input("Enter your Supabase URL: ").strip()
    supabase_service_key = input("Enter your Supabase service key: ").strip()
    
    # Get LLM model (with default)
    llm_model = input("Enter LLM model to use (default: gpt-4o-mini): ").strip()
    if not llm_model:
        llm_model = "gpt-4o-mini"
    
    # Create .env file
    with open(".env", "w") as f:
        f.write(f"# OpenAI API Key for LLM\n")
        f.write(f"OPENAI_API_KEY={openai_api_key}\n\n")
        
        f.write(f"# Brave Search API Key\n")
        f.write(f"BRAVE_SEARCH_API_KEY={brave_search_api_key}\n\n")
        
        f.write(f"# Supabase for vector storage\n")
        f.write(f"SUPABASE_URL={supabase_url}\n")
        f.write(f"SUPABASE_SERVICE_KEY={supabase_service_key}\n\n")
        
        f.write(f"# LLM Model to use\n")
        f.write(f"LLM_MODEL={llm_model}\n")
    
    print("\n.env file created successfully!")
    print("You can now run the application using:")
    print("  - python run_app.py")
    print("  - streamlit run streamlit_app.py")
    print("  - docker-compose up -d")

if __name__ == "__main__":
    setup_env() 