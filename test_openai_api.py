#!/usr/bin/env python3
import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI

def test_openai_api():
    """Test the OpenAI API with the provided API key."""
    print("=== OpenAI API Test ===")
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Enter your OpenAI API key: ").strip()
    
    if not api_key:
        print("Error: No API key provided.")
        return
    
    # Get model name
    model = os.getenv("LLM_MODEL", "gpt-4o")
    
    print(f"\nTesting OpenAI API with model: {model}")
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Make a simple request
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello! Can you give me a brief response to test the API connection?"}
            ],
            max_tokens=100
        )
        
        # Check response
        if response and hasattr(response, 'choices') and len(response.choices) > 0:
            print("\n✅ API test successful!")
            
            # Print response
            message = response.choices[0].message.content
            print("\nResponse from OpenAI:")
            print(f"\"{message}\"")
            
            # Print model and token usage
            print(f"\nModel used: {response.model}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Completion tokens: {response.usage.completion_tokens}")
            print(f"Total tokens: {response.usage.total_tokens}")
            
            # Ask if user wants to see full response
            show_full = input("\nShow full API response? (y/n): ").lower()
            if show_full == "y":
                print("\nFull API response:")
                print(json.dumps(response.model_dump(), indent=2))
        else:
            print("\n❌ API test failed: Unexpected response format")
            print(f"Response: {response}")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        
        # Provide more helpful error messages for common issues
        if "Incorrect API key" in str(e) or "Invalid API key" in str(e):
            print("\nTip: Make sure your API key is correct and has not expired.")
        elif "Rate limit" in str(e):
            print("\nTip: You've hit a rate limit. Try again later or check your usage tier.")
        elif "not_found" in str(e) or "The model" in str(e):
            print(f"\nTip: The model '{model}' might not be available to your account.")
            print("Try using a different model like 'gpt-3.5-turbo' in your .env file.")

if __name__ == "__main__":
    test_openai_api() 