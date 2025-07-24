#!/usr/bin/env python3
"""
Render deployment entry point for JSON-RPC Playground

This script is specifically designed for Render.com deployment.
It runs both the JSON-RPC server and Streamlit client in a single process.
"""

import os
import sys
import threading
import time
import subprocess

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from jsonrpc_playground.server import JSONRPCServer

def run_json_rpc_server():
    """Run the JSON-RPC server on port 4000."""
    print("🔧 Starting JSON-RPC server on port 4000...")
    
    try:
        server = JSONRPCServer(host="0.0.0.0", port=4000)
        print("✅ JSON-RPC server is starting on port 4000")
        server.start()
    except Exception as e:
        print(f"❌ Failed to start JSON-RPC server: {e}")

def run_streamlit_client():
    """Run the Streamlit client."""
    print("🌐 Starting Streamlit client...")
    
    # Wait a moment for the server to start
    time.sleep(2)
    
    # Get the port from environment (Render sets this)
    port = os.environ.get('PORT', '8501')
    
    try:
        # Run streamlit with the render-specific entry point
        subprocess.run([
            sys.executable, 
            "-m", 
            "streamlit", 
            "run", 
            "streamlit_app.py",
            "--server.port", 
            port,
            "--server.address", 
            "0.0.0.0",
            "--server.headless", 
            "true",
            "--server.enableCORS", 
            "false",
            "--server.enableXsrfProtection", 
            "false"
        ])
    except Exception as e:
        print(f"❌ Failed to start Streamlit client: {e}")

def main():
    """Main entry point for Render deployment."""
    print("🚀 Starting JSON-RPC Playground on Render...")
    
    # Start JSON-RPC server in a separate thread
    server_thread = threading.Thread(target=run_json_rpc_server, daemon=True)
    server_thread.start()
    
    # Start Streamlit client in the main thread
    run_streamlit_client()

if __name__ == "__main__":
    main()
