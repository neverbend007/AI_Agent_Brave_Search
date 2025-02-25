import os
import sys
import json
import asyncio
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory to the path so we can import from agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.company_analyzer import CompanyAnalyzer

async def create_archon_thread():
    """
    Create a new Archon thread.
    
    Returns:
        str: Thread ID
    """
    # This is a placeholder for the actual Archon MCP integration
    # In a real implementation, you would call the Archon MCP API
    return "archon-thread-id"

async def run_archon_agent(thread_id: str, user_input: str) -> str:
    """
    Run the Archon agent with user input.
    
    Args:
        thread_id: The thread ID
        user_input: The user's input message
        
    Returns:
        str: The agent's response
    """
    # This is a placeholder for the actual Archon MCP integration
    # In a real implementation, you would call the Archon MCP API
    
    # For demonstration purposes, we'll use our CompanyAnalyzer directly
    analyzer = CompanyAnalyzer()
    
    # Extract company name from user input (simplified)
    company_name = None
    words = user_input.split()
    for word in words:
        if word[0].isupper():
            company_name = word
            break
    
    if not company_name:
        return "Please specify a company name for analysis."
    
    try:
        # Analyze the company
        analysis = analyzer.analyze_company(company_name)
        
        # Format the analysis as a response
        response = f"# Analysis of {company_name}\n\n"
        response += f"Industry: {analysis.company_info.industry}\n"
        response += f"Description: {analysis.company_info.description}\n"
        response += f"Founded: {analysis.company_info.founded}\n"
        response += f"Headquarters: {analysis.company_info.headquarters}\n"
        
        response += "\nFinancial Highlights:\n"
        response += f"Revenue: {analysis.financial_analysis.revenue}\n"
        response += f"Market Cap: {analysis.financial_analysis.market_cap}\n"
        
        response += "\nStrengths:\n"
        for strength in analysis.strengths_weaknesses.strengths[:3]:
            response += f"- {strength}\n"
        
        response += f"\nSummary: {analysis.summary[:200]}...\n"
        
        return response
    except Exception as e:
        return f"Error analyzing {company_name}: {str(e)}"

async def main():
    """Main function to demonstrate Archon integration."""
    print("Creating Archon thread...")
    thread_id = await create_archon_thread()
    print(f"Thread ID: {thread_id}")
    
    # Example user input
    user_input = "Analyze Microsoft and provide insights on their financial performance"
    
    print(f"\nUser Input: {user_input}")
    response = await run_archon_agent(thread_id, user_input)
    
    print("\nArchon Response:")
    print(response)

if __name__ == "__main__":
    asyncio.run(main()) 