import os
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Import utility functions
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.utils import search_brave, store_search_results, search_vector_db

# Load environment variables
load_dotenv()

# Define models
class CompanyInfo(BaseModel):
    """Information about a company."""
    name: str = Field(..., description="The name of the company")
    industry: str = Field(..., description="The industry the company operates in")
    description: str = Field(..., description="A brief description of the company")
    founded: str = Field(..., description="When the company was founded")
    headquarters: str = Field(..., description="Where the company is headquartered")
    key_products: List[str] = Field(..., description="Key products or services offered by the company")
    competitors: List[str] = Field(..., description="Main competitors of the company")

class FinancialAnalysis(BaseModel):
    """Financial analysis of a company."""
    revenue: str = Field(..., description="Revenue information")
    profit_margin: str = Field(..., description="Profit margin information")
    market_cap: str = Field(..., description="Market capitalization")
    pe_ratio: str = Field(..., description="Price-to-earnings ratio")
    recent_performance: str = Field(..., description="Recent financial performance")
    growth_prospects: str = Field(..., description="Growth prospects")

class MarketAnalysis(BaseModel):
    """Market analysis of a company."""
    market_position: str = Field(..., description="Position in the market")
    market_share: str = Field(..., description="Estimated market share")
    target_audience: str = Field(..., description="Target audience or customer base")
    market_trends: str = Field(..., description="Relevant market trends")
    opportunities: List[str] = Field(..., description="Market opportunities")
    threats: List[str] = Field(..., description="Market threats")

class StrengthsWeaknesses(BaseModel):
    """Strengths and weaknesses of a company."""
    strengths: List[str] = Field(..., description="Company strengths")
    weaknesses: List[str] = Field(..., description="Company weaknesses")

class CompanyAnalysis(BaseModel):
    """Complete analysis of a company."""
    company_info: CompanyInfo = Field(..., description="Basic information about the company")
    financial_analysis: FinancialAnalysis = Field(..., description="Financial analysis of the company")
    market_analysis: MarketAnalysis = Field(..., description="Market analysis of the company")
    strengths_weaknesses: StrengthsWeaknesses = Field(..., description="Strengths and weaknesses of the company")
    summary: str = Field(..., description="Executive summary of the analysis")
    sources: List[str] = Field(..., description="Sources used for the analysis")

