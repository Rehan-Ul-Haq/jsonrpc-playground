#!/usr/bin/env python3
"""
Test the Render deployment setup locally
"""

import os
import subprocess
import sys

def test_local_deployment():
    """Test the render deployment locally."""
    print("🧪 Testing Render deployment setup locally...")
    
    # Set environment variables like Render would
    os.environ['PORT'] = '8501'
    
    try:
        # Run the render app
        subprocess.run([sys.executable, 'render_app.py'])
    except KeyboardInterrupt:
        print("\n✅ Local test completed. Press Ctrl+C to stop.")

if __name__ == "__main__":
    test_local_deployment()
