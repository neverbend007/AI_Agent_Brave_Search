import os
import json
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import openai
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Brave Search API configuration
BRAVE_SEARCH_API_KEY = os.getenv("BRAVE_SEARCH_API_KEY")
BRAVE_SEARCH_API_URL = "https://api.search.brave.com/res/v1/web/search"

def search_brave(query: str, count: int = 10) -> Dict[str, Any]:
    """
    Search the web using Brave Search API.
    
    Args:
        query: The search query
        count: Number of results to return
        
    Returns:
        Dict containing search results
    """
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_SEARCH_API_KEY
    }
    
    params = {
        "q": query,
        "count": count
    }
    
    response = requests.get(BRAVE_SEARCH_API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error searching Brave: {response.status_code} - {response.text}")

def get_embedding(text: str) -> List[float]:
    """
    Get embedding for a text using OpenAI's embedding model.
    
    Args:
        text: The text to embed
        
    Returns:
        List of floats representing the embedding
    """
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def store_search_results(results: Dict[str, Any], company_name: Optional[str] = None) -> None:
    """
    Store search results in Supabase.
    
    Args:
        results: The search results from Brave Search API
        company_name: Optional company name for categorization
    """
    if "web" not in results or "results" not in results["web"]:
        return
    
    for i, result in enumerate(results["web"]["results"]):
        # Extract relevant information
        url = result.get("url", "")
        title = result.get("title", "")
        description = result.get("description", "")
        
        # Create metadata
        metadata = {
            "position": i,
            "source": "brave_search",
            "query_time": results.get("query", {}).get("timestamp", "")
        }
        
        # Get embedding for the content
        content = f"{title}\n{description}"
        embedding = get_embedding(content)
        
        # Store in Supabase
        supabase.table("site_pages").insert({
            "url": url,
            "chunk_number": i,
            "title": title,
            "summary": description[:200] if description else "",
            "content": content,
            "company_name": company_name,
            "metadata": metadata,
            "embedding": embedding
        }).execute()

def search_vector_db(query: str, threshold: float = 0.7, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Search the vector database for similar content.
    
    Args:
        query: The search query
        threshold: Similarity threshold
        limit: Maximum number of results
        
    Returns:
        List of matching documents
    """
    query_embedding = get_embedding(query)
    
    response = supabase.rpc(
        "match_site_pages",
        {
            "query_embedding": query_embedding,
            "match_threshold": threshold,
            "match_count": limit
        }
    ).execute()
    
    if hasattr(response, "data"):
        return response.data
    return [] 