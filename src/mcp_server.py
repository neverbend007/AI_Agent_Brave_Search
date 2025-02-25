import os
import sys
import json
import uuid
import asyncio
from typing import Dict, Any, Optional

# Add the parent directory to the path so we can import from agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.company_analyzer import CompanyAnalyzer

# Dictionary to store active threads
threads: Dict[str, Any] = {}

async def handle_create_thread(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new conversation thread.
    
    Args:
        params: Parameters for thread creation
        
    Returns:
        Dict containing the thread ID
    """
    thread_id = str(uuid.uuid4())
    threads[thread_id] = {
        "analyzer": CompanyAnalyzer(),
        "history": []
    }
    return {"thread_id": thread_id}

async def handle_run_agent(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run the company analyzer agent.
    
    Args:
        params: Parameters including thread_id and user_input
        
    Returns:
        Dict containing the agent's response
    """
    thread_id = params.get("thread_id")
    user_input = params.get("user_input", "")
    
    if not thread_id or thread_id not in threads:
        return {"error": "Invalid thread ID. Please create a thread first."}
    
    thread = threads[thread_id]
    analyzer = thread["analyzer"]
    
    # Add user input to history
    thread["history"].append({"role": "user", "content": user_input})
    
    # Process the user input
    response = await process_user_input(user_input, analyzer)
    
    # Add response to history
    thread["history"].append({"role": "assistant", "content": response})
    
    return {"response": response}

async def process_user_input(user_input: str, analyzer: CompanyAnalyzer) -> str:
    """
    Process user input and generate a response.
    
    Args:
        user_input: The user's input message
        analyzer: The CompanyAnalyzer instance
        
    Returns:
        String response from the agent
    """
    # Extract company name from user input
    company_name = extract_company_name(user_input)
    
    if not company_name:
        return (
            "I couldn't identify a company name in your request. "
            "Please specify a company name for analysis, for example: "
            "'Analyze Tesla' or 'Tell me about Microsoft'."
        )
    
    try:
        # Analyze the company
        analysis = analyzer.analyze_company(company_name)
        
        # Format the analysis as a response
        return format_analysis_response(analysis)
    except Exception as e:
        return f"I encountered an error while analyzing {company_name}: {str(e)}"

def extract_company_name(user_input: str) -> Optional[str]:
    """
    Extract company name from user input.
    
    Args:
        user_input: The user's input message
        
    Returns:
        Extracted company name or None
    """
    # This is a simple extraction method
    # In a production system, you might use NER or a more sophisticated approach
    
    # Common phrases that might precede a company name
    prefixes = [
        "analyze", "research", "tell me about", "information on", 
        "what do you know about", "can you analyze", "look up",
        "search for", "find information about", "company analysis for"
    ]
    
    lower_input = user_input.lower()
    
    for prefix in prefixes:
        if prefix in lower_input:
            # Extract text after the prefix
            start_idx = lower_input.find(prefix) + len(prefix)
            company_name = user_input[start_idx:].strip()
            
            # Remove common words that might follow the company name
            for suffix in ["company", "corporation", "inc", "ltd", "and", "for", "of"]:
                if company_name.lower().endswith(f" {suffix}"):
                    company_name = company_name[:-len(suffix)-1].strip()
            
            return company_name
    
    # If no prefix is found, try to identify a company name directly
    # This is a very simple approach and would need to be improved
    words = user_input.split()
    for i, word in enumerate(words):
        if word[0].isupper() and i < len(words) - 1 and words[i+1][0].isupper():
            # Two consecutive capitalized words might be a company name
            return f"{word} {words[i+1]}"
    
    # If all else fails, just return the first capitalized word
    for word in words:
        if word[0].isupper():
            return word
    
    return None

def format_analysis_response(analysis) -> str:
    """
    Format the company analysis as a readable response.
    
    Args:
        analysis: CompanyAnalysis object
        
    Returns:
        Formatted string response
    """
    company_info = analysis.company_info
    financial = analysis.financial_analysis
    market = analysis.market_analysis
    strengths_weaknesses = analysis.strengths_weaknesses
    
    response = f"# Analysis of {company_info.name}\n\n"
    
    response += "## Company Information\n"
    response += f"- **Industry**: {company_info.industry}\n"
    response += f"- **Description**: {company_info.description}\n"
    response += f"- **Founded**: {company_info.founded}\n"
    response += f"- **Headquarters**: {company_info.headquarters}\n"
    response += "- **Key Products/Services**:\n"
    for product in company_info.key_products:
        response += f"  - {product}\n"
    response += "- **Main Competitors**:\n"
    for competitor in company_info.competitors:
        response += f"  - {competitor}\n"
    
    response += "\n## Financial Analysis\n"
    response += f"- **Revenue**: {financial.revenue}\n"
    response += f"- **Profit Margin**: {financial.profit_margin}\n"
    response += f"- **Market Cap**: {financial.market_cap}\n"
    response += f"- **P/E Ratio**: {financial.pe_ratio}\n"
    response += f"- **Recent Performance**: {financial.recent_performance}\n"
    response += f"- **Growth Prospects**: {financial.growth_prospects}\n"
    
    response += "\n## Market Analysis\n"
    response += f"- **Market Position**: {market.market_position}\n"
    response += f"- **Market Share**: {market.market_share}\n"
    response += f"- **Target Audience**: {market.target_audience}\n"
    response += f"- **Market Trends**: {market.market_trends}\n"
    response += "- **Opportunities**:\n"
    for opportunity in market.opportunities:
        response += f"  - {opportunity}\n"
    response += "- **Threats**:\n"
    for threat in market.threats:
        response += f"  - {threat}\n"
    
    response += "\n## Strengths & Weaknesses\n"
    response += "### Strengths\n"
    for strength in strengths_weaknesses.strengths:
        response += f"- {strength}\n"
    response += "\n### Weaknesses\n"
    for weakness in strengths_weaknesses.weaknesses:
        response += f"- {weakness}\n"
    
    response += f"\n## Executive Summary\n{analysis.summary}\n"
    
    response += "\n## Sources\n"
    for source in analysis.sources:
        response += f"- {source}\n"
    
    return response

async def handle_mcp_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle MCP messages.
    
    Args:
        message: The MCP message
        
    Returns:
        Response to the MCP message
    """
    method = message.get("method")
    params = message.get("params", {})
    
    if method == "mcp_create_thread":
        return await handle_create_thread(params)
    elif method == "mcp_run_agent":
        return await handle_run_agent(params)
    else:
        return {"error": f"Unknown method: {method}"}

async def main():
    """Main function to handle stdin/stdout communication."""
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
                
            message = json.loads(line)
            response = await handle_mcp_message(message)
            
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main()) 