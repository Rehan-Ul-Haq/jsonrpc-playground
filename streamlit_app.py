#!/usr/bin/env python3
"""
Streamlit Cloud entry point for JSON-RPC Playground
This file is specifically for Streamlit Cloud deployment.
"""
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the client
from jsonrpc_playground.client import main

if __name__ == "__main__":
    main()
