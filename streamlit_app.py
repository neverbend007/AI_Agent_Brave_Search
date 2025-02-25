import os
import sys
import asyncio
import streamlit as st
from dotenv import load_dotenv

# Add the src directory to the path so we can import from agent
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
from agent.company_analyzer import CompanyAnalyzer

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Company Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for the analyzer
if "analyzer" not in st.session_state:
    st.session_state.analyzer = CompanyAnalyzer()
    st.session_state.analysis_complete = False
    st.session_state.analysis_result = None

# Title and description
st.title("📊 Company Analyzer")
st.markdown("""
This app uses the Brave Search API to gather information about companies and provides a comprehensive analysis
including financial performance, market position, and business strategy.
""")

# Sidebar for API keys
with st.sidebar:
    st.header("API Configuration")
    
    # OpenAI API Key
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        help="Enter your OpenAI API key to use the LLM for analysis."
    )
    
    # Brave Search API Key
    brave_api_key = st.text_input(
        "Brave Search API Key",
        type="password",
        value=os.getenv("BRAVE_SEARCH_API_KEY", ""),
        help="Enter your Brave Search API key to search for company information."
    )
    
    # Update environment variables
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
    
    if brave_api_key:
        os.environ["BRAVE_SEARCH_API_KEY"] = brave_api_key
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This app uses:
    - Brave Search API for web search
    - OpenAI for analysis
    - Streamlit for the interface
    """)

# Main form for company analysis
with st.form("analysis_form"):
    st.subheader("Enter Company Details")
    
    # Company name input
    company_name = st.text_input(
        "Company Name",
        placeholder="e.g., Microsoft, Apple, Tesla",
        help="Enter the name of the company you want to analyze."
    )
    
    # Number of search results
    num_results = st.slider(
        "Number of Search Results",
        min_value=5,
        max_value=30,
        value=15,
        step=5,
        help="Number of search results to retrieve for analysis."
    )
    
    # Submit button
    submitted = st.form_submit_button("Analyze Company")

# Process form submission
if submitted:
    if not company_name:
        st.error("Please enter a company name.")
    elif not openai_api_key.startswith("sk-"):
        st.error("Please enter a valid OpenAI API key.")
    elif not brave_api_key:
        st.error("Please enter a valid Brave Search API key.")
    else:
        # Show progress
        with st.spinner(f"Analyzing {company_name}... This may take a minute or two."):
            try:
                # Create a new analyzer with the updated API keys
                analyzer = CompanyAnalyzer()
                
                # Analyze the company
                analysis = analyzer.search_company(company_name, num_results=num_results)
                
                # Format search results for the prompt
                formatted_results = ""
                if "web" in analysis and "results" in analysis["web"]:
                    for i, result in enumerate(analysis["web"]["results"]):
                        formatted_results += f"[{i+1}] {result.get('title', 'No title')}\n"
                        formatted_results += f"URL: {result.get('url', 'No URL')}\n"
                        formatted_results += f"Description: {result.get('description', 'No description')}\n\n"
                
                # Run the analysis
                analysis_result = analyzer.analyze_company(company_name)
                
                # Store the result in session state
                st.session_state.analysis_result = analysis_result
                st.session_state.analysis_complete = True
                
                # Show success message
                st.success(f"Analysis of {company_name} completed successfully!")
            
            except Exception as e:
                st.error(f"Error analyzing {company_name}: {str(e)}")

# Display analysis results if available
if st.session_state.analysis_complete and st.session_state.analysis_result:
    analysis = st.session_state.analysis_result
    
    # Create tabs for different sections of the analysis
    tabs = st.tabs([
        "Company Info", 
        "Financial Analysis", 
        "Market Analysis", 
        "SWOT Analysis",
        "Executive Summary",
        "Sources"
    ])
    
    # Company Info tab
    with tabs[0]:
        st.header(f"{analysis.company_info.name}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Industry")
            st.write(analysis.company_info.industry)
            
            st.subheader("Founded")
            st.write(analysis.company_info.founded)
            
            st.subheader("Headquarters")
            st.write(analysis.company_info.headquarters)
        
        with col2:
            st.subheader("Description")
            st.write(analysis.company_info.description)
        
        st.subheader("Key Products/Services")
        for product in analysis.company_info.key_products:
            st.markdown(f"- {product}")
        
        st.subheader("Main Competitors")
        for competitor in analysis.company_info.competitors:
            st.markdown(f"- {competitor}")
    
    # Financial Analysis tab
    with tabs[1]:
        st.header("Financial Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Revenue")
            st.write(analysis.financial_analysis.revenue)
            
            st.subheader("Profit Margin")
            st.write(analysis.financial_analysis.profit_margin)
            
            st.subheader("Market Cap")
            st.write(analysis.financial_analysis.market_cap)
        
        with col2:
            st.subheader("P/E Ratio")
            st.write(analysis.financial_analysis.pe_ratio)
            
            st.subheader("Recent Performance")
            st.write(analysis.financial_analysis.recent_performance)
            
            st.subheader("Growth Prospects")
            st.write(analysis.financial_analysis.growth_prospects)
    
    # Market Analysis tab
    with tabs[2]:
        st.header("Market Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Market Position")
            st.write(analysis.market_analysis.market_position)
            
            st.subheader("Market Share")
            st.write(analysis.market_analysis.market_share)
        
        with col2:
            st.subheader("Target Audience")
            st.write(analysis.market_analysis.target_audience)
            
            st.subheader("Market Trends")
            st.write(analysis.market_analysis.market_trends)
        
        st.subheader("Opportunities")
        for opportunity in analysis.market_analysis.opportunities:
            st.markdown(f"- {opportunity}")
        
        st.subheader("Threats")
        for threat in analysis.market_analysis.threats:
            st.markdown(f"- {threat}")
    
    # SWOT Analysis tab
    with tabs[3]:
        st.header("Strengths & Weaknesses")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Strengths")
            for strength in analysis.strengths_weaknesses.strengths:
                st.markdown(f"- {strength}")
        
        with col2:
            st.subheader("Weaknesses")
            for weakness in analysis.strengths_weaknesses.weaknesses:
                st.markdown(f"- {weakness}")
    
    # Executive Summary tab
    with tabs[4]:
        st.header("Executive Summary")
        st.write(analysis.summary)
    
    # Sources tab
    with tabs[5]:
        st.header("Sources")
        for source in analysis.sources:
            st.markdown(f"- {source}")

# Footer
st.markdown("---")
st.markdown("Powered by Brave Search API and OpenAI") 