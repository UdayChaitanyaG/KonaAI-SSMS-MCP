#!/usr/bin/env python3
"""
MCP Tools Testing Script
Tests individual MCP tools to ensure they work correctly.
"""

import sys
import asyncio
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_dir))

# Import centralized configuration
from config.app_config import setup_environment

# Set up environment variables
setup_environment()

# Import MCP server and tools
from server.ssms_mcp_server import SSMSServer

async def test_mcp_tools():
    """Test individual MCP tools."""
    print("MCP Tools Testing")
    print("=" * 20)
    
    try:
        # Initialize server
        server = SSMSServer()
        print("OK Server initialized")
        
        # Test Query Tool
        print("\nTesting Query Tool:")
        try:
            # Test simple query
            result = await server.query_tool.execute_query({
                'database': 'master',
                'query': 'SELECT TOP 1 * FROM App.Client',
                'max_rows': 5
            })
            print("OK Query tool working")
            print(f"   Result: {len(result.get('data', []))} rows returned")
        except Exception as e:
            print(f"ERROR Query tool failed: {str(e)}")
        
        # Test Schema Tool
        print("\nTesting Schema Tool:")
        try:
            result = await server.schema_tool.get_tables({
                'database': 'master'
            })
            print("OK Schema tool working")
            print(f"   Result: {len(result.get('tables', []))} tables found")
        except Exception as e:
            print(f"ERROR Schema tool failed: {str(e)}")
        
        # Test CRUD Tool
        print("\nTesting CRUD Tool:")
        try:
            # Test read operation
            result = await server.crud_tool.read_data({
                'database': 'master',
                'table': 'App.Client',
                'limit': 5
            })
            print("OK CRUD tool working")
            print(f"   Result: {len(result.get('data', []))} rows returned")
        except Exception as e:
            print(f"ERROR CRUD tool failed: {str(e)}")
        
        print("\nMCP Tools testing completed!")
        return True
        
    except Exception as e:
        print(f"Error testing MCP tools: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_mcp_tools())
    sys.exit(0 if success else 1)
