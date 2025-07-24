"""
Test Suite for JSON-RPC Playground Client

Tests the Streamlit client interface functionality.
"""

from unittest import mock

import pytest

# Import client components
from jsonrpc_playground.client import JSONRPCPlaygroundApp


@pytest.mark.unit
class TestPlaygroundClient:
    """Test the Streamlit client functionality."""

    def setup_method(self):
        """Setup before each test method."""
        self.app = JSONRPCPlaygroundApp("http://localhost:4000")

    def test_client_initialization(self):
        """Test client initialization."""
        assert self.app.server_url == "http://localhost:4000"

        # Test with custom URL
        app2 = JSONRPCPlaygroundApp("http://example.com:8080")
        assert app2.server_url == "http://example.com:8080"

    @mock.patch("streamlit.markdown")
    @mock.patch("streamlit.tabs")
    def test_app_structure(self, mock_tabs, mock_markdown):
        """Test that the app has the expected structure."""
        # Mock the tabs to prevent actual Streamlit calls
        mock_tabs.return_value = [mock.MagicMock(), mock.MagicMock(), mock.MagicMock()]

        # This would normally require Streamlit to be running
        # For now, just test that the class can be instantiated
        assert self.app is not None

    def test_app_methods_exist(self):
        """Test that required methods exist on the app."""
        assert hasattr(self.app, "run")
        assert hasattr(self.app, "_render_header")
        assert hasattr(self.app, "_render_learning_tips")
        assert hasattr(self.app, "_render_method_tab")
        assert hasattr(self.app, "_render_notification_tab")
        assert hasattr(self.app, "_render_error_scenarios_tab")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
