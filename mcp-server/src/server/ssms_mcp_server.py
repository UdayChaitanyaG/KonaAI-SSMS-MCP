"""
KonaAI SSMS MCP Server

Main MCP server implementation for SQL Server Management Studio integration.
Provides enhanced database access capabilities through the Model Context Protocol.
"""

import asyncio
import logging
import sys
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    ListResourcesRequest,
    ListToolsRequest,
    ReadResourceRequest,
    Resource,
    Tool,
)

# Import configuration
from config.database_config import AppConfig

# Import database classes
from .database.master_db import MasterDatabase
from .database.datamgmt_db import DataManagementDatabase

# Import tools
from .tools.query_tool import QueryTool
from .tools.crud_tool import CrudTool
from .tools.schema_tool import SchemaTool
from .tools.sp_tool import StoredProcedureTool

# Import resources
from .resources.tables import TablesResource
from .resources.procedures import ProceduresResource
from .resources.triggers import TriggersResource
from .resources.views import ViewsResource

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SSMSServer:
    """
    KonaAI SSMS MCP Server implementation.
    
    Provides comprehensive SQL Server database access through MCP protocol.
    """
    
    def __init__(self):
        """Initialize the MCP server with all components."""
        self.settings = AppConfig()
        self.server = Server("konaai-ssms")
        
        # Initialize database connections
        self.master_db = MasterDatabase(self.settings.get_master_db_config())
        self.datamgmt_db = DataManagementDatabase(self.settings.get_data_mgmt_db_config())
        
        # Initialize tools
        self.query_tool = QueryTool(self.master_db, self.datamgmt_db)
        self.crud_tool = CrudTool(self.master_db, self.datamgmt_db)
        self.schema_tool = SchemaTool(self.master_db, self.datamgmt_db)
        self.sp_tool = StoredProcedureTool(self.master_db, self.datamgmt_db)
        
        # Initialize resources
        self.tables_resource = TablesResource(self.master_db, self.datamgmt_db)
        self.procedures_resource = ProceduresResource(self.master_db, self.datamgmt_db)
        self.triggers_resource = TriggersResource(self.master_db, self.datamgmt_db)
        self.views_resource = ViewsResource(self.master_db, self.datamgmt_db)
        
        # Register handlers
        self._register_handlers()
        
        logger.info("SSMS MCP Server initialized successfully")
    
    def _register_handlers(self):
        """Register MCP handlers for tools and resources."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List all available tools."""
            tools = []
            
            # Add query tool
            tools.append(Tool(
                name="execute_query",
                description="Execute SQL queries (SELECT, INSERT, UPDATE, DELETE) on either database",
                inputSchema=self.query_tool.get_input_schema()
            ))
            
            # Add CRUD tools
            tools.append(Tool(
                name="insert_data",
                description="Insert data into a table",
                inputSchema=self.crud_tool.get_insert_schema()
            ))
            
            tools.append(Tool(
                name="update_data",
                description="Update data in a table",
                inputSchema=self.crud_tool.get_update_schema()
            ))
            
            tools.append(Tool(
                name="delete_data",
                description="Delete data from a table",
                inputSchema=self.crud_tool.get_delete_schema()
            ))
            
            # Add schema tools
            tools.append(Tool(
                name="get_schema",
                description="Get comprehensive database schema information",
                inputSchema=self.schema_tool.get_schema_schema()
            ))
            
            tools.append(Tool(
                name="get_tables",
                description="Get list of tables with metadata",
                inputSchema=self.schema_tool.get_tables_schema()
            ))
            
            tools.append(Tool(
                name="get_table_schema",
                description="Get detailed table schema information",
                inputSchema=self.schema_tool.get_table_schema_schema()
            ))
            
            tools.append(Tool(
                name="get_stored_procedures",
                description="Get list of stored procedures",
                inputSchema=self.schema_tool.get_procedures_schema()
            ))
            
            tools.append(Tool(
                name="get_triggers",
                description="Get list of triggers",
                inputSchema=self.schema_tool.get_triggers_schema()
            ))
            
            tools.append(Tool(
                name="get_views",
                description="Get list of views",
                inputSchema=self.schema_tool.get_views_schema()
            ))
            
            # Add stored procedure tool
            tools.append(Tool(
                name="execute_procedure",
                description="Execute stored procedures with parameters",
                inputSchema=self.sp_tool.get_input_schema()
            ))
            
            return tools
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
            """Handle tool execution requests."""
            try:
                if name == "execute_query":
                    return await self.query_tool.execute_query(arguments)
                elif name == "insert_data":
                    return await self.crud_tool.insert_data(arguments)
                elif name == "update_data":
                    return await self.crud_tool.update_data(arguments)
                elif name == "delete_data":
                    return await self.crud_tool.delete_data(arguments)
                elif name == "get_schema":
                    return await self.schema_tool.get_schema(arguments)
                elif name == "get_tables":
                    return await self.schema_tool.get_tables(arguments)
                elif name == "get_table_schema":
                    return await self.schema_tool.get_table_schema(arguments)
                elif name == "get_stored_procedures":
                    return await self.schema_tool.get_stored_procedures(arguments)
                elif name == "get_triggers":
                    return await self.schema_tool.get_triggers(arguments)
                elif name == "get_views":
                    return await self.schema_tool.get_views(arguments)
                elif name == "execute_procedure":
                    return await self.sp_tool.execute_procedure(arguments)
                else:
                    return {
                        "error": f"Unknown tool: {name}",
                        "available_tools": [
                            "execute_query", "insert_data", "update_data", "delete_data",
                            "get_schema", "get_tables", "get_table_schema", "get_stored_procedures",
                            "get_triggers", "get_views", "execute_procedure"
                        ]
                    }
            except Exception as e:
                logger.error(f"Error executing tool {name}: {str(e)}")
                return {"error": f"Tool execution failed: {str(e)}"}
        
        @self.server.list_resources()
        async def list_resources() -> List[Resource]:
            """List all available resources."""
            resources = []
            
            # Add table resources
            resources.extend(await self.tables_resource.list_resources())
            
            # Add procedure resources
            resources.extend(await self.procedures_resource.list_resources())
            
            # Add trigger resources
            resources.extend(await self.triggers_resource.list_resources())
            
            # Add view resources
            resources.extend(await self.views_resource.list_resources())
            
            return resources
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Handle resource read requests."""
            try:
                # Route to appropriate resource handler
                if uri.startswith("ssms://master/tables/") or uri.startswith("ssms://datamgmt/tables/"):
                    return await self.tables_resource.read_resource(uri)
                elif uri.startswith("ssms://master/procedures/") or uri.startswith("ssms://datamgmt/procedures/"):
                    return await self.procedures_resource.read_resource(uri)
                elif uri.startswith("ssms://master/triggers/") or uri.startswith("ssms://datamgmt/triggers/"):
                    return await self.triggers_resource.read_resource(uri)
                elif uri.startswith("ssms://master/views/") or uri.startswith("ssms://datamgmt/views/"):
                    return await self.views_resource.read_resource(uri)
                else:
                    return f"Unknown resource URI: {uri}"
            except Exception as e:
                logger.error(f"Error reading resource {uri}: {str(e)}")
                return f"Resource read failed: {str(e)}"
    
    async def run(self):
        """Run the MCP server with StdIO transport."""
        try:
            logger.info("Starting SSMS MCP Server...")
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options()
                )
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
            raise
        finally:
            # Cleanup database connections
            await self.cleanup()
    
    def test_connection(self):
        """Test database connection and display table information."""
        print("SSMS MCP Server - Database Connection Test")
        print("=" * 60)
        
        try:
            # Test Master Database
            print("Testing Master Database Connection...")
            master_tables = self.master_db.get_tables()
            print(f"Master Database: {len(master_tables)} tables found")
            
            if master_tables:
                print("First 5 tables in Master Database:")
                for i, table in enumerate(master_tables[:5], 1):
                    print(f"   {i}. {table['table_name']} (Schema: {table['table_schema']})")
            
            # Test Data Management Database
            print("\nTesting Data Management Database Connection...")
            datamgmt_tables = self.datamgmt_db.get_tables()
            print(f"Data Management Database: {len(datamgmt_tables)} tables found")
            
            if datamgmt_tables:
                print("First 5 tables in Data Management Database:")
                for i, table in enumerate(datamgmt_tables[:5], 1):
                    print(f"   {i}. {table['table_name']} (Schema: {table['table_schema']})")
            
            print("\nDatabase connection test completed successfully!")
            return True
            
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            print("\nTroubleshooting steps:")
            print("1. Ensure SQL Server is running")
            print("2. Check Windows Authentication is enabled")
            print("3. Verify database access permissions")
            return False

    async def cleanup(self):
        """Cleanup database connections."""
        try:
            await self.master_db.close_all_connections()
            await self.datamgmt_db.close_all_connections()
            logger.info("Database connections closed")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")


async def main():
    """Main entry point for the MCP server."""
    server = SSMSServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
