#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import signal
import atexit

def start_streamlit():
    """Start the Streamlit app."""
    print("Starting Streamlit app...")
    streamlit_process = subprocess.Popen(
        ["streamlit", "run", "streamlit_app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return streamlit_process

def start_mcp_server():
    """Start the MCP server."""
    print("Starting MCP server...")
    mcp_process = subprocess.Popen(
        [sys.executable, "src/mcp_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return mcp_process

def cleanup(processes):
    """Clean up processes on exit."""
    print("\nShutting down processes...")
    for process in processes:
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

def main():
    """Main function to run both the Streamlit app and MCP server."""
    print("Starting Company Analyzer application...")
    
    # Start processes
    streamlit_process = start_streamlit()
    mcp_process = start_mcp_server()
    
    # Register cleanup function
    processes = [streamlit_process, mcp_process]
    atexit.register(cleanup, processes)
    
    # Handle keyboard interrupt
    def signal_handler(sig, frame):
        print("\nReceived interrupt signal. Shutting down...")
        cleanup(processes)
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Print URLs
    print("\n=== Company Analyzer is running ===")
    print("Streamlit app: http://localhost:8501")
    print("MCP server is running in the background")
    print("\nPress Ctrl+C to stop all services\n")
    
    # Keep the script running
    try:
        while True:
            # Check if processes are still running
            if streamlit_process.poll() is not None:
                print("Streamlit app has stopped. Restarting...")
                streamlit_process = start_streamlit()
                processes[0] = streamlit_process
            
            if mcp_process.poll() is not None:
                print("MCP server has stopped. Restarting...")
                mcp_process = start_mcp_server()
                processes[1] = mcp_process
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt. Shutting down...")
        cleanup(processes)

if __name__ == "__main__":
    main() 