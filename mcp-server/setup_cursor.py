#!/usr/bin/env python3
"""
Cursor MCP Setup Script
This script helps set up the SSMS MCP Server with Cursor IDE.
"""

import os
import json
import sys
from pathlib import Path

def get_project_path():
    """Get the absolute path to the mcp-server directory."""
    return Path(__file__).parent.absolute()

def create_cursor_config():
    """Create Cursor MCP configuration."""
    project_path = get_project_path()
    
    config = {
        "mcpServers": {
            "konaai-ssms": {
                "command": "python",
                "args": ["main.py"],
                "cwd": str(project_path),
                "env": {
                    "PYTHONPATH": "."
                }
            }
        }
    }
    
    return config

def save_cursor_config():
    """Save Cursor MCP configuration to file."""
    config = create_cursor_config()
    config_file = get_project_path() / "cursor_mcp_config.json"
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config_file

def test_mcp_server():
    """Test if the MCP server can start."""
    try:
        # Test database connection
        print("Testing database connection...")
        import subprocess
        result = subprocess.run([
            sys.executable, "tests/test_connection.py"
        ], capture_output=True, text=True, cwd=get_project_path())
        
        if result.returncode == 0:
            print("Database connection test passed")
            return True
        else:
            print("Database connection test failed")
            print("Error:", result.stderr)
            return False
    except Exception as e:
        print(f"Error testing MCP server: {e}")
        return False

def main():
    """Main setup function."""
    print("SSMS MCP Server - Cursor Setup")
    print("=" * 50)
    
    # Get project path
    project_path = get_project_path()
    print(f"Project path: {project_path}")
    
    # Test MCP server
    print("\nTesting MCP server...")
    if not test_mcp_server():
        print("\nMCP server test failed. Please check:")
        print("1. SQL Server is running")
        print("2. Database connections are working")
        print("3. All dependencies are installed")
        return False
    
    # Create Cursor configuration
    print("\nCreating Cursor MCP configuration...")
    config_file = save_cursor_config()
    print(f"Configuration saved to: {config_file}")
    
    # Display configuration
    print("\nCursor MCP Configuration:")
    print("-" * 40)
    config = create_cursor_config()
    print(json.dumps(config, indent=2))
    
    # Instructions
    print("\nNext Steps:")
    print("1. Copy the configuration above")
    print("2. Open Cursor IDE")
    print("3. Go to Settings > MCP")
    print("4. Add the configuration")
    print("5. Restart Cursor")
    print("6. The MCP server should appear in Cursor's MCP server list")
    
    print("\nSetup completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
