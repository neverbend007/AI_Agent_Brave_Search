#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from pathlib import Path

def create_venv():
    """Create a virtual environment if it doesn't exist."""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("Virtual environment created.")
    else:
        print("Virtual environment already exists.")

def install_dependencies():
    """Install dependencies from requirements.txt."""
    print("Installing dependencies...")
    
    # Determine the pip executable based on the platform
    pip_cmd = "venv/bin/pip" if os.name != "nt" else r"venv\Scripts\pip"
    
    # Install dependencies
    subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
    print("Dependencies installed.")

def generate_mcp_config():
    """Generate MCP configuration for AI IDEs."""
    # Get the absolute path to the workspace
    workspace_path = os.path.abspath(os.path.dirname(__file__))
    
    # Determine the Python executable path based on the platform
    python_path = os.path.join(workspace_path, "venv/bin/python") if os.name != "nt" else os.path.join(workspace_path, r"venv\Scripts\python.exe")
    
    # MCP server path
    mcp_server_path = os.path.join(workspace_path, "src/mcp_server.py")
    
    # Generate MCP config for Windsurf
    windsurf_config = {
        "name": "BraveSearchAgent",
        "command": python_path,
        "args": [mcp_server_path]
    }
    
    # Generate command for Cursor
    cursor_command = f"{python_path} {mcp_server_path}"
    
    print("\n=== MCP Configuration ===")
    print("\nFor Windsurf:")
    print(json.dumps(windsurf_config, indent=2))
    
    print("\nFor Cursor:")
    print("Name: BraveSearchAgent")
    print("Type: command")
    print(f"Command: {cursor_command}")
    
    print("\nSetup complete! You can now configure your AI IDE to use the BraveSearchAgent.")

def main():
    """Main setup function."""
    print("Setting up BraveSearchAgent MCP server...")
    
    # Create virtual environment
    create_venv()
    
    # Install dependencies
    install_dependencies()
    
    # Generate MCP configuration
    generate_mcp_config()

if __name__ == "__main__":
    main() 