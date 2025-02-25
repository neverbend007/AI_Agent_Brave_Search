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

class ArchonMCPRealIntegration:
    """Real integration with Archon MCP using the actual MCP functions."""
    
    def __init__(self):
        """Initialize the Archon MCP integration."""
        self.thread_id = None
    
    async def create_thread(self) -> str:
        """
        Create a new Archon thread using the MCP API.
        
        Returns:
            str: Thread ID
        """
        try:
            # This would be replaced with the actual MCP function call:
            # mcp_create_thread({"random_string": "dummy"})
            
            # For demonstration, we'll simulate the response
            response = {"thread_id": "archon-" + os.urandom(4).hex()}
            
            self.thread_id = response["thread_id"]
            return self.thread_id
        except Exception as e:
            print(f"Error creating Archon thread: {e}")
            return "error-thread-id"
    
    async def run_agent(self, user_input: str) -> str:
        """
        Run the Archon agent with user input using the MCP API.
        
        Args:
            user_input: The user's input message
            
        Returns:
            str: The agent's response
        """
        if not self.thread_id:
            self.thread_id = await self.create_thread()
        
        try:
            # This would be replaced with the actual MCP function call:
            # mcp_run_agent({"thread_id": self.thread_id, "user_input": prompt})
            
            # Prepare the prompt for Archon
            prompt = f"""
            I need an agent that can search the web using Brave Search API and perform in-depth analysis on a company.
            
            The agent should:
            1. Use the Brave Search API to gather information about a company
            2. Store the search results in a vector database
            3. Analyze the company's financial performance, market position, and business strategy
            4. Provide a comprehensive report with strengths, weaknesses, opportunities, and threats
            
            The agent should be able to handle this user query:
            "{user_input}"
            
            Please provide the complete code for this agent.
            """
            
            # For demonstration, we'll use our CompanyAnalyzer directly
            analyzer = CompanyAnalyzer()
            company_name = self._extract_company_name(user_input)
            
            if not company_name:
                return "Please specify a company name for analysis."
            
            try:
                # Analyze the company
                analysis = analyzer.analyze_company(company_name)
                
                # Format the analysis as a response
                return self._format_analysis_response(analysis)
            except Exception as e:
                return f"Error analyzing {company_name}: {str(e)}"
            
        except Exception as e:
            print(f"Error running Archon agent: {e}")
            return f"Error: {str(e)}"
    
    def _extract_company_name(self, user_input: str) -> Optional[str]:
        """
        Extract company name from user input.
        
        Args:
            user_input: The user's input message
            
        Returns:
            Extracted company name or None
        """
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
    
    def _format_analysis_response(self, analysis) -> str:
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

# Example of how to use the MCP functions in a real implementation
async def real_mcp_integration():
    """
    Example of how to use the MCP functions in a real implementation.
    This would be used in the actual MCP server.
    """
    # Create a thread
    # thread_response = mcp_create_thread({"random_string": "dummy"})
    # thread_id = thread_response["thread_id"]
    
    # Simulate thread_id for demonstration
    thread_id = "archon-" + os.urandom(4).hex()
    
    # User input
    user_input = "Analyze Microsoft and provide insights on their financial performance"
    
    # Prepare the prompt for Archon
    prompt = f"""
    I need an agent that can search the web using Brave Search API and perform in-depth analysis on a company.
    
    The agent should:
    1. Use the Brave Search API to gather information about a company
    2. Store the search results in a vector database
    3. Analyze the company's financial performance, market position, and business strategy
    4. Provide a comprehensive report with strengths, weaknesses, opportunities, and threats
    
    The agent should be able to handle this user query:
    "{user_input}"
    
    Please provide the complete code for this agent.
    """
    
    # Run the agent
    # agent_response = mcp_run_agent({"thread_id": thread_id, "user_input": prompt})
    # response = agent_response["response"]
    
    # Simulate response for demonstration
    response = f"Archon would generate code for an agent that analyzes {user_input}"
    
    return response

async def main():
    """Main function to demonstrate Archon MCP integration."""
    integration = ArchonMCPRealIntegration()
    
    print("Creating Archon thread...")
    thread_id = await integration.create_thread()
    print(f"Thread ID: {thread_id}")
    
    # Example user input
    user_input = "Analyze Microsoft and provide insights on their financial performance"
    
    print(f"\nUser Input: {user_input}")
    response = await integration.run_agent(user_input)
    
    print("\nArchon Response:")
    print(response)
    
    # Example of real MCP integration
    print("\nExample of real MCP integration:")
    real_response = await real_mcp_integration()
    print(real_response)

if __name__ == "__main__":
    asyncio.run(main()) 