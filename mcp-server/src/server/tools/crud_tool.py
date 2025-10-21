"""
CRUD operations tool for MCP server.
Provides safe INSERT, UPDATE, and DELETE operations with parameterized queries.
"""

import logging
import re
import time
from typing import Any, Dict, List, Optional

from mcp.types import Tool
from ..database.master_db import MasterDatabase
from ..database.datamgmt_db import DataManagementDatabase


logger = logging.getLogger(__name__)


class CrudTool:
    """
    Tool for performing CRUD operations with security validation.
    """
    
    def __init__(self, master_db: MasterDatabase, data_mgmt_db: DataManagementDatabase):
        """
        Initialize CRUD tool.
        
        Args:
            master_db: Master database connection
            data_mgmt_db: Data Management database connection
        """
        self.master_db = master_db
        self.data_mgmt_db = data_mgmt_db
    
    def get_insert_tool(self) -> Tool:
        """
        Get the INSERT tool definition.
        
        Returns:
            MCP Tool definition for INSERT operations
        """
        return Tool(
            name="insert_data",
            description="Insert data into a table with parameterized queries",
            inputSchema={
                "type": "object",
                "properties": {
                    "database": {
                        "type": "string",
                        "enum": ["master", "datamgmt"],
                        "description": "Database to insert into"
                    },
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table"
                    },
                    "schema": {
                        "type": "string",
                        "description": "Schema name (default: 'dbo')",
                        "default": "dbo"
                    },
                    "data": {
                        "type": "object",
                        "description": "Data to insert as key-value pairs",
                        "additionalProperties": True
                    },
                    "return_id": {
                        "type": "boolean",
                        "description": "Whether to return the inserted ID (if applicable)",
                        "default": False
                    }
                },
                "required": ["database", "table_name", "data"]
            }
        )
    
    def get_update_tool(self) -> Tool:
        """
        Get the UPDATE tool definition.
        
        Returns:
            MCP Tool definition for UPDATE operations
        """
        return Tool(
            name="update_data",
            description="Update data in a table with parameterized queries",
            inputSchema={
                "type": "object",
                "properties": {
                    "database": {
                        "type": "string",
                        "enum": ["master", "datamgmt"],
                        "description": "Database to update"
                    },
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table"
                    },
                    "schema": {
                        "type": "string",
                        "description": "Schema name (default: 'dbo')",
                        "default": "dbo"
                    },
                    "data": {
                        "type": "object",
                        "description": "Data to update as key-value pairs",
                        "additionalProperties": True
                    },
                    "where_clause": {
                        "type": "string",
                        "description": "WHERE clause for the update (use parameters for values)"
                    },
                    "where_parameters": {
                        "type": "object",
                        "description": "Parameters for the WHERE clause",
                        "additionalProperties": True
                    }
                },
                "required": ["database", "table_name", "data", "where_clause"]
            }
        )
    
    def get_delete_tool(self) -> Tool:
        """
        Get the DELETE tool definition.
        
        Returns:
            MCP Tool definition for DELETE operations
        """
        return Tool(
            name="delete_data",
            description="Delete data from a table with parameterized queries",
            inputSchema={
                "type": "object",
                "properties": {
                    "database": {
                        "type": "string",
                        "enum": ["master", "datamgmt"],
                        "description": "Database to delete from"
                    },
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table"
                    },
                    "schema": {
                        "type": "string",
                        "description": "Schema name (default: 'dbo')",
                        "default": "dbo"
                    },
                    "where_clause": {
                        "type": "string",
                        "description": "WHERE clause for the delete (use parameters for values)"
                    },
                    "where_parameters": {
                        "type": "object",
                        "description": "Parameters for the WHERE clause",
                        "additionalProperties": True
                    },
                    "confirm_delete": {
                        "type": "boolean",
                        "description": "Confirmation flag for delete operations",
                        "default": False
                    }
                },
                "required": ["database", "table_name", "where_clause"]
            }
        )
    
    def _validate_table_name(self, table_name: str) -> bool:
        """
        Validate table name for security.
        
        Args:
            table_name: Table name to validate
            
        Returns:
            True if table name is safe, False otherwise
        """
        # Check for SQL injection patterns
        dangerous_patterns = [
            ';', '--', '/*', '*/', 'xp_', 'sp_', 'exec', 'execute',
            'union', 'select', 'insert', 'update', 'delete', 'drop',
            'alter', 'create', 'grant', 'revoke', 'deny'
        ]
        
        table_lower = table_name.lower()
        for pattern in dangerous_patterns:
            if pattern in table_lower:
                logger.warning(f"Dangerous pattern in table name: {pattern}")
                return False
        
        # Check for valid table name format
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table_name):
            logger.warning(f"Invalid table name format: {table_name}")
            return False
        
        return True
    
    def _validate_where_clause(self, where_clause: str) -> bool:
        """
        Validate WHERE clause for security.
        
        Args:
            where_clause: WHERE clause to validate
            
        Returns:
            True if WHERE clause is safe, False otherwise
        """
        # Check for dangerous patterns
        dangerous_patterns = [
            ';', '--', '/*', '*/', 'xp_', 'sp_', 'exec', 'execute',
            'union', 'select', 'insert', 'update', 'delete', 'drop',
            'alter', 'create', 'grant', 'revoke', 'deny', 'or 1=1',
            'and 1=1', 'or true', 'and true'
        ]
        
        where_lower = where_clause.lower()
        for pattern in dangerous_patterns:
            if pattern in where_lower:
                logger.warning(f"Dangerous pattern in WHERE clause: {pattern}")
                return False
        
        return True
    
    async def insert(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert data into a table.
        
        Args:
            args: Tool arguments containing database, table, and data
            
        Returns:
            Dictionary with insert results
        """
        try:
            database = args.get('database')
            table_name = args.get('table_name', '').strip()
            schema = args.get('schema', 'dbo').strip()
            data = args.get('data', {})
            return_id = args.get('return_id', False)
            
            if not table_name:
                return {
                    "success": False,
                    "error": "Table name is required"
                }
            
            if not data:
                return {
                    "success": False,
                    "error": "Data to insert is required"
                }
            
            # Validate table name
            if not self._validate_table_name(table_name):
                return {
                    "success": False,
                    "error": "Invalid table name"
                }
            
            # Get appropriate database connection
            if database == 'master':
                db = self.master_db
            elif database == 'datamgmt':
                db = self.data_mgmt_db
            else:
                return {
                    "success": False,
                    "error": f"Invalid database: {database}. Must be 'master' or 'datamgmt'"
                }
            
            # Build INSERT query
            columns = list(data.keys())
            placeholders = [f"@{col}" for col in columns]
            
            query = f"INSERT INTO [{schema}].[{table_name}] ({', '.join([f'[{col}]' for col in columns])}) VALUES ({', '.join(placeholders)})"
            
            # Add RETURNING clause if requested
            if return_id:
                query += "; SELECT SCOPE_IDENTITY() as inserted_id"
            
            # Execute insert
            start_time = time.time()
            
            if return_id:
                result = db.execute_query(query, data, fetch=True)
                inserted_id = result[0]['inserted_id'] if result else None
            else:
                affected_rows = db.execute_query(query, data, fetch=False)
                inserted_id = None
            
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "affected_rows": 1,
                "inserted_id": inserted_id,
                "execution_time": round(execution_time, 3),
                "table": f"{schema}.{table_name}",
                "database": database
            }
            
        except Exception as e:
            logger.error(f"Insert operation error: {e}")
            return {
                "success": False,
                "error": f"Insert operation failed: {str(e)}",
                "database": args.get('database', 'unknown')
            }
    
    async def update(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update data in a table.
        
        Args:
            args: Tool arguments containing database, table, data, and WHERE clause
            
        Returns:
            Dictionary with update results
        """
        try:
            database = args.get('database')
            table_name = args.get('table_name', '').strip()
            schema = args.get('schema', 'dbo').strip()
            data = args.get('data', {})
            where_clause = args.get('where_clause', '').strip()
            where_parameters = args.get('where_parameters', {})
            
            if not table_name:
                return {
                    "success": False,
                    "error": "Table name is required"
                }
            
            if not data:
                return {
                    "success": False,
                    "error": "Data to update is required"
                }
            
            if not where_clause:
                return {
                    "success": False,
                    "error": "WHERE clause is required for update operations"
                }
            
            # Validate table name and WHERE clause
            if not self._validate_table_name(table_name):
                return {
                    "success": False,
                    "error": "Invalid table name"
                }
            
            if not self._validate_where_clause(where_clause):
                return {
                    "success": False,
                    "error": "Invalid WHERE clause"
                }
            
            # Get appropriate database connection
            if database == 'master':
                db = self.master_db
            elif database == 'datamgmt':
                db = self.data_mgmt_db
            else:
                return {
                    "success": False,
                    "error": f"Invalid database: {database}. Must be 'master' or 'datamgmt'"
                }
            
            # Build UPDATE query
            set_clause = ', '.join([f"[{col}] = @{col}" for col in data.keys()])
            query = f"UPDATE [{schema}].[{table_name}] SET {set_clause} WHERE {where_clause}"
            
            # Combine parameters
            all_parameters = {**data, **where_parameters}
            
            # Execute update
            start_time = time.time()
            affected_rows = db.execute_query(query, all_parameters, fetch=False)
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "affected_rows": affected_rows,
                "execution_time": round(execution_time, 3),
                "table": f"{schema}.{table_name}",
                "database": database
            }
            
        except Exception as e:
            logger.error(f"Update operation error: {e}")
            return {
                "success": False,
                "error": f"Update operation failed: {str(e)}",
                "database": args.get('database', 'unknown')
            }
    
    async def delete(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete data from a table.
        
        Args:
            args: Tool arguments containing database, table, and WHERE clause
            
        Returns:
            Dictionary with delete results
        """
        try:
            database = args.get('database')
            table_name = args.get('table_name', '').strip()
            schema = args.get('schema', 'dbo').strip()
            where_clause = args.get('where_clause', '').strip()
            where_parameters = args.get('where_parameters', {})
            confirm_delete = args.get('confirm_delete', False)
            
            if not table_name:
                return {
                    "success": False,
                    "error": "Table name is required"
                }
            
            if not where_clause:
                return {
                    "success": False,
                    "error": "WHERE clause is required for delete operations"
                }
            
            if not confirm_delete:
                return {
                    "success": False,
                    "error": "Delete operations require confirmation. Set 'confirm_delete' to true."
                }
            
            # Validate table name and WHERE clause
            if not self._validate_table_name(table_name):
                return {
                    "success": False,
                    "error": "Invalid table name"
                }
            
            if not self._validate_where_clause(where_clause):
                return {
                    "success": False,
                    "error": "Invalid WHERE clause"
                }
            
            # Get appropriate database connection
            if database == 'master':
                db = self.master_db
            elif database == 'datamgmt':
                db = self.data_mgmt_db
            else:
                return {
                    "success": False,
                    "error": f"Invalid database: {database}. Must be 'master' or 'datamgmt'"
                }
            
            # Build DELETE query
            query = f"DELETE FROM [{schema}].[{table_name}] WHERE {where_clause}"
            
            # Execute delete
            start_time = time.time()
            affected_rows = db.execute_query(query, where_parameters, fetch=False)
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "affected_rows": affected_rows,
                "execution_time": round(execution_time, 3),
                "table": f"{schema}.{table_name}",
                "database": database
            }
            
        except Exception as e:
            logger.error(f"Delete operation error: {e}")
            return {
                "success": False,
                "error": f"Delete operation failed: {str(e)}",
                "database": args.get('database', 'unknown')
            }
