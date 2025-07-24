"""
JSON-RPC Playground - An educational tool for learning JSON-RPC 2.0 protocol.

This package provides a comprehensive learning environment for understanding
JSON-RPC 2.0 with interactive examples, error scenarios, and real-time testing.
"""

__version__ = "0.1.0"
__author__ = "M Rehan ul Haq"
__email__ = "mrehanulhaq3@gmail.com"

from .client import JSONRPCPlaygroundApp
from .server import JSONRPCServer

__all__ = ["JSONRPCServer", "JSONRPCPlaygroundApp", "__version__"]
