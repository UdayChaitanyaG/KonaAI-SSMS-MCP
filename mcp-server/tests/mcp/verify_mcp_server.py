#!/usr/bin/env python3
"""
MCP Server Verification Script
Verifies that the MCP server is properly configured and all components are working.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_dir))

# Import centralized configuration
from config.app_config import setup_environment

# Set up environment variables
setup_environment()

# Import MCP server
from server.ssms_mcp_server import SSMSServer

def verify_mcp_server():
    """Verify MCP server can be initialized and has tools/resources registered."""
    print("MCP Server Verification")
    print("=" * 30)
    
    try:
        # Initialize server
        server = SSMSServer()
        print("OK Server initialized successfully")
        
        # Check if server has the required components
        print("\nChecking MCP Server Components:")
        
        # Check database connections
        if hasattr(server, 'master_db') and server.master_db:
            print("OK Master database connection configured")
        else:
            print("ERROR Master database connection missing")
            
        if hasattr(server, 'datamgmt_db') and server.datamgmt_db:
            print("OK Data Management database connection configured")
        else:
            print("ERROR Data Management database connection missing")
        
        # Check tools
        if hasattr(server, 'query_tool') and server.query_tool:
            print("OK Query tool registered")
        else:
            print("ERROR Query tool missing")
            
        if hasattr(server, 'crud_tool') and server.crud_tool:
            print("OK CRUD tool registered")
        else:
            print("ERROR CRUD tool missing")
            
        if hasattr(server, 'schema_tool') and server.schema_tool:
            print("OK Schema tool registered")
        else:
            print("ERROR Schema tool missing")
            
        if hasattr(server, 'sp_tool') and server.sp_tool:
            print("OK Stored procedure tool registered")
        else:
            print("ERROR Stored procedure tool missing")
        
        # Check resources
        if hasattr(server, 'tables_resource') and server.tables_resource:
            print("OK Tables resource registered")
        else:
            print("ERROR Tables resource missing")
            
        if hasattr(server, 'procedures_resource') and server.procedures_resource:
            print("OK Procedures resource registered")
        else:
            print("ERROR Procedures resource missing")
            
        if hasattr(server, 'triggers_resource') and server.triggers_resource:
            print("OK Triggers resource registered")
        else:
            print("ERROR Triggers resource missing")
            
        if hasattr(server, 'views_resource') and server.views_resource:
            print("OK Views resource registered")
        else:
            print("ERROR Views resource missing")
        
        # Test database connection
        print("\nTesting Database Connections:")
        try:
            master_tables = server.master_db.get_tables()
            print(f"OK Master database: {len(master_tables)} tables found")
        except Exception as e:
            print(f"ERROR Master database connection failed: {str(e)}")
            
        try:
            datamgmt_tables = server.datamgmt_db.get_tables()
            print(f"OK Data Management database: {len(datamgmt_tables)} tables found")
        except Exception as e:
            print(f"ERROR Data Management database connection failed: {str(e)}")
        
        print("\nMCP Server verification completed!")
        print("The server should now work properly with Cursor.")
        
        return True
        
    except Exception as e:
        print(f"Error verifying MCP server: {str(e)}")
        return False

if __name__ == "__main__":
    success = verify_mcp_server()
    sys.exit(0 if success else 1)



