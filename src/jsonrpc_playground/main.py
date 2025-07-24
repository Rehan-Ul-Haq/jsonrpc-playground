"""
JSON-RPC Playground Main Application

This module provides the main entry point for the JSON-RPC Playground application.
It orchestrates the startup of both the JSON-RPC server and the Streamlit client interface.
"""

import os
import subprocess
import sys
import time
from typing import Optional

import requests


class PlaygroundLauncher:
    """Launcher for the JSON-RPC Playground application."""

    def __init__(self, server_port: int = 4000, client_port: int = 8501):
        """Initialize the playground launcher.

        Args:
            server_port: Port for the JSON-RPC server
            client_port: Port for the Streamlit client
        """
        self.server_port = server_port
        self.client_port = client_port
        self.server_proc: Optional[subprocess.Popen] = None
        self.client_proc: Optional[subprocess.Popen] = None

    def start(self):
        """Start both server and client applications."""
        print("🚀 Starting JSON-RPC Playground...")

        try:
            # Start the JSON-RPC server
            self._start_server()

            # Wait for server to be ready
            if not self._wait_for_server():
                print("❌ Server failed to start in time.")
                self._cleanup()
                return False

            # Start the Streamlit client
            self._start_client()

            print("✅ JSON-RPC Playground is running!")
            print(f"🌐 Open your browser to: http://localhost:{self.client_port}")
            print(f"🔧 JSON-RPC Server: http://localhost:{self.server_port}")
            print("Press Ctrl+C to stop the application.")

            # Wait for the client process to finish
            if self.client_proc:
                self.client_proc.wait()

        except KeyboardInterrupt:
            print("\n🛑 Shutting down JSON-RPC Playground...")
        finally:
            self._cleanup()

    def _start_server(self):
        """Start the JSON-RPC server in a subprocess."""
        print(f"🔧 Starting JSON-RPC server on port {self.server_port}...")

        try:
            # Use the scripts/run_server.py script
            server_script = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "scripts",
                "run_server.py",
            )
            self.server_proc = subprocess.Popen(
                [sys.executable, server_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as e:
            print(f"❌ Failed to start JSON-RPC server: {e}")
            self.server_proc = None

    def _start_client(self):
        """Start the Streamlit client in a subprocess."""
        print(f"🌐 Starting Streamlit client on port {self.client_port}...")

        try:
            # Use the scripts/run_client.py script
            client_script = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "scripts",
                "run_client.py",
            )
            self.client_proc = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "streamlit",
                    "run",
                    client_script,
                    "--server.port",
                    str(self.client_port),
                    "--server.headless",
                    "true",
                ]
            )
        except Exception as e:
            print(f"❌ Failed to start Streamlit client: {e}")
            self.client_proc = None

    def _wait_for_server(self, timeout: int = 20) -> bool:
        """Wait for the server to be ready.

        Args:
            timeout: Maximum time to wait in seconds

        Returns:
            True if server is ready, False otherwise
        """
        server_url = f"http://localhost:{self.server_port}"

        for _ in range(timeout * 5):  # Check every 0.2 seconds
            try:
                # Try to make a simple request
                response = requests.post(
                    server_url,
                    json={
                        "jsonrpc": "2.0",
                        "method": "add",
                        "params": {"a": 1, "b": 1},
                        "id": "test",
                    },
                    timeout=0.5,
                )
                if response.status_code == 200:
                    print("✅ JSON-RPC server is ready!")
                    return True
            except Exception:
                time.sleep(0.2)
                continue

        return False

    def _cleanup(self):
        """Clean up running processes."""
        if self.server_proc:
            print("🛑 Stopping JSON-RPC server...")
            self.server_proc.terminate()
            try:
                self.server_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.server_proc.kill()
                self.server_proc.wait()

        if self.client_proc:
            print("🛑 Stopping Streamlit client...")
            self.client_proc.terminate()
            try:
                self.client_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.client_proc.kill()
                self.client_proc.wait()


def main():
    """Main entry point for the JSON-RPC Playground."""
    # Handle command line arguments for custom ports
    server_port = 4000
    client_port = 8501

    if len(sys.argv) > 1:
        try:
            server_port = int(sys.argv[1])
        except ValueError:
            print("Warning: Invalid server port, using default 4000")

    if len(sys.argv) > 2:
        try:
            client_port = int(sys.argv[2])
        except ValueError:
            print("Warning: Invalid client port, using default 8501")

    launcher = PlaygroundLauncher(server_port, client_port)
    launcher.start()


if __name__ == "__main__":
    main()
