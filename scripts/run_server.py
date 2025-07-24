#!/usr/bin/env python3
"""
Server entry point for JSON-RPC Playground
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from jsonrpc_playground.server import main

if __name__ == "__main__":
    main()
