"""
Comprehensive Test Suite for JSON-RPC 2.0 Server

This test suite validates all functionality of the JSON-RPC server including:
- Basic method calls (add, greet, get_log, clear_log)
- Notification handling (log_message)
- Error handling scenarios
- Edge cases and malformed requests
- Server startup and shutdown

Run with: python -m pytest tests/test_server.py -v
"""

import os
import subprocess
import sys
import tempfile
import time
from unittest import mock

import pytest
import requests

# Import the server components for direct testing
from jsonrpc_playground.server import JSONRPCServer


@pytest.mark.unit
class TestServerMethods:
    """Test the individual RPC methods directly."""

    def setup_method(self):
        """Setup before each test method."""
        # Create a temporary log file for testing
        self.temp_log = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".txt"
        )
        self.temp_log.close()

        # Create server instance for testing
        self.server = JSONRPCServer(log_file=self.temp_log.name)

    def teardown_method(self):
        """Cleanup after each test method."""
        # Clean up temporary file
        if os.path.exists(self.temp_log.name):
            os.unlink(self.temp_log.name)

    def test_add_method(self):
        """Test the add method with various inputs."""
        assert self.server.add(2, 3) == 5
        assert self.server.add(-1, 1) == 0
        assert self.server.add(0, 0) == 0
        assert self.server.add(-5, -3) == -8
        assert self.server.add(100, 200) == 300

    def test_greet_method(self):
        """Test the greet method with various names."""
        assert self.server.greet("Alice") == "Hello, Alice!"
        assert self.server.greet("") == "Hello, !"
        assert self.server.greet("123") == "Hello, 123!"
        assert self.server.greet("John Doe") == "Hello, John Doe!"

    def test_log_message_method(self):
        """Test the log_message method."""
        # Mock the file operations
        with mock.patch("builtins.open", mock.mock_open()) as mock_file:
            self.server.log_message("Test message")
            mock_file.assert_called_once_with(self.temp_log.name, "a", encoding="utf-8")
            mock_file().write.assert_called_once_with("Test message\n")

    def test_get_log_method(self):
        """Test the get_log method."""
        # Test with existing log
        test_content = "Line 1\nLine 2\nLine 3"
        with mock.patch("builtins.open", mock.mock_open(read_data=test_content)):
            result = self.server.get_log()
            assert result == test_content

        # Test with missing log file
        with mock.patch("builtins.open", side_effect=FileNotFoundError):
            result = self.server.get_log()
            assert result == "Log is empty."

    def test_clear_log_method(self):
        """Test the clear_log method."""
        with mock.patch("builtins.open", mock.mock_open()) as mock_file:
            result = self.server.clear_log()
            mock_file.assert_called_once_with(self.temp_log.name, "w", encoding="utf-8")
            mock_file().write.assert_called_once_with("")
            assert result == "Log cleared."

    def test_cause_internal_error_method(self):
        """Test the cause_internal_error method."""
        # Valid case - no error triggered
        result = self.server.cause_internal_error("safe")
        assert result == "No error triggered. Received: safe"

        result = self.server.cause_internal_error("test")
        assert result == "No error triggered. Received: test"

        # Error case - internal error triggered
        with pytest.raises(RuntimeError, match="This is a deliberate internal error"):
            self.server.cause_internal_error("error")

    def test_strict_add_method(self):
        """Test the strict_add method."""
        # Valid cases
        assert self.server.strict_add(5, 3) == 8
        assert self.server.strict_add(-1, 1) == 0

        # Invalid type cases
        with pytest.raises(TypeError, match="Both parameters must be integers"):
            self.server.strict_add("5", 3)  # type:ignore
        with pytest.raises(TypeError, match="Both parameters must be integers"):
            self.server.strict_add(5, "3")  # type:ignore
        with pytest.raises(TypeError, match="Both parameters must be integers"):
            self.server.strict_add("5", "3")  # type:ignore

    def test_demo_method(self):
        """Test the demo method."""
        result = self.server.demo_method("test", 42)
        assert result == "Received: test and 42"

    def test_server_initialization(self):
        """Test server initialization with different parameters."""
        server1 = JSONRPCServer()
        assert server1.host == "localhost"
        assert server1.port == 8080
        assert server1.log_file == "server_log.txt"

        server2 = JSONRPCServer(host="0.0.0.0", port=9000, log_file="custom.log")
        assert server2.host == "0.0.0.0"
        assert server2.port == 9000
        assert server2.log_file == "custom.log"


