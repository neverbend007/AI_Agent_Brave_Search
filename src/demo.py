import os
import sys
import asyncio
from dotenv import load_dotenv

# Add the parent directory to the path so we can import from agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.company_analyzer import CompanyAnalyzer

# Load environment variables
load_dotenv()

async def demo_company_analyzer():
    """Demonstrate the CompanyAnalyzer agent."""
    print("=== Company Analyzer Demo ===")
    print("This demo will analyze a company using the Brave Search API.")
    
    # Initialize the analyzer
    analyzer = CompanyAnalyzer()
    
    # Get company name from user
    company_name = input("\nEnter a company name to analyze: ")
    
    print(f"\nAnalyzing {company_name}...")
    print("This may take a minute or two as we search for information and analyze the company.")
    
    try:
        # Analyze the company
        analysis = analyzer.analyze_company(company_name)
        
        # Print the analysis
        print("\n" + "=" * 80)
        print(f"Analysis of {company_name}")
        print("=" * 80)
        
        print("\n--- Company Information ---")
        print(f"Industry: {analysis.company_info.industry}")
        print(f"Description: {analysis.company_info.description}")
        print(f"Founded: {analysis.company_info.founded}")
        print(f"Headquarters: {analysis.company_info.headquarters}")
        
        print("\nKey Products/Services:")
        for product in analysis.company_info.key_products:
            print(f"- {product}")
        
        print("\nMain Competitors:")
        for competitor in analysis.company_info.competitors:
            print(f"- {competitor}")
        
        print("\n--- Financial Analysis ---")
        print(f"Revenue: {analysis.financial_analysis.revenue}")
        print(f"Profit Margin: {analysis.financial_analysis.profit_margin}")
        print(f"Market Cap: {analysis.financial_analysis.market_cap}")
        print(f"P/E Ratio: {analysis.financial_analysis.pe_ratio}")
        print(f"Recent Performance: {analysis.financial_analysis.recent_performance}")
        print(f"Growth Prospects: {analysis.financial_analysis.growth_prospects}")
        
        print("\n--- Market Analysis ---")
        print(f"Market Position: {analysis.market_analysis.market_position}")
        print(f"Market Share: {analysis.market_analysis.market_share}")
        print(f"Target Audience: {analysis.market_analysis.target_audience}")
        print(f"Market Trends: {analysis.market_analysis.market_trends}")
        
        print("\nOpportunities:")
        for opportunity in analysis.market_analysis.opportunities:
            print(f"- {opportunity}")
        
        print("\nThreats:")
        for threat in analysis.market_analysis.threats:
            print(f"- {threat}")
        
        print("\n--- Strengths & Weaknesses ---")
        print("Strengths:")
        for strength in analysis.strengths_weaknesses.strengths:
            print(f"- {strength}")
        
        print("\nWeaknesses:")
        for weakness in analysis.strengths_weaknesses.weaknesses:
            print(f"- {weakness}")
        
        print("\n--- Executive Summary ---")
        print(analysis.summary)
        
        print("\n--- Sources ---")
        for source in analysis.sources:
            print(f"- {source}")
        
    except Exception as e:
        print(f"Error analyzing {company_name}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(demo_company_analyzer()) 