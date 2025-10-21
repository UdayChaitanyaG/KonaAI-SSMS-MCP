#!/usr/bin/env python3
"""
Test connection script for SSMS MCP Server
This script tests the database connection using the MCP server's built-in test method.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

# Import centralized configuration
from config.app_config import setup_environment

def test_mcp_connection():
    """Test database connection using MCP server's test method."""
    print("SSMS MCP Server - Connection Test")
    print("=" * 50)
    
    try:
        # Set up environment variables
        setup_environment()
        
        # Import MCP server
        from server.ssms_mcp_server import SSMSServer
        
        # Create server instance
        print("Initializing MCP Server...")
        server = SSMSServer()
        
        # Test connection
        print("Testing database connections...")
        success = server.test_connection()
        
        if success:
            print("\nMCP Server is ready for use!")
            print("You can now:")
            print("   - Start the MCP server with: python main.py")
            print("   - Connect MCP clients using mcp_config.json")
            print("   - Use the MCP tools and resources")
        else:
            print("\nMCP Server connection test failed")
            print("Please check the troubleshooting steps above")
        
        return success
        
    except Exception as e:
        print(f"Error during MCP server test: {str(e)}")
        print("\nPlease check:")
        print("1. Ensure all dependencies are installed")
        print("2. Verify database configuration")
        print("3. Check SQL Server is running")
        return False

if __name__ == "__main__":
    test_mcp_connection()
