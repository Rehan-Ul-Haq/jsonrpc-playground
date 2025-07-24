"""
Test Suite for JSON-RPC Playground Main Module

Tests the main application launcher functionality.
"""

from unittest import mock

import pytest

# Import main components
from jsonrpc_playground.main import PlaygroundLauncher


@pytest.mark.unit
class TestPlaygroundLauncher:
    """Test the main application launcher."""

    def setup_method(self):
        """Setup before each test method."""
        self.launcher = PlaygroundLauncher(server_port=4002, client_port=8502)

    def test_launcher_initialization(self):
        """Test launcher initialization."""
        assert self.launcher.server_port == 4002
        assert self.launcher.client_port == 8502
        assert self.launcher.server_proc is None
        assert self.launcher.client_proc is None

    def test_launcher_default_ports(self):
        """Test launcher with default ports."""
        launcher = PlaygroundLauncher()
        assert launcher.server_port == 4000
        assert launcher.client_port == 8501

    @mock.patch("subprocess.Popen")
    def test_start_server(self, mock_popen):
        """Test server startup."""
        mock_popen.return_value = mock.MagicMock()

        self.launcher._start_server()

        # Verify subprocess was called with correct arguments
        mock_popen.assert_called_once()
        args = mock_popen.call_args[0][0]
        assert "run_server.py" in " ".join(args)

    @mock.patch("subprocess.Popen")
    def test_start_client(self, mock_popen):
        """Test client startup."""
        mock_popen.return_value = mock.MagicMock()

        self.launcher._start_client()

        # Verify subprocess was called with streamlit
        mock_popen.assert_called_once()
        args = mock_popen.call_args[0][0]
        assert "streamlit" in " ".join(args)
        assert "run_client.py" in " ".join(args)

    @mock.patch("requests.post")
    def test_wait_for_server_success(self, mock_post):
        """Test successful server ready check."""
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        result = self.launcher._wait_for_server(timeout=1)
        assert result is True

    @mock.patch("requests.post")
    def test_wait_for_server_timeout(self, mock_post):
        """Test server ready check timeout."""
        mock_post.side_effect = Exception("Connection failed")

        result = self.launcher._wait_for_server(timeout=1)
        assert result is False

    def test_cleanup_no_processes(self):
        """Test cleanup when no processes are running."""
        # Should not raise any exceptions
        self.launcher._cleanup()

    @mock.patch("subprocess.Popen")
    def test_cleanup_with_processes(self, mock_popen):
        """Test cleanup with running processes."""
        mock_proc = mock.MagicMock()
        mock_popen.return_value = mock_proc

        # Set up mock processes
        self.launcher.server_proc = mock_proc
        self.launcher.client_proc = mock_proc

        self.launcher._cleanup()

        # Verify terminate was called
        assert mock_proc.terminate.call_count == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
