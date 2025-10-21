"""
Schema introspection tool for MCP server.
Provides comprehensive database schema information.
"""

import logging
from typing import Any, Dict, List, Optional

from mcp.types import Tool
from ..database.master_db import MasterDatabase
from ..database.datamgmt_db import DataManagementDatabase


logger = logging.getLogger(__name__)


class SchemaTool:
    """
    Tool for database schema introspection and analysis.
    """
    
    def __init__(self, master_db: MasterDatabase, data_mgmt_db: DataManagementDatabase):
        """
        Initialize schema tool.
        
        Args:
            master_db: Master database connection
            data_mgmt_db: Data Management database connection
        """
        self.master_db = master_db
        self.data_mgmt_db = data_mgmt_db
    
    def get_schema_tool(self) -> Tool:
        """
        Get the main schema tool definition.
        
        Returns:
            MCP Tool definition for schema operations
        """
        return Tool(
            name="get_schema",
            description="Get comprehensive database schema information",
            inputSchema={
                "type": "object",
                "properties": {
                    "database": {
                        "type": "string",
                        "enum": ["master", "datamgmt"],
                        "description": "Database to analyze"
                    },
                    "schema_type": {
                        "type": "string",
                        "enum": ["overview", "tables", "procedures", "triggers", "views", "relationships"],
                        "description": "Type of schema information to retrieve"
                    },
                    "table_name": {
                        "type": "string",
                        "description": "Specific table name (for detailed analysis)"
                    },
                    "schema_name": {
                        "type": "string",
                        "description": "Schema name (default: 'dbo')",
                        "default": "dbo"
                    }
                },
                "required": ["database", "schema_type"]
            }
        )
    
    def get_tables_tool(self) -> Tool:
        """
        Get the tables tool definition.
        
        Returns:
            MCP Tool definition for table operations
        """
        return Tool(
            name="get_tables",
            description="Get list of all tables in the database",
            inputSchema={
                "type": "object",
                "properties": {
                    "database": {
                        "type": "string",
                        "enum": ["master", "datamgmt"],
                        "description": "Database to query"
                    },
                    "include_views": {
                        "type": "boolean",
                        "description": "Include views in the results",
                        "default": False
                    }
                },
                "required": ["database"]
            }
        )
    
    def get_table_schema_tool(self) -> Tool:
        """
        Get the table schema tool definition.
        
        Returns:
            MCP Tool definition for table schema operations
        """
        return Tool(
            name="get_table_schema",
            description="Get detailed schema information for a specific table",
            inputSchema={
                "type": "object",
                "properties": {
                    "database": {
                        "type": "string",
                        "enum": ["master", "datamgmt"],
                        "description": "Database to query"
                    },
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table"
                    },
                    "schema_name": {
                        "type": "string",
                        "description": "Schema name (default: 'dbo')",
                        "default": "dbo"
                    },
                    "include_indexes": {
                        "type": "boolean",
                        "description": "Include index information",
                        "default": True
                    },
                    "include_foreign_keys": {
                        "type": "boolean",
                        "description": "Include foreign key relationships",
                        "default": True
                    }
                },
                "required": ["database", "table_name"]
            }
        )
    
    def get_stored_procedures_tool(self) -> Tool:
        """
        Get the stored procedures tool definition.
        
        Returns:
            MCP Tool definition for stored procedure operations
        """
        return Tool(
            name="get_stored_procedures",
            description="Get list of all stored procedures in the database",
            inputSchema={
                "type": "object",
                "properties": {
                    "database": {
                        "type": "string",
                        "enum": ["master", "datamgmt"],
                        "description": "Database to query"
                    },
                    "include_definition": {
                        "type": "boolean",
                        "description": "Include procedure definitions",
                        "default": False
                    }
                },
                "required": ["database"]
            }
        )
    
    def get_triggers_tool(self) -> Tool:
        """
        Get the triggers tool definition.
        
        Returns:
            MCP Tool definition for trigger operations
        """
        return Tool(
            name="get_triggers",
            description="Get list of all triggers in the database",
            inputSchema={
                "type": "object",
                "properties": {
                    "database": {
                        "type": "string",
                        "enum": ["master", "datamgmt"],
                        "description": "Database to query"
                    },
                    "include_definition": {
                        "type": "boolean",
                        "description": "Include trigger definitions",
                        "default": False
                    }
                },
                "required": ["database"]
            }
        )
    
    def get_views_tool(self) -> Tool:
        """
        Get the views tool definition.
        
        Returns:
            MCP Tool definition for view operations
        """
        return Tool(
            name="get_views",
            description="Get list of all views in the database",
            inputSchema={
                "type": "object",
                "properties": {
                    "database": {
                        "type": "string",
                        "enum": ["master", "datamgmt"],
                        "description": "Database to query"
                    },
                    "include_definition": {
                        "type": "boolean",
                        "description": "Include view definitions",
                        "default": False
                    }
                },
                "required": ["database"]
            }
        )
    
    def _get_database(self, database: str):
        """
        Get the appropriate database connection.
        
        Args:
            database: Database name ('master' or 'datamgmt')
            
        Returns:
            Database connection object
        """
        if database == 'master':
            return self.master_db
        elif database == 'datamgmt':
            return self.data_mgmt_db
        else:
            raise ValueError(f"Invalid database: {database}. Must be 'master' or 'datamgmt'")
    
    async def get_schema(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get comprehensive schema information.
        
        Args:
            args: Tool arguments
            
        Returns:
            Dictionary with schema information
        """
        try:
            database = args.get('database')
            schema_type = args.get('schema_type', 'overview')
            table_name = args.get('table_name')
            schema_name = args.get('schema_name', 'dbo')
            
            db = self._get_database(database)
            
            if schema_type == 'overview':
                return await self._get_database_overview(db, database)
            elif schema_type == 'tables':
                return await self._get_tables_info(db, database)
            elif schema_type == 'procedures':
                return await self._get_procedures_info(db, database)
            elif schema_type == 'triggers':
                return await self._get_triggers_info(db, database)
            elif schema_type == 'views':
                return await self._get_views_info(db, database)
            elif schema_type == 'relationships':
                return await self._get_relationships_info(db, database)
            else:
                return {
                    "success": False,
                    "error": f"Invalid schema type: {schema_type}"
                }
                
        except Exception as e:
            logger.error(f"Schema analysis error: {e}")
            return {
                "success": False,
                "error": f"Schema analysis failed: {str(e)}"
            }
    
    async def get_tables(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get list of tables.
        
        Args:
            args: Tool arguments
            
        Returns:
            Dictionary with table information
        """
        try:
            database = args.get('database')
            include_views = args.get('include_views', False)
            
            db = self._get_database(database)
            
            if include_views:
                # Get both tables and views
                tables = db.get_tables()
                views = db.get_views()
                
                return {
                    "success": True,
                    "tables": tables,
                    "views": views,
                    "total_tables": len(tables),
                    "total_views": len(views),
                    "database": database
                }
            else:
                tables = db.get_tables()
                return {
                    "success": True,
                    "tables": tables,
                    "total_tables": len(tables),
                    "database": database
                }
                
        except Exception as e:
            logger.error(f"Get tables error: {e}")
            return {
                "success": False,
                "error": f"Get tables failed: {str(e)}"
            }
    
    async def get_table_schema(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get detailed table schema.
        
        Args:
            args: Tool arguments
            
        Returns:
            Dictionary with table schema information
        """
        try:
            database = args.get('database')
            table_name = args.get('table_name')
            schema_name = args.get('schema_name', 'dbo')
            include_indexes = args.get('include_indexes', True)
            include_foreign_keys = args.get('include_foreign_keys', True)
            
            db = self._get_database(database)
            
            # Get basic table schema
            columns = db.get_table_schema(table_name, schema_name)
            primary_keys = db.get_primary_keys(table_name, schema_name)
            
            result = {
                "success": True,
                "table_name": table_name,
                "schema_name": schema_name,
                "columns": columns,
                "primary_keys": primary_keys,
                "database": database
            }
            
            # Add indexes if requested
            if include_indexes:
                indexes = db.get_indexes(table_name, schema_name)
                result["indexes"] = indexes
            
            # Add foreign keys if requested
            if include_foreign_keys:
                foreign_keys = db.get_foreign_keys(table_name, schema_name)
                result["foreign_keys"] = foreign_keys
            
            # Add table statistics
            try:
                row_count = db.get_table_row_count(table_name, schema_name)
                result["row_count"] = row_count
            except Exception as e:
                logger.warning(f"Could not get row count for {table_name}: {e}")
                result["row_count"] = None
            
            return result
            
        except Exception as e:
            logger.error(f"Get table schema error: {e}")
            return {
                "success": False,
                "error": f"Get table schema failed: {str(e)}"
            }
    
    async def get_stored_procedures(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get stored procedures information.
        
        Args:
            args: Tool arguments
            
        Returns:
            Dictionary with stored procedures information
        """
        try:
            database = args.get('database')
            include_definition = args.get('include_definition', False)
            
            db = self._get_database(database)
            procedures = db.get_stored_procedures()
            
            result = {
                "success": True,
                "procedures": procedures,
                "total_procedures": len(procedures),
                "database": database
            }
            
            if include_definition:
                procedures_with_definitions = []
                for proc in procedures:
                    proc_name = proc['routine_name']
                    proc_schema = proc['routine_schema']
                    definition = db.get_stored_procedure_definition(proc_name, proc_schema)
                    parameters = db.get_stored_procedure_parameters(proc_name, proc_schema)
                    
                    procedures_with_definitions.append({
                        **proc,
                        "definition": definition,
                        "parameters": parameters
                    })
                
                result["procedures"] = procedures_with_definitions
            
            return result
            
        except Exception as e:
            logger.error(f"Get stored procedures error: {e}")
            return {
                "success": False,
                "error": f"Get stored procedures failed: {str(e)}"
            }
    
    async def get_triggers(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get triggers information.
        
        Args:
            args: Tool arguments
            
        Returns:
            Dictionary with triggers information
        """
        try:
            database = args.get('database')
            include_definition = args.get('include_definition', False)
            
            db = self._get_database(database)
            triggers = db.get_triggers()
            
            result = {
                "success": True,
                "triggers": triggers,
                "total_triggers": len(triggers),
                "database": database
            }
            
            if include_definition:
                triggers_with_definitions = []
                for trigger in triggers:
                    trigger_name = trigger['trigger_name']
                    definition = db.get_trigger_definition(trigger_name)
                    
                    triggers_with_definitions.append({
                        **trigger,
                        "definition": definition
                    })
                
                result["triggers"] = triggers_with_definitions
            
            return result
            
        except Exception as e:
            logger.error(f"Get triggers error: {e}")
            return {
                "success": False,
                "error": f"Get triggers failed: {str(e)}"
            }
    
    async def get_views(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get views information.
        
        Args:
            args: Tool arguments
            
        Returns:
            Dictionary with views information
        """
        try:
            database = args.get('database')
            include_definition = args.get('include_definition', False)
            
            db = self._get_database(database)
            views = db.get_views()
            
            result = {
                "success": True,
                "views": views,
                "total_views": len(views),
                "database": database
            }
            
            if include_definition:
                views_with_definitions = []
                for view in views:
                    view_name = view['table_name']
                    view_schema = view['table_schema']
                    definition = db.get_view_definition(view_name, view_schema)
                    
                    views_with_definitions.append({
                        **view,
                        "definition": definition
                    })
                
                result["views"] = views_with_definitions
            
            return result
            
        except Exception as e:
            logger.error(f"Get views error: {e}")
            return {
                "success": False,
                "error": f"Get views failed: {str(e)}"
            }
    
    async def _get_database_overview(self, db, database: str) -> Dict[str, Any]:
        """Get database overview information."""
        try:
            # Get basic database info
            db_info = db.get_database_info()
            
            # Get counts
            tables = db.get_tables()
            procedures = db.get_stored_procedures()
            triggers = db.get_triggers()
            views = db.get_views()
            
            return {
                "success": True,
                "database_info": db_info,
                "summary": {
                    "total_tables": len(tables),
                    "total_procedures": len(procedures),
                    "total_triggers": len(triggers),
                    "total_views": len(views)
                },
                "database": database
            }
        except Exception as e:
            logger.error(f"Database overview error: {e}")
            return {
                "success": False,
                "error": f"Database overview failed: {str(e)}"
            }
    
    async def _get_tables_info(self, db, database: str) -> Dict[str, Any]:
        """Get detailed tables information."""
        try:
            tables = db.get_tables()
            
            # Get additional info for each table
            tables_with_info = []
            for table in tables:
                table_name = table['table_name']
                schema_name = table['table_schema']
                
                try:
                    row_count = db.get_table_row_count(table_name, schema_name)
                    table['row_count'] = row_count
                except:
                    table['row_count'] = None
                
                tables_with_info.append(table)
            
            return {
                "success": True,
                "tables": tables_with_info,
                "total_tables": len(tables_with_info),
                "database": database
            }
        except Exception as e:
            logger.error(f"Tables info error: {e}")
            return {
                "success": False,
                "error": f"Tables info failed: {str(e)}"
            }
    
    async def _get_procedures_info(self, db, database: str) -> Dict[str, Any]:
        """Get detailed procedures information."""
        try:
            procedures = db.get_stored_procedures()
            return {
                "success": True,
                "procedures": procedures,
                "total_procedures": len(procedures),
                "database": database
            }
        except Exception as e:
            logger.error(f"Procedures info error: {e}")
            return {
                "success": False,
                "error": f"Procedures info failed: {str(e)}"
            }
    
    async def _get_triggers_info(self, db, database: str) -> Dict[str, Any]:
        """Get detailed triggers information."""
        try:
            triggers = db.get_triggers()
            return {
                "success": True,
                "triggers": triggers,
                "total_triggers": len(triggers),
                "database": database
            }
        except Exception as e:
            logger.error(f"Triggers info error: {e}")
            return {
                "success": False,
                "error": f"Triggers info failed: {str(e)}"
            }
    
    async def _get_views_info(self, db, database: str) -> Dict[str, Any]:
        """Get detailed views information."""
        try:
            views = db.get_views()
            return {
                "success": True,
                "views": views,
                "total_views": len(views),
                "database": database
            }
        except Exception as e:
            logger.error(f"Views info error: {e}")
            return {
                "success": False,
                "error": f"Views info failed: {str(e)}"
            }
    
    async def _get_relationships_info(self, db, database: str) -> Dict[str, Any]:
        """Get database relationships information."""
        try:
            tables = db.get_tables()
            relationships = []
            
            for table in tables:
                table_name = table['table_name']
                schema_name = table['table_schema']
                
                foreign_keys = db.get_foreign_keys(table_name, schema_name)
                if foreign_keys:
                    relationships.append({
                        "table": f"{schema_name}.{table_name}",
                        "foreign_keys": foreign_keys
                    })
            
            return {
                "success": True,
                "relationships": relationships,
                "total_relationships": len(relationships),
                "database": database
            }
        except Exception as e:
            logger.error(f"Relationships info error: {e}")
            return {
                "success": False,
                "error": f"Relationships info failed: {str(e)}"
            }