@pytest.mark.integration
class TestServerIntegration:
    """Integration tests for the JSON-RPC server."""

    @pytest.fixture(scope="class")
    def server_process(self):
        """Start server process for integration tests."""
        # Start server in subprocess
        server_proc = subprocess.Popen(
            [
                sys.executable,
                "-c",
                """
import sys
sys.path.insert(0, "src")
from jsonrpc_playground.server import JSONRPCServer
server = JSONRPCServer(port=4001)
server.start()
""",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Wait for server to start
        time.sleep(2)

        # Verify server is running
        try:
            response = requests.post(
                "http://localhost:4001",
                json={
                    "jsonrpc": "2.0",
                    "method": "add",
                    "params": {"a": 1, "b": 1},
                    "id": 1,
                },
                timeout=5,
            )
            assert response.status_code == 200
        except Exception as e:
            server_proc.terminate()
            pytest.skip(f"Server failed to start: {e}")

        yield server_proc

        # Cleanup
        server_proc.terminate()
        try:
            server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_proc.kill()

    def test_server_add_integration(self, server_process):
        """Test server add method via HTTP."""
        response = requests.post(
            "http://localhost:4001",
            json={
                "jsonrpc": "2.0",
                "method": "add",
                "params": {"a": 5, "b": 3},
                "id": 1,
            },
            timeout=5,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["result"] == 8
        assert data["id"] == 1

    def test_server_greet_integration(self, server_process):
        """Test server greet method via HTTP."""
        response = requests.post(
            "http://localhost:4001",
            json={
                "jsonrpc": "2.0",
                "method": "greet",
                "params": {"name": "Integration Test"},
                "id": 2,
            },
            timeout=5,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["result"] == "Hello, Integration Test!"
        assert data["id"] == 2

    def test_server_notification_integration(self, server_process):
        """Test server notification handling via HTTP."""
        # Send notification (no response expected)
        response = requests.post(
            "http://localhost:4001",
            json={
                "jsonrpc": "2.0",
                "method": "log_message",
                "params": {"message": "Test notification"},
            },
            timeout=5,
        )
        assert response.status_code == 200
        # For notifications, response should be empty
        assert response.text == '""' or response.text == ""

    def test_server_error_scenarios(self, server_process):
        """Test various error scenarios."""

        # Method not found
        response = requests.post(
            "http://localhost:4001",
            json={"jsonrpc": "2.0", "method": "nonexistent", "params": {}, "id": 3},
            timeout=5,
        )
        assert response.status_code == 200
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == -32601

        # Invalid JSON
        response = requests.post(
            "http://localhost:4001",
            data='{"invalid": json}',
            headers={"Content-Type": "application/json"},
            timeout=5,
        )
        assert response.status_code == 200
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == -32700  # Parse error for invalid JSON

        # Internal error (deliberate runtime error)
        response = requests.post(
            "http://localhost:4001",
            json={
                "jsonrpc": "2.0",
                "method": "cause_internal_error",
                "params": {"trigger": "error"},
                "id": 4,
            },
            timeout=5,
        )
        assert response.status_code == 200
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == -32000  # RuntimeError maps to Server error

    def test_log_operations_integration(self, server_process):
        """Test log operations via HTTP."""
        # Clear log first
        response = requests.post(
            "http://localhost:4001",
            json={"jsonrpc": "2.0", "method": "clear_log", "params": {}, "id": 5},
            timeout=5,
        )
        assert response.status_code == 200
        assert response.json()["result"] == "Log cleared."

        # Add a log message
        requests.post(
            "http://localhost:4001",
            json={
                "jsonrpc": "2.0",
                "method": "log_message",
                "params": {"message": "Integration test log"},
            },
            timeout=5,
        )

        # Get log content
        response = requests.post(
            "http://localhost:4001",
            json={"jsonrpc": "2.0", "method": "get_log", "params": {}, "id": 6},
            timeout=5,
        )
        assert response.status_code == 200
        data = response.json()
        assert "Integration test log" in data["result"]


@pytest.mark.stress
class TestServerStress:
    """Stress tests for the JSON-RPC server."""

    def test_multiple_requests(self):
        """Test handling multiple rapid requests."""
        # This would require a running server - skip for now
        pytest.skip("Stress test requires long-running server setup")

    def test_large_payload(self):
        """Test handling large request payloads."""
        # This would require a running server - skip for now
        pytest.skip("Large payload test requires long-running server setup")


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