class CompanyAnalyzer:
    """Agent for analyzing companies using Brave Search."""
    
    def __init__(self):
        """Initialize the CompanyAnalyzer agent."""
        self.llm = ChatOpenAI(
            model_name=os.getenv("LLM_MODEL", "gpt-4o-mini"),
            temperature=0.2,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Define the analysis prompt
        self.analysis_prompt = PromptTemplate(
            input_variables=["company_name", "search_results"],
            template="""
            You are an expert business analyst tasked with providing a comprehensive analysis of {company_name}.
            
            Use the following search results to inform your analysis:
            
            {search_results}
            
            Provide a detailed analysis covering:
            1. Basic company information (name, industry, description, founding date, headquarters, key products, competitors)
            2. Financial analysis (revenue, profit margin, market cap, P/E ratio, recent performance, growth prospects)
            3. Market analysis (market position, market share, target audience, market trends, opportunities, threats)
            4. Strengths and weaknesses
            5. An executive summary
            6. List of sources used
            
            Your analysis should be data-driven, balanced, and insightful. If certain information is not available in the search results, 
            make reasonable inferences based on available data but indicate when you're making an inference rather than stating a fact.
            """
        )
        
        self.analysis_chain = LLMChain(llm=self.llm, prompt=self.analysis_prompt)
    
    def search_company(self, company_name: str, num_results: int = 15) -> Dict[str, Any]:
        """
        Search for information about a company using Brave Search.
        
        Args:
            company_name: The name of the company to search for
            num_results: Number of search results to retrieve
            
        Returns:
            Dict containing search results
        """
        # Create search queries
        queries = [
            f"{company_name} company information",
            f"{company_name} financial performance",
            f"{company_name} market analysis",
            f"{company_name} competitors",
            f"{company_name} recent news"
        ]
        
        all_results = {}
        
        # Execute searches
        for query in queries:
            results = search_brave(query, count=num_results // len(queries))
            
            # Store results in vector database
            store_search_results(results, company_name)
            
            # Add to combined results
            if "web" in results and "results" in results["web"]:
                if "web" not in all_results:
                    all_results["web"] = {"results": []}
                all_results["web"]["results"].extend(results["web"]["results"])
        
        return all_results
    
    def analyze_company(self, company_name: str) -> CompanyAnalysis:
        """
        Perform a comprehensive analysis of a company.
        
        Args:
            company_name: The name of the company to analyze
            
        Returns:
            CompanyAnalysis object containing the analysis
        """
        # Search for company information
        search_results = self.search_company(company_name)
        
        # Format search results for the prompt
        formatted_results = ""
        if "web" in search_results and "results" in search_results["web"]:
            for i, result in enumerate(search_results["web"]["results"]):
                formatted_results += f"[{i+1}] {result.get('title', 'No title')}\n"
                formatted_results += f"URL: {result.get('url', 'No URL')}\n"
                formatted_results += f"Description: {result.get('description', 'No description')}\n\n"
        
        # Also check vector database for relevant information
        vector_results = search_vector_db(f"{company_name} company analysis")
        for i, result in enumerate(vector_results):
            formatted_results += f"[VDB {i+1}] {result.get('title', 'No title')}\n"
            formatted_results += f"URL: {result.get('url', 'No URL')}\n"
            formatted_results += f"Content: {result.get('content', 'No content')}\n\n"
        
        # Run the analysis chain
        analysis_result = self.analysis_chain.run(
            company_name=company_name,
            search_results=formatted_results
        )
        
        # Parse the result into structured format
        try:
            # The LLM might not return valid JSON, so we'll try to extract structured data
            # but fall back to a more flexible approach if needed
            return self._parse_analysis_result(analysis_result, company_name)
        except Exception as e:
            print(f"Error parsing analysis result: {e}")
            # Fallback to a more flexible approach
            return self._create_fallback_analysis(analysis_result, company_name)
    
    def _parse_analysis_result(self, analysis_result: str, company_name: str) -> CompanyAnalysis:
        """
        Parse the LLM output into a structured CompanyAnalysis object.
        
        Args:
            analysis_result: The raw LLM output
            company_name: The name of the company
            
        Returns:
            CompanyAnalysis object
        """
        # Use the LLM to convert the analysis into a structured format
        structure_prompt = PromptTemplate(
            input_variables=["analysis", "company_name"],
            template="""
            Convert the following company analysis into a structured JSON format:
            
            {analysis}
            
            The JSON should have the following structure:
            {{
                "company_info": {{
                    "name": "{company_name}",
                    "industry": "",
                    "description": "",
                    "founded": "",
                    "headquarters": "",
                    "key_products": [],
                    "competitors": []
                }},
                "financial_analysis": {{
                    "revenue": "",
                    "profit_margin": "",
                    "market_cap": "",
                    "pe_ratio": "",
                    "recent_performance": "",
                    "growth_prospects": ""
                }},
                "market_analysis": {{
                    "market_position": "",
                    "market_share": "",
                    "target_audience": "",
                    "market_trends": "",
                    "opportunities": [],
                    "threats": []
                }},
                "strengths_weaknesses": {{
                    "strengths": [],
                    "weaknesses": []
                }},
                "summary": "",
                "sources": []
            }}
            
            Return only the JSON object, nothing else.
            """
        )
        
        structure_chain = LLMChain(llm=self.llm, prompt=structure_prompt)
        structured_result = structure_chain.run(
            analysis=analysis_result,
            company_name=company_name
        )
        
        # Extract the JSON part
        try:
            # Find JSON object in the response
            json_start = structured_result.find("{")
            json_end = structured_result.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                json_str = structured_result[json_start:json_end]
                data = json.loads(json_str)
                return CompanyAnalysis(**data)
        except:
            pass
        
        # If we couldn't extract JSON, try a more direct approach
        return self._create_fallback_analysis(analysis_result, company_name)
    
    def _create_fallback_analysis(self, analysis_result: str, company_name: str) -> CompanyAnalysis:
        """
        Create a fallback analysis when structured parsing fails.
        
        Args:
            analysis_result: The raw LLM output
            company_name: The name of the company
            
        Returns:
            CompanyAnalysis object
        """
        # Create a minimal structure
        return CompanyAnalysis(
            company_info=CompanyInfo(
                name=company_name,
                industry="Information not structured",
                description="See summary for details",
                founded="Information not structured",
                headquarters="Information not structured",
                key_products=["Information not structured"],
                competitors=["Information not structured"]
            ),
            financial_analysis=FinancialAnalysis(
                revenue="Information not structured",
                profit_margin="Information not structured",
                market_cap="Information not structured",
                pe_ratio="Information not structured",
                recent_performance="Information not structured",
                growth_prospects="Information not structured"
            ),
            market_analysis=MarketAnalysis(
                market_position="Information not structured",
                market_share="Information not structured",
                target_audience="Information not structured",
                market_trends="Information not structured",
                opportunities=["Information not structured"],
                threats=["Information not structured"]
            ),
            strengths_weaknesses=StrengthsWeaknesses(
                strengths=["Information not structured"],
                weaknesses=["Information not structured"]
            ),
            summary=analysis_result,
            sources=["Information not structured"]
        ) 