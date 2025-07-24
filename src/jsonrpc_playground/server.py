"""
JSON-RPC 2.0 Server Implementation

This module provides a HTTP server that implements JSON-RPC 2.0 protocol.
It includes various methods for demonstration purposes including arithmetic operations,
logging functionality, and error handling examples.
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional

from jsonrpc import JSONRPCResponseManager, dispatcher


class JSONRPCServer:
    """JSON-RPC 2.0 Server class for educational demonstrations."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        log_file: str = "server_log.txt",
    ):
        """Initialize the JSON-RPC server.

        Args:
            host: Server host address
            port: Server port number
            log_file: Path to log file for logging operations
        """
        self.host = host
        self.port = port
        self.log_file = log_file
        self.server: Optional[HTTPServer] = None
        self._setup_methods()

    def _setup_methods(self):
        """Setup all JSON-RPC methods."""
        # Clear existing methods
        dispatcher.method_map.clear()

        # Add arithmetic methods
        dispatcher.add_method(self.add, "add")
        dispatcher.add_method(self.strict_add, "strict_add")
        dispatcher.add_method(self.cause_internal_error, "cause_internal_error")

        # Add utility methods
        dispatcher.add_method(self.greet, "greet")
        dispatcher.add_method(self.demo_method, "demo_method")

        # Add logging methods
        dispatcher.add_method(self.log_message, "log_message")
        dispatcher.add_method(self.get_log, "get_log")
        dispatcher.add_method(self.clear_log, "clear_log")

    # --- JSON-RPC Methods ---

    def add(self, a: int, b: int) -> int:
        """Add two integers and return the result."""
        return a + b

    def greet(self, name: str) -> str:
        """Return a greeting message for the given name."""
        return f"Hello, {name}!"

    def log_message(self, message: str) -> None:
        """Log a message to the server log file."""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(message + "\n")

    def get_log(self) -> str:
        """Return the contents of the server log file."""
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "Log is empty."

    def clear_log(self) -> str:
        """Clear the server log file and return confirmation message."""
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("")
        return "Log cleared."

    def cause_internal_error(self, trigger: str = "error") -> str:
        """Deliberately cause an internal error for demonstration purposes.

        Args:
            trigger: A string that if equals 'error', will cause an internal error

        Returns:
            Success message if no error is triggered

        Raises:
            RuntimeError: When trigger equals 'error' to demonstrate -32603 internal error
        """
        if trigger == "error":
            raise RuntimeError("This is a deliberate internal error for demonstration")
        return f"No error triggered. Received: {trigger}"

    def strict_add(self, a: int, b: int) -> int:
        """Strictly typed addition - will cause -32602 error if wrong types sent."""
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError("Both parameters must be integers")
        return a + b

    def demo_method(self, param1: str, param2: int) -> str:
        """Demo method with specific parameter requirements."""
        return f"Received: {param1} and {param2}"

    def start(self):
        """Start the JSON-RPC server."""
        print(f"Starting JSON-RPC 2.0 Server at http://{self.host}:{self.port}")
        self.server = HTTPServer((self.host, self.port), self._create_request_handler())
        self.server.serve_forever()

    def stop(self):
        """Stop the JSON-RPC server."""
        if self.server:
            self.server.shutdown()
            self.server = None

    def _create_request_handler(self):
        """Create a request handler class with access to server instance."""

        class RequestHandler(BaseHTTPRequestHandler):
            """HTTP request handler for JSON-RPC 2.0 requests."""

            def do_POST(self):
                """Handle HTTP POST requests containing JSON-RPC calls."""
                try:
                    content_length = int(self.headers["Content-Length"])
                    request_data = self.rfile.read(content_length).decode()

                    # Handle the request with JSONRPCResponseManager
                    response = JSONRPCResponseManager.handle(request_data, dispatcher)

                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    # Send response data
                    if response:
                        self.wfile.write(json.dumps(response.data).encode())
                    else:
                        # This handles notifications (no response expected)
                        self.wfile.write(b"")

                except (ValueError, KeyError, UnicodeDecodeError) as e:
                    # Handle JSON parsing and encoding errors
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    error_response = {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32603,
                            "message": "Internal error",
                            "data": str(e),
                        },
                        "id": None,
                    }
                    self.wfile.write(json.dumps(error_response).encode())
                except Exception as e:
                    # Handle any other unexpected server-side errors
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    error_response = {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32603,
                            "message": "Internal error",
                            "data": str(e),
                        },
                        "id": None,
                    }
                    self.wfile.write(json.dumps(error_response).encode())

        return RequestHandler


def main():
    """Main entry point for running the server standalone."""
    server = JSONRPCServer(host="localhost", port=4000)
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop()


if __name__ == "__main__":
    main()
