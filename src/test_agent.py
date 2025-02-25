import os
import sys
import asyncio
from dotenv import load_dotenv

# Add the parent directory to the path so we can import from agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.company_analyzer import CompanyAnalyzer

# Load environment variables
load_dotenv()

async def test_company_analyzer():
    """Test the CompanyAnalyzer agent."""
    print("Initializing CompanyAnalyzer...")
    analyzer = CompanyAnalyzer()
    
    # Test company name
    company_name = "Microsoft"
    print(f"\nAnalyzing {company_name}...")
    
    try:
        # Analyze the company
        analysis = analyzer.analyze_company(company_name)
        
        # Print basic information
        print(f"\n=== {company_name} Analysis ===")
        print(f"Industry: {analysis.company_info.industry}")
        print(f"Founded: {analysis.company_info.founded}")
        print(f"Headquarters: {analysis.company_info.headquarters}")
        
        print("\nKey Products:")
        for product in analysis.company_info.key_products[:3]:  # Show first 3 products
            print(f"- {product}")
        
        print("\nFinancial Highlights:")
        print(f"Revenue: {analysis.financial_analysis.revenue}")
        print(f"Market Cap: {analysis.financial_analysis.market_cap}")
        
        print("\nStrengths:")
        for strength in analysis.strengths_weaknesses.strengths[:3]:  # Show first 3 strengths
            print(f"- {strength}")
        
        print("\nSummary:")
        print(analysis.summary[:200] + "..." if len(analysis.summary) > 200 else analysis.summary)
        
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_company_analyzer()) 