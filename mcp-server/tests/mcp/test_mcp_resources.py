#!/usr/bin/env python3
"""
MCP Resources Testing Script
Tests individual MCP resources to ensure they work correctly.
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

# Import MCP server and resources
from server.ssms_mcp_server import SSMSServer

async def test_mcp_resources():
    """Test individual MCP resources."""
    print("MCP Resources Testing")
    print("=" * 25)
    
    try:
        # Initialize server
        server = SSMSServer()
        print("OK Server initialized")
        
        # Test Tables Resource
        print("\nTesting Tables Resource:")
        try:
            resources = await server.tables_resource.list_resources()
            print(f"OK Tables resource working")
            print(f"   Result: {len(resources)} table resources found")
        except Exception as e:
            print(f"ERROR Tables resource failed: {str(e)}")
        
        # Test Procedures Resource
        print("\nTesting Procedures Resource:")
        try:
            resources = await server.procedures_resource.list_resources()
            print(f"OK Procedures resource working")
            print(f"   Result: {len(resources)} procedure resources found")
        except Exception as e:
            print(f"ERROR Procedures resource failed: {str(e)}")
        
        # Test Triggers Resource
        print("\nTesting Triggers Resource:")
        try:
            resources = await server.triggers_resource.list_resources()
            print(f"OK Triggers resource working")
            print(f"   Result: {len(resources)} trigger resources found")
        except Exception as e:
            print(f"ERROR Triggers resource failed: {str(e)}")
        
        # Test Views Resource
        print("\nTesting Views Resource:")
        try:
            resources = await server.views_resource.list_resources()
            print(f"OK Views resource working")
            print(f"   Result: {len(resources)} view resources found")
        except Exception as e:
            print(f"ERROR Views resource failed: {str(e)}")
        
        print("\nMCP Resources testing completed!")
        return True
        
    except Exception as e:
        print(f"Error testing MCP resources: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_mcp_resources())
    sys.exit(0 if success else 1)



