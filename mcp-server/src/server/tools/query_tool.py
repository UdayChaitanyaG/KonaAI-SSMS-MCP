"""
Query execution tool for MCP server.
Provides safe SQL query execution with parameterized queries.
"""

import logging
import re
import time
from typing import Any, Dict, List, Optional, Union

from mcp.types import Tool
from ..database.master_db import MasterDatabase
from ..database.datamgmt_db import DataManagementDatabase


logger = logging.getLogger(__name__)


class QueryTool:
    """
    Tool for executing SQL queries with security validation.
    """
    
    def __init__(self, master_db: MasterDatabase, data_mgmt_db: DataManagementDatabase):
        """
        Initialize query tool.
        
        Args:
            master_db: Master database connection
            data_mgmt_db: Data Management database connection
        """
        self.master_db = master_db
        self.data_mgmt_db = data_mgmt_db
        
        # Allowed SQL keywords for security validation
        self.allowed_keywords = {
            'select', 'insert', 'update', 'delete', 'exec', 'execute',
            'with', 'from', 'where', 'order', 'group', 'having',
            'join', 'inner', 'left', 'right', 'outer', 'cross',
            'union', 'except', 'intersect', 'case', 'when', 'then',
            'else', 'end', 'as', 'and', 'or', 'not', 'in', 'exists',
            'between', 'like', 'is', 'null', 'top', 'distinct',
            'count', 'sum', 'avg', 'min', 'max', 'cast', 'convert'
        }
        
        # Dangerous keywords to block
        self.blocked_keywords = {
            'drop', 'truncate', 'alter', 'create', 'grant', 'revoke',
            'deny', 'backup', 'restore', 'shutdown', 'kill', 'sp_',
            'xp_', 'openrowset', 'opendatasource', 'bulk', 'bcp'
        }
    
    def get_tool(self) -> Tool:
        """
        Get the MCP tool definition.
        
        Returns:
            MCP Tool definition
        """
        return Tool(
            name="execute_query",
            description="Execute SQL queries on the specified database with security validation",
            inputSchema={
                "type": "object",
                "properties": {
                    "database": {
                        "type": "string",
                        "enum": ["master", "datamgmt"],
                        "description": "Database to execute query on"
                    },
                    "query": {
                        "type": "string",
                        "description": "SQL query to execute"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Query parameters (optional)",
                        "additionalProperties": True
                    },
                    "max_rows": {
                        "type": "integer",
                        "description": "Maximum number of rows to return (default: 1000)",
                        "default": 1000
                    }
                },
                "required": ["database", "query"]
            }
        )
    
    def _validate_query(self, query: str) -> bool:
        """
        Validate SQL query for security.
        
        Args:
            query: SQL query to validate
            
        Returns:
            True if query is safe, False otherwise
        """
        # Convert to lowercase for keyword checking
        query_lower = query.lower().strip()
        
        # Check for blocked keywords
        for blocked in self.blocked_keywords:
            if blocked in query_lower:
                logger.warning(f"Blocked keyword detected: {blocked}")
                return False
        
        # Check if query starts with allowed keywords
        first_word = query_lower.split()[0] if query_lower.split() else ""
        if first_word not in self.allowed_keywords:
            logger.warning(f"Query does not start with allowed keyword: {first_word}")
            return False
        
        # Additional security checks
        dangerous_patterns = [
            r'--',  # SQL comments
            r'/\*.*\*/',  # Block comments
            r'union.*select',  # Union-based injection
            r'exec\s*\(',  # Dynamic execution
            r'sp_executesql',  # Stored procedure execution
            r'xp_cmdshell',  # Extended procedure
            r'openrowset',  # Ad hoc queries
            r'opendatasource'  # Ad hoc queries
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, query_lower, re.IGNORECASE):
                logger.warning(f"Dangerous pattern detected: {pattern}")
                return False
        
        return True
    
    def _apply_row_limit(self, query: str, max_rows: int) -> str:
        """
        Apply row limit to SELECT queries.
        
        Args:
            query: Original SQL query
            max_rows: Maximum number of rows to return
            
        Returns:
            Modified query with row limit
        """
        query_lower = query.lower().strip()
        
        # Only apply to SELECT queries
        if not query_lower.startswith('select'):
            return query
        
        # Check if TOP is already specified
        if 'top ' in query_lower:
            return query
        
        # Add TOP clause
        if 'select' in query_lower:
            # Replace first SELECT with SELECT TOP
            modified_query = re.sub(
                r'^select\s+',
                f'SELECT TOP {max_rows} ',
                query,
                flags=re.IGNORECASE,
                count=1
            )
            return modified_query
        
        return query
    
    async def execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute SQL query.
        
        Args:
            args: Tool arguments containing database, query, and parameters
            
        Returns:
            Dictionary with query results and metadata
        """
        try:
            database = args.get('database')
            query = args.get('query', '').strip()
            parameters = args.get('parameters', {})
            max_rows = args.get('max_rows', 1000)
            
            if not query:
                return {
                    "success": False,
                    "error": "Query cannot be empty"
                }
            
            # Validate query for security
            if not self._validate_query(query):
                return {
                    "success": False,
                    "error": "Query contains potentially dangerous SQL. Only SELECT, INSERT, UPDATE, DELETE, and EXEC statements are allowed."
                }
            
            # Apply row limit to SELECT queries
            if max_rows and max_rows > 0:
                query = self._apply_row_limit(query, max_rows)
            
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
            
            # Execute query
            start_time = time.time()
            
            # Determine if this is a SELECT query (for fetching results)
            is_select = query.strip().lower().startswith('select')
            
            if is_select:
                results = db.execute_query(query, parameters, fetch=True)
                execution_time = time.time() - start_time
                
                return {
                    "success": True,
                    "data": results,
                    "row_count": len(results) if isinstance(results, list) else 0,
                    "execution_time": round(execution_time, 3),
                    "database": database,
                    "query": query
                }
            else:
                # For INSERT, UPDATE, DELETE, EXEC
                affected_rows = db.execute_query(query, parameters, fetch=False)
                execution_time = time.time() - start_time
                
                return {
                    "success": True,
                    "affected_rows": affected_rows,
                    "execution_time": round(execution_time, 3),
                    "database": database,
                    "query": query
                }
                
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            return {
                "success": False,
                "error": f"Query execution failed: {str(e)}",
                "database": args.get('database', 'unknown')
            }
    
    def get_query_examples(self) -> List[Dict[str, str]]:
        """
        Get example queries for different operations.
        
        Returns:
            List of example queries with descriptions
        """
        return [
            {
                "description": "Get all tables in Master database",
                "query": "SELECT TABLE_NAME, TABLE_SCHEMA FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'",
                "database": "master"
            },
            {
                "description": "Get table schema for a specific table",
                "query": "SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'YourTableName'",
                "database": "master"
            },
            {
                "description": "Get recent file uploads",
                "query": "SELECT TOP 10 FileName, FileSize, UploadedOn FROM File_Detail WHERE IsActive = 1 ORDER BY UploadedOn DESC",
                "database": "datamgmt"
            },
            {
                "description": "Get client projects",
                "query": "SELECT ProjectName, ClientId, ProjectStatus, StartDate FROM ClientProject WHERE IsActive = 1",
                "database": "datamgmt"
            },
            {
                "description": "Get stored procedures",
                "query": "SELECT ROUTINE_NAME, ROUTINE_SCHEMA FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_TYPE = 'PROCEDURE'",
                "database": "master"
            }
        ]
