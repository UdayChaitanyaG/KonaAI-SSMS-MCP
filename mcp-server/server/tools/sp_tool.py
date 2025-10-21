"""
Stored procedure execution tool for MCP server.
Provides safe execution of stored procedures with parameter support.
"""

import logging
import re
import time
from typing import Any, Dict, List, Optional

from mcp.types import Tool
from ..database.master_db import MasterDatabase
from ..database.datamgmt_db import DataManagementDatabase


logger = logging.getLogger(__name__)


class StoredProcedureTool:
    """
    Tool for executing stored procedures with parameter validation.
    """
    
    def __init__(self, master_db: MasterDatabase, data_mgmt_db: DataManagementDatabase):
        """
        Initialize stored procedure tool.
        
        Args:
            master_db: Master database connection
            data_mgmt_db: Data Management database connection
        """
        self.master_db = master_db
        self.data_mgmt_db = data_mgmt_db
    
    def get_tool(self) -> Tool:
        """
        Get the stored procedure execution tool definition.
        
        Returns:
            MCP Tool definition for stored procedure execution
        """
        return Tool(
            name="execute_procedure",
            description="Execute stored procedures with input/output parameter support",
            inputSchema={
                "type": "object",
                "properties": {
                    "database": {
                        "type": "string",
                        "enum": ["master", "datamgmt"],
                        "description": "Database to execute procedure on"
                    },
                    "procedure_name": {
                        "type": "string",
                        "description": "Name of the stored procedure"
                    },
                    "schema": {
                        "type": "string",
                        "description": "Schema name (default: 'dbo')",
                        "default": "dbo"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Input parameters for the procedure",
                        "additionalProperties": True
                    },
                    "output_parameters": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of output parameter names to retrieve"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Execution timeout in seconds (default: 30)",
                        "default": 30
                    }
                },
                "required": ["database", "procedure_name"]
            }
        )
    
    def get_procedure_info_tool(self) -> Tool:
        """
        Get the procedure information tool definition.
        
        Returns:
            MCP Tool definition for procedure information
        """
        return Tool(
            name="get_procedure_info",
            description="Get information about a stored procedure including parameters",
            inputSchema={
                "type": "object",
                "properties": {
                    "database": {
                        "type": "string",
                        "enum": ["master", "datamgmt"],
                        "description": "Database to query"
                    },
                    "procedure_name": {
                        "type": "string",
                        "description": "Name of the stored procedure"
                    },
                    "schema": {
                        "type": "string",
                        "description": "Schema name (default: 'dbo')",
                        "default": "dbo"
                    },
                    "include_definition": {
                        "type": "boolean",
                        "description": "Include procedure definition",
                        "default": True
                    }
                },
                "required": ["database", "procedure_name"]
            }
        )
    
    def _validate_procedure_name(self, procedure_name: str) -> bool:
        """
        Validate stored procedure name for security.
        
        Args:
            procedure_name: Procedure name to validate
            
        Returns:
            True if procedure name is safe, False otherwise
        """
        # Check for dangerous patterns
        dangerous_patterns = [
            ';', '--', '/*', '*/', 'xp_', 'sp_executesql', 'exec', 'execute',
            'union', 'select', 'insert', 'update', 'delete', 'drop',
            'alter', 'create', 'grant', 'revoke', 'deny', 'openrowset',
            'opendatasource', 'bulk', 'bcp'
        ]
        
        proc_lower = procedure_name.lower()
        for pattern in dangerous_patterns:
            if pattern in proc_lower:
                logger.warning(f"Dangerous pattern in procedure name: {pattern}")
                return False
        
        # Check for valid procedure name format
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', procedure_name):
            logger.warning(f"Invalid procedure name format: {procedure_name}")
            return False
        
        return True
    
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
    
    async def execute_procedure(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a stored procedure.
        
        Args:
            args: Tool arguments containing procedure details and parameters
            
        Returns:
            Dictionary with procedure execution results
        """
        try:
            database = args.get('database')
            procedure_name = args.get('procedure_name', '').strip()
            schema = args.get('schema', 'dbo').strip()
            parameters = args.get('parameters', {})
            output_parameters = args.get('output_parameters', [])
            timeout = args.get('timeout', 30)
            
            if not procedure_name:
                return {
                    "success": False,
                    "error": "Procedure name is required"
                }
            
            # Validate procedure name
            if not self._validate_procedure_name(procedure_name):
                return {
                    "success": False,
                    "error": "Invalid procedure name"
                }
            
            # Get appropriate database connection
            db = self._get_database(database)
            
            # Build full procedure name
            full_procedure_name = f"{schema}.{procedure_name}"
            
            # Execute procedure
            start_time = time.time()
            
            try:
                result = db.execute_procedure(
                    full_procedure_name,
                    parameters,
                    output_parameters
                )
                
                execution_time = time.time() - start_time
                
                return {
                    "success": True,
                    "procedure_name": full_procedure_name,
                    "result_sets": result.get("result_sets", []),
                    "output_parameters": result.get("output_parameters", {}),
                    "execution_time": round(execution_time, 3),
                    "database": database,
                    "parameters_used": parameters
                }
                
            except Exception as proc_error:
                execution_time = time.time() - start_time
                logger.error(f"Procedure execution error: {proc_error}")
                
                return {
                    "success": False,
                    "error": f"Procedure execution failed: {str(proc_error)}",
                    "procedure_name": full_procedure_name,
                    "execution_time": round(execution_time, 3),
                    "database": database
                }
                
        except Exception as e:
            logger.error(f"Stored procedure tool error: {e}")
            return {
                "success": False,
                "error": f"Stored procedure execution failed: {str(e)}",
                "database": args.get('database', 'unknown')
            }
    
    async def get_procedure_info(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get information about a stored procedure.
        
        Args:
            args: Tool arguments containing procedure details
            
        Returns:
            Dictionary with procedure information
        """
        try:
            database = args.get('database')
            procedure_name = args.get('procedure_name', '').strip()
            schema = args.get('schema', 'dbo').strip()
            include_definition = args.get('include_definition', True)
            
            if not procedure_name:
                return {
                    "success": False,
                    "error": "Procedure name is required"
                }
            
            # Validate procedure name
            if not self._validate_procedure_name(procedure_name):
                return {
                    "success": False,
                    "error": "Invalid procedure name"
                }
            
            # Get appropriate database connection
            db = self._get_database(database)
            
            # Get procedure information
            try:
                # Get procedure parameters
                parameters = db.get_stored_procedure_parameters(procedure_name, schema)
                
                result = {
                    "success": True,
                    "procedure_name": f"{schema}.{procedure_name}",
                    "parameters": parameters,
                    "parameter_count": len(parameters),
                    "database": database
                }
                
                # Add definition if requested
                if include_definition:
                    definition = db.get_stored_procedure_definition(procedure_name, schema)
                    result["definition"] = definition
                
                # Categorize parameters
                input_params = [p for p in parameters if p.get('parameter_mode', '').upper() == 'IN']
                output_params = [p for p in parameters if p.get('parameter_mode', '').upper() == 'OUT']
                inout_params = [p for p in parameters if p.get('parameter_mode', '').upper() == 'INOUT']
                
                result["parameter_summary"] = {
                    "input_parameters": len(input_params),
                    "output_parameters": len(output_params),
                    "inout_parameters": len(inout_params)
                }
                
                return result
                
            except Exception as info_error:
                logger.error(f"Procedure info error: {info_error}")
                return {
                    "success": False,
                    "error": f"Could not retrieve procedure information: {str(info_error)}",
                    "procedure_name": f"{schema}.{procedure_name}",
                    "database": database
                }
                
        except Exception as e:
            logger.error(f"Get procedure info error: {e}")
            return {
                "success": False,
                "error": f"Get procedure info failed: {str(e)}",
                "database": args.get('database', 'unknown')
            }
    
    def get_procedure_examples(self) -> List[Dict[str, Any]]:
        """
        Get example stored procedure calls.
        
        Returns:
            List of example procedure calls with descriptions
        """
        return [
            {
                "description": "Execute a simple procedure without parameters",
                "procedure_name": "sp_helpdb",
                "schema": "dbo",
                "parameters": {},
                "database": "master"
            },
            {
                "description": "Execute a procedure with input parameters",
                "procedure_name": "sp_help",
                "schema": "dbo",
                "parameters": {
                    "objname": "YourTableName"
                },
                "database": "master"
            },
            {
                "description": "Execute a procedure with output parameters",
                "procedure_name": "sp_spaceused",
                "schema": "dbo",
                "parameters": {
                    "objname": "YourTableName"
                },
                "output_parameters": ["reserved", "data", "index_size", "unused"],
                "database": "master"
            },
            {
                "description": "Execute a custom business procedure",
                "procedure_name": "GetClientProjects",
                "schema": "dbo",
                "parameters": {
                    "ClientId": "12345",
                    "Status": "Active"
                },
                "database": "datamgmt"
            }
        ]
    
    def get_common_procedures(self, database: str) -> List[Dict[str, str]]:
        """
        Get list of common system procedures for a database.
        
        Args:
            database: Database name ('master' or 'datamgmt')
            
        Returns:
            List of common procedures with descriptions
        """
        common_procedures = {
            "master": [
                {
                    "name": "sp_helpdb",
                    "description": "Display information about databases",
                    "parameters": {}
                },
                {
                    "name": "sp_help",
                    "description": "Display information about database objects",
                    "parameters": {"objname": "object_name"}
                },
                {
                    "name": "sp_spaceused",
                    "description": "Display space usage information",
                    "parameters": {"objname": "object_name"}
                },
                {
                    "name": "sp_who",
                    "description": "Display current user and process information",
                    "parameters": {}
                },
                {
                    "name": "sp_lock",
                    "description": "Display lock information",
                    "parameters": {}
                }
            ],
            "datamgmt": [
                {
                    "name": "sp_help",
                    "description": "Display information about database objects",
                    "parameters": {"objname": "object_name"}
                },
                {
                    "name": "sp_spaceused",
                    "description": "Display space usage information",
                    "parameters": {"objname": "object_name"}
                }
            ]
        }
        
        return common_procedures.get(database, [])
