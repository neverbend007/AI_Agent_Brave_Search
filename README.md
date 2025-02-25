# AI Agent for Brave Search

An AI agent that can search the web using Brave Search API and perform in-depth analysis on any company. This agent leverages the power of Brave Search API to gather information and uses advanced LLM capabilities to analyze and synthesize the data.

## Features

- Web search using Brave Search API
- In-depth company analysis
- Retrieval-augmented generation for better context
- Vector database storage with Supabase
- Interactive querying through MCP integration
- Archon MCP integration for agent generation

## Prerequisites

- Python 3.11+
- Brave Search API key
- OpenAI API key
- Supabase account and database
- MCP-compatible AI IDE (like Cursor)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI_Agent_Brave_Search.git
cd AI_Agent_Brave_Search
```

2. Install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables:
   - Option 1: Use the setup script:
     ```bash
     python setup_env.py
     ```
   - Option 2: Manually configure:
     - Rename `.env.example` to `.env`
     - Edit `.env` with your API keys and preferences

4. Set up the database:
   - Execute `src/utils/site_pages.sql` in your Supabase SQL Editor
   - This creates tables and enables vector similarity search

## Testing the Brave Search API

Before using the application, you can verify that your Brave Search API key is working correctly:

```bash
python test_brave_api.py
```

This script will:
1. Use the API key from your `.env` file or prompt you to enter one
2. Send a test query to the Brave Search API
3. Display sample results if successful
4. Provide detailed error information if the request fails

A successful test confirms that your API key is valid and that you can connect to the Brave Search API.

## Testing the OpenAI API

You can also verify that your OpenAI API key is working correctly:

```bash
python test_openai_api.py
```

This script will:
1. Use the API key from your `.env` file or prompt you to enter one
2. Use the model specified in your `.env` file (defaults to gpt-4o)
3. Send a simple test query to the OpenAI API
4. Display the response and token usage information
5. Provide helpful error messages for common issues

A successful test confirms that your OpenAI API key is valid and that you can access the specified model.

## Testing the Supabase Connection

You can verify that your Supabase connection is working correctly:

```bash
python test_supabase.py
```

This script will:
1. Use the credentials from your `.env` file or prompt you to enter them
2. Test the connection to your Supabase instance
3. Check if the required `site_pages` table exists
4. Verify that the vector extension is properly configured
5. Provide helpful error messages for common issues

A successful test confirms that your Supabase setup is correct and ready for use with the application.

## Testing All Connections

For convenience, you can test all connections at once:

```bash
python test_all_connections.py
```

This script will:
1. Check if all required modules are installed
2. Verify that all necessary environment variables are set
3. Allow you to choose which connections to test (OpenAI, Brave Search, Supabase, or all)
4. Run the selected tests and provide a summary of results
5. Suggest next steps based on the test results

This is the recommended way to verify your setup before using the application.

## Usage

### Using the Demo Script

1. Run the demo script:
```bash
python src/demo.py
```

2. Enter a company name when prompted
3. The agent will search for information and provide a comprehensive analysis

### Using with MCP-compatible AI IDE

1. Run the setup script to configure MCP:
```bash
python setup_mcp.py
```

2. Configure your AI IDE to use the MCP server as instructed by the setup script
3. You can now ask your AI IDE to search the web and analyze companies using the agent

### Using with Archon

The project includes integration with Archon MCP for agent generation. To use this feature:

1. Make sure you have Archon MCP set up in your AI IDE
2. Use the following files for Archon integration:
   - `src/archon_mcp_integration.py`: Real integration with Archon MCP
   - `src/real_archon_integration.py`: Example of using Archon MCP functions

Example prompt for Archon:
```
I need an agent that can search the web using Brave Search API and perform in-depth analysis on a company.

The agent should:
1. Use the Brave Search API to gather information about a company
2. Store the search results in a vector database
3. Analyze the company's financial performance, market position, and business strategy
4. Provide a comprehensive report with strengths, weaknesses, opportunities, and threats

Please provide the complete code for this agent.
```

### Example Queries

- "Search for information about Tesla and analyze their financial performance"
- "Find recent news about Microsoft and analyze their market position"
- "Research Amazon's supply chain strategy and provide an analysis"

### Using the Streamlit App

1. Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

2. The app will open in your browser (typically at http://localhost:8501)
3. Enter your API keys in the sidebar
4. Enter a company name and click "Analyze Company"
5. View the comprehensive analysis in the tabbed interface

### Running the Complete Application

To run both the Streamlit app and MCP server together:

```bash
python run_app.py
```

This will:
- Start the Streamlit web interface
- Start the MCP server in the background
- Monitor both services and restart them if they crash
- Provide a single point to stop all services (Ctrl+C)

### Using Docker

You can also run the application using Docker:

1. Build and start the container:
```bash
docker-compose up -d
```

2. Access the Streamlit app at http://localhost:8501

3. Stop the container:
```bash
docker-compose down
```

## Project Structure

- `src/agent/company_analyzer.py`: Main agent for company analysis
- `src/utils/utils.py`: Utility functions for API calls and database operations
- `src/utils/site_pages.sql`: SQL setup for Supabase database
- `src/mcp_server.py`: MCP server for AI IDE integration
- `src/archon_mcp_integration.py`: Integration with Archon MCP
- `src/demo.py`: Demo script for testing the agent
- `setup_mcp.py`: Setup script for MCP configuration
- `setup_env.py`: Script to set up environment variables
- `test_brave_api.py`: Script to test the Brave Search API
- `test_openai_api.py`: Script to test the OpenAI API
- `test_supabase.py`: Script to test the Supabase connection
- `test_all_connections.py`: Script to test all API connections at once
- `streamlit_app.py`: Streamlit web application for interactive company analysis
- `run_app.py`: Script to run both the Streamlit app and MCP server together
- `Dockerfile`: Docker configuration for containerization
- `docker-compose.yml`: Docker Compose configuration for easy deployment

## License

MIT