#!/usr/bin/env python3
"""
Entry point for JSON-RPC Playground

This script serves as the main entry point for the JSON-RPC Playground application.
It can be used when the package is installed via pip/uv or run directly.

Usage:
    python main.py [server_port] [client_port]
    
Examples:
    python main.py                  # Use default ports (4000, 8501)
    python main.py 5000             # Custom server port, default client port
    python main.py 5000 8502        # Custom server and client ports
"""

import sys
import os

# Add the src directory to Python path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from jsonrpc_playground.main import main

if __name__ == "__main__":
    main()
