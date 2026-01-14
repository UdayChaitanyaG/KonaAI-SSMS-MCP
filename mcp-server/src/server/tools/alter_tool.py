"""
ALTER operations tool for MCP server.
Provides safe ALTER TABLE, ALTER COLUMN, and other schema modification operations.
"""

import logging
import re
import time
from typing import Any, Dict, List, Optional

from mcp.types import Tool
from ..database.master_db import MasterDatabase
from ..database.datamgmt_db import DataManagementDatabase


logger = logging.getLogger(__name__)


class AlterTool:
    """
    Tool for performing ALTER operations with security validation.
    """
    
    def __init__(self, master_db: MasterDatabase, data_mgmt_db: DataManagementDatabase):
        """
        Initialize ALTER tool.
        
        Args:
            master_db: Master database connection
            data_mgmt_db: Data Management database connection
        """
        self.master_db = master_db
        self.data_mgmt_db = data_mgmt_db
    
    def get_alter_table_tool(self) -> Tool:
        """
        Get the ALTER TABLE tool definition.
        
        Returns:
            MCP Tool definition for ALTER TABLE operations
        """
        return Tool(
            name="alter_table",
            description="Alter table structure (add/drop columns, modify columns, add constraints, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "database": {
                        "type": "string",
                        "enum": ["master", "datamgmt"],
                        "description": "Database to alter"
                    },
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table to alter"
                    },
                    "schema": {
                        "type": "string",
                        "description": "Schema name (default: 'dbo')",
                        "default": "dbo"
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["add_column", "drop_column", "alter_column", "add_constraint", "drop_constraint", "rename_column", "rename_table"],
                        "description": "Type of ALTER operation to perform"
                    },
                    "column_name": {
                        "type": "string",
                        "description": "Column name (required for column operations)"
                    },
                    "new_column_name": {
                        "type": "string",
                        "description": "New column name (for rename operations)"
                    },
                    "data_type": {
                        "type": "string",
                        "description": "SQL Server data type (e.g., 'NVARCHAR(255)', 'INT', 'DATETIME2')"
                    },
                    "nullable": {
                        "type": "boolean",
                        "description": "Whether column allows NULL values",
                        "default": True
                    },
                    "default_value": {
                        "type": "string",
                        "description": "Default value for the column (SQL expression)"
                    },
                    "constraint_name": {
                        "type": "string",
                        "description": "Constraint name (for constraint operations)"
                    },
                    "constraint_type": {
                        "type": "string",
                        "enum": ["PRIMARY KEY", "FOREIGN KEY", "UNIQUE", "CHECK", "DEFAULT"],
                        "description": "Type of constraint to add"
                    },
                    "constraint_definition": {
                        "type": "string",
                        "description": "Constraint definition (e.g., 'CHECK (age > 0)', 'FOREIGN KEY (user_id) REFERENCES Users(id)')"
                    },
                    "new_table_name": {
                        "type": "string",
                        "description": "New table name (for rename_table operation)"
                    }
                },
                "required": ["database", "table_name", "operation"]
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
            'create', 'grant', 'revoke', 'deny'
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
    
    def _validate_column_name(self, column_name: str) -> bool:
        """
        Validate column name for security.
        
        Args:
            column_name: Column name to validate
            
        Returns:
            True if column name is safe, False otherwise
        """
        # Check for SQL injection patterns
        dangerous_patterns = [
            ';', '--', '/*', '*/', 'xp_', 'sp_', 'exec', 'execute',
            'union', 'select', 'insert', 'update', 'delete', 'drop',
            'alter', 'create', 'grant', 'revoke', 'deny'
        ]
        
        column_lower = column_name.lower()
        for pattern in dangerous_patterns:
            if pattern in column_lower:
                logger.warning(f"Dangerous pattern in column name: {pattern}")
                return False
        
        # Check for valid column name format
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', column_name):
            logger.warning(f"Invalid column name format: {column_name}")
            return False
        
        return True
    
    def _validate_data_type(self, data_type: str) -> bool:
        """
        Validate data type for security.
        
        Args:
            data_type: Data type to validate
            
        Returns:
            True if data type is safe, False otherwise
        """
        # Check for dangerous patterns
        dangerous_patterns = [
            ';', '--', '/*', '*/', 'xp_', 'sp_', 'exec', 'execute',
            'union', 'select', 'insert', 'update', 'delete', 'drop',
            'create', 'grant', 'revoke', 'deny'
        ]
        
        data_type_lower = data_type.lower()
        for pattern in dangerous_patterns:
            if pattern in data_type_lower:
                logger.warning(f"Dangerous pattern in data type: {pattern}")
                return False
        
        # Allow common SQL Server data types
        valid_types = [
            'int', 'bigint', 'smallint', 'tinyint', 'bit',
            'decimal', 'numeric', 'float', 'real', 'money', 'smallmoney',
            'char', 'varchar', 'nchar', 'nvarchar', 'text', 'ntext',
            'date', 'time', 'datetime', 'datetime2', 'smalldatetime', 'datetimeoffset',
            'binary', 'varbinary', 'image',
            'uniqueidentifier', 'xml', 'sql_variant', 'timestamp'
        ]
        
        # Extract base type (before parentheses)
        base_type = data_type_lower.split('(')[0].strip()
        if base_type not in valid_types:
            logger.warning(f"Unrecognized data type: {data_type}")
            return False
        
        return True
    
    async def alter_table(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform ALTER TABLE operation.
        
        Args:
            args: Tool arguments containing database, table, and operation details
            
        Returns:
            Dictionary with ALTER operation results
        """
        try:
            database = args.get('database')
            table_name = args.get('table_name', '').strip()
            schema = args.get('schema', 'dbo').strip()
            operation = args.get('operation', '').lower()
            
            if not table_name:
                return {
                    "success": False,
                    "error": "Table name is required"
                }
            
            if not operation:
                return {
                    "success": False,
                    "error": "Operation is required"
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
            
            # Build and execute ALTER statement based on operation
            start_time = time.time()
            
            if operation == 'add_column':
                result = await self._add_column(db, schema, table_name, args)
            elif operation == 'drop_column':
                result = await self._drop_column(db, schema, table_name, args)
            elif operation == 'alter_column':
                result = await self._alter_column(db, schema, table_name, args)
            elif operation == 'add_constraint':
                result = await self._add_constraint(db, schema, table_name, args)
            elif operation == 'drop_constraint':
                result = await self._drop_constraint(db, schema, table_name, args)
            elif operation == 'rename_column':
                result = await self._rename_column(db, schema, table_name, args)
            elif operation == 'rename_table':
                result = await self._rename_table(db, schema, table_name, args)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported operation: {operation}"
                }
            
            execution_time = time.time() - start_time
            
            if result.get('success'):
                result['execution_time'] = round(execution_time, 3)
                result['table'] = f"{schema}.{table_name}"
                result['database'] = database
            
            return result
            
        except Exception as e:
            logger.error(f"ALTER TABLE operation error: {e}", exc_info=True)
            return {
                "success": False,
                "error": f"ALTER TABLE operation failed: {str(e)}",
                "database": args.get('database', 'unknown')
            }
    
    async def _add_column(self, db, schema: str, table_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Add a column to a table."""
        column_name = args.get('column_name', '').strip()
        data_type = args.get('data_type', '').strip()
        nullable = args.get('nullable', True)
        default_value = args.get('default_value')
        
        if not column_name:
            return {"success": False, "error": "Column name is required for add_column operation"}
        
        if not data_type:
            return {"success": False, "error": "Data type is required for add_column operation"}
        
        if not self._validate_column_name(column_name):
            return {"success": False, "error": "Invalid column name"}
        
        if not self._validate_data_type(data_type):
            return {"success": False, "error": "Invalid data type"}
        
        # Build ALTER TABLE ADD COLUMN statement
        null_clause = "NULL" if nullable else "NOT NULL"
        query = f"ALTER TABLE [{schema}].[{table_name}] ADD [{column_name}] {data_type} {null_clause}"
        
        if default_value:
            query += f" DEFAULT {default_value}"
        
        try:
            db.execute_query(query, {}, fetch=False)
            return {
                "success": True,
                "operation": "add_column",
                "column_name": column_name,
                "message": f"Column '{column_name}' added successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to add column: {str(e)}"
            }
    
    async def _drop_column(self, db, schema: str, table_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Drop a column from a table."""
        column_name = args.get('column_name', '').strip()
        
        if not column_name:
            return {"success": False, "error": "Column name is required for drop_column operation"}
        
        if not self._validate_column_name(column_name):
            return {"success": False, "error": "Invalid column name"}
        
        # Build ALTER TABLE DROP COLUMN statement
        query = f"ALTER TABLE [{schema}].[{table_name}] DROP COLUMN [{column_name}]"
        
        try:
            db.execute_query(query, {}, fetch=False)
            return {
                "success": True,
                "operation": "drop_column",
                "column_name": column_name,
                "message": f"Column '{column_name}' dropped successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to drop column: {str(e)}"
            }
    
    async def _alter_column(self, db, schema: str, table_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Alter a column in a table."""
        column_name = args.get('column_name', '').strip()
        data_type = args.get('data_type', '').strip()
        nullable = args.get('nullable')
        default_value = args.get('default_value')
        
        if not column_name:
            return {"success": False, "error": "Column name is required for alter_column operation"}
        
        if not self._validate_column_name(column_name):
            return {"success": False, "error": "Invalid column name"}
        
        # Build ALTER TABLE ALTER COLUMN statement
        if data_type:
            if not self._validate_data_type(data_type):
                return {"success": False, "error": "Invalid data type"}
            
            null_clause = ""
            if nullable is not None:
                null_clause = "NULL" if nullable else "NOT NULL"
            
            query = f"ALTER TABLE [{schema}].[{table_name}] ALTER COLUMN [{column_name}] {data_type}"
            if null_clause:
                query += f" {null_clause}"
        else:
            # Only changing nullability
            if nullable is None:
                return {"success": False, "error": "Either data_type or nullable must be specified"}
            
            # Get current data type first
            try:
                columns = db.get_table_schema(table_name, schema)
                current_col = next((c for c in columns if c.get('column_name') == column_name), None)
                if not current_col:
                    return {"success": False, "error": f"Column '{column_name}' not found"}
                
                current_type = current_col.get('data_type', '')
                null_clause = "NULL" if nullable else "NOT NULL"
                query = f"ALTER TABLE [{schema}].[{table_name}] ALTER COLUMN [{column_name}] {current_type} {null_clause}"
            except Exception as e:
                return {"success": False, "error": f"Failed to get current column definition: {str(e)}"}
        
        try:
            db.execute_query(query, {}, fetch=False)
            
            # Handle default value separately if provided
            if default_value:
                # Drop existing default if any
                try:
                    db.execute_query(f"ALTER TABLE [{schema}].[{table_name}] DROP CONSTRAINT IF EXISTS DF_{table_name}_{column_name}", {}, fetch=False)
                except:
                    pass
                
                # Add new default
                try:
                    default_query = f"ALTER TABLE [{schema}].[{table_name}] ADD CONSTRAINT DF_{table_name}_{column_name} DEFAULT {default_value} FOR [{column_name}]"
                    db.execute_query(default_query, {}, fetch=False)
                except Exception as e:
                    logger.warning(f"Failed to set default value: {e}")
            
            return {
                "success": True,
                "operation": "alter_column",
                "column_name": column_name,
                "message": f"Column '{column_name}' altered successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to alter column: {str(e)}"
            }
    
    async def _add_constraint(self, db, schema: str, table_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Add a constraint to a table."""
        constraint_name = args.get('constraint_name', '').strip()
        constraint_type = args.get('constraint_type', '').strip()
        constraint_definition = args.get('constraint_definition', '').strip()
        
        if not constraint_name:
            return {"success": False, "error": "Constraint name is required for add_constraint operation"}
        
        if not constraint_type:
            return {"success": False, "error": "Constraint type is required for add_constraint operation"}
        
        if not self._validate_table_name(constraint_name):
            return {"success": False, "error": "Invalid constraint name"}
        
        # Build ALTER TABLE ADD CONSTRAINT statement
        if constraint_type == "FOREIGN KEY" or constraint_type == "CHECK":
            if not constraint_definition:
                return {"success": False, "error": f"Constraint definition is required for {constraint_type}"}
            query = f"ALTER TABLE [{schema}].[{table_name}] ADD CONSTRAINT [{constraint_name}] {constraint_type} {constraint_definition}"
        elif constraint_type == "PRIMARY KEY" or constraint_type == "UNIQUE":
            if not constraint_definition:
                return {"success": False, "error": f"Constraint definition is required for {constraint_type} (e.g., '(column_name)')"}
            query = f"ALTER TABLE [{schema}].[{table_name}] ADD CONSTRAINT [{constraint_name}] {constraint_type} {constraint_definition}"
        elif constraint_type == "DEFAULT":
            if not constraint_definition:
                return {"success": False, "error": "Default value is required for DEFAULT constraint (e.g., 'FOR column_name DEFAULT value')"}
            query = f"ALTER TABLE [{schema}].[{table_name}] ADD CONSTRAINT [{constraint_name}] DEFAULT {constraint_definition}"
        else:
            return {"success": False, "error": f"Unsupported constraint type: {constraint_type}"}
        
        try:
            db.execute_query(query, {}, fetch=False)
            return {
                "success": True,
                "operation": "add_constraint",
                "constraint_name": constraint_name,
                "constraint_type": constraint_type,
                "message": f"Constraint '{constraint_name}' added successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to add constraint: {str(e)}"
            }
    
    async def _drop_constraint(self, db, schema: str, table_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Drop a constraint from a table."""
        constraint_name = args.get('constraint_name', '').strip()
        
        if not constraint_name:
            return {"success": False, "error": "Constraint name is required for drop_constraint operation"}
        
        # Build ALTER TABLE DROP CONSTRAINT statement
        query = f"ALTER TABLE [{schema}].[{table_name}] DROP CONSTRAINT [{constraint_name}]"
        
        try:
            db.execute_query(query, {}, fetch=False)
            return {
                "success": True,
                "operation": "drop_constraint",
                "constraint_name": constraint_name,
                "message": f"Constraint '{constraint_name}' dropped successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to drop constraint: {str(e)}"
            }
    
    async def _rename_column(self, db, schema: str, table_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Rename a column in a table."""
        column_name = args.get('column_name', '').strip()
        new_column_name = args.get('new_column_name', '').strip()
        
        if not column_name:
            return {"success": False, "error": "Column name is required for rename_column operation"}
        
        if not new_column_name:
            return {"success": False, "error": "New column name is required for rename_column operation"}
        
        if not self._validate_column_name(column_name):
            return {"success": False, "error": "Invalid column name"}
        
        if not self._validate_column_name(new_column_name):
            return {"success": False, "error": "Invalid new column name"}
        
        # SQL Server uses sp_rename for renaming columns
        query = f"EXEC sp_rename '{schema}.{table_name}.{column_name}', '{new_column_name}', 'COLUMN'"
        
        try:
            db.execute_query(query, {}, fetch=False)
            return {
                "success": True,
                "operation": "rename_column",
                "old_column_name": column_name,
                "new_column_name": new_column_name,
                "message": f"Column '{column_name}' renamed to '{new_column_name}' successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to rename column: {str(e)}"
            }
    
    async def _rename_table(self, db, schema: str, table_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Rename a table."""
        new_table_name = args.get('new_table_name', '').strip()
        
        if not new_table_name:
            return {"success": False, "error": "New table name is required for rename_table operation"}
        
        if not self._validate_table_name(new_table_name):
            return {"success": False, "error": "Invalid new table name"}
        
        # SQL Server uses sp_rename for renaming tables
        query = f"EXEC sp_rename '{schema}.{table_name}', '{new_table_name}'"
        
        try:
            db.execute_query(query, {}, fetch=False)
            return {
                "success": True,
                "operation": "rename_table",
                "old_table_name": table_name,
                "new_table_name": new_table_name,
                "message": f"Table '{schema}.{table_name}' renamed to '{schema}.{new_table_name}' successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to rename table: {str(e)}"
            }
