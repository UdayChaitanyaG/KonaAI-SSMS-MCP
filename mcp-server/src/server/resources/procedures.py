"""
Stored procedures resource provider for MCP server.
Provides read-only access to stored procedure metadata and definitions.
"""

import logging
from typing import Any, Dict, List, Optional

from mcp.types import Resource
from ..database.master_db import MasterDatabase
from ..database.datamgmt_db import DataManagementDatabase


logger = logging.getLogger(__name__)


class ProceduresResource:
    """
    Resource provider for stored procedures.
    """
    
    def __init__(self, master_db: MasterDatabase, data_mgmt_db: DataManagementDatabase):
        """
        Initialize procedures resource.
        
        Args:
            master_db: Master database connection
            data_mgmt_db: Data Management database connection
        """
        self.master_db = master_db
        self.data_mgmt_db = data_mgmt_db
    
    def get_resources(self) -> List[Resource]:
        """
        Get list of stored procedure resources for both databases.
        
        Returns:
            List of MCP Resource objects
        """
        resources = []
        
        # Get Master database procedures
        try:
            logger.info("Fetching Master database stored procedures for resources...")
            master_procedures = self.master_db.get_stored_procedures()
            logger.info(f"Found {len(master_procedures)} stored procedures in Master database")
            
            for proc in master_procedures:
                proc_name = proc.get('routine_name', '')
                schema_name = proc.get('routine_schema', 'dbo')
                if proc_name:
                    uri = f"ssms://master/procedures/{schema_name}/{proc_name}"
                    
                    resources.append(Resource(
                        uri=uri,
                        name=f"Master Procedure: {schema_name}.{proc_name}",
                        description=f"Stored procedure definition and metadata for {schema_name}.{proc_name} in Master database",
                        mimeType="application/json"
                    ))
        except Exception as e:
            logger.error(f"Error getting Master database procedure resources: {e}", exc_info=True)
            # Add a resource indicating the error
            resources.append(Resource(
                uri="ssms://master/procedures/error",
                name="Master Database Procedures (Error)",
                description=f"Error loading Master database procedures: {str(e)}",
                mimeType="text/plain"
            ))
        
        # Get Data Management database procedures
        try:
            logger.info("Fetching Data Management database stored procedures for resources...")
            data_mgmt_procedures = self.data_mgmt_db.get_stored_procedures()
            logger.info(f"Found {len(data_mgmt_procedures)} stored procedures in Data Management database")
            
            for proc in data_mgmt_procedures:
                proc_name = proc.get('routine_name', '')
                schema_name = proc.get('routine_schema', 'dbo')
                if proc_name:
                    uri = f"ssms://datamgmt/procedures/{schema_name}/{proc_name}"
                    
                    resources.append(Resource(
                        uri=uri,
                        name=f"Data Management Procedure: {schema_name}.{proc_name}",
                        description=f"Stored procedure definition and metadata for {schema_name}.{proc_name} in Data Management database",
                        mimeType="application/json"
                    ))
        except Exception as e:
            logger.error(f"Error getting Data Management database procedure resources: {e}", exc_info=True)
            # Add a resource indicating the error
            resources.append(Resource(
                uri="ssms://datamgmt/procedures/error",
                name="Data Management Database Procedures (Error)",
                description=f"Error loading Data Management database procedures: {str(e)}",
                mimeType="text/plain"
            ))
        
        logger.info(f"Returning {len(resources)} procedure resources")
        return resources
    
    async def get_procedure_resource(self, uri: str) -> Dict[str, Any]:
        """
        Get detailed stored procedure resource content.
        
        Args:
            uri: Resource URI in format ssms://{database}/procedures/{schema}/{procedure}
            
        Returns:
            Dictionary with procedure resource content
        """
        try:
            # Parse URI
            parts = uri.split('/')
            if len(parts) < 5 or parts[0] != 'ssms:' or parts[1] != '' or parts[2] != 'procedures':
                return {
                    "error": "Invalid procedure resource URI format",
                    "expected_format": "ssms://{database}/procedures/{schema}/{procedure}"
                }
            
            database = parts[3]
            schema_name = parts[4]
            proc_name = parts[5] if len(parts) > 5 else None
            
            if not proc_name:
                return {
                    "error": "Procedure name is required in URI"
                }
            
            # Get appropriate database connection
            if database == 'master':
                db = self.master_db
            elif database == 'datamgmt':
                db = self.data_mgmt_db
            else:
                return {
                    "error": f"Invalid database: {database}. Must be 'master' or 'datamgmt'"
                }
            
            # Get comprehensive procedure information
            procedure_info = {
                "database": database,
                "procedure_name": proc_name,
                "schema_name": schema_name,
                "full_name": f"{schema_name}.{proc_name}"
            }
            
            # Get procedure definition
            try:
                definition = db.get_stored_procedure_definition(proc_name, schema_name)
                procedure_info["definition"] = definition
            except Exception as e:
                logger.warning(f"Could not get procedure definition for {proc_name}: {e}")
                procedure_info["definition"] = ""
            
            # Get procedure parameters
            try:
                parameters = db.get_stored_procedure_parameters(proc_name, schema_name)
                procedure_info["parameters"] = parameters
                procedure_info["parameter_count"] = len(parameters)
                
                # Categorize parameters
                input_params = [p for p in parameters if p.get('parameter_mode', '').upper() == 'IN']
                output_params = [p for p in parameters if p.get('parameter_mode', '').upper() == 'OUT']
                inout_params = [p for p in parameters if p.get('parameter_mode', '').upper() == 'INOUT']
                
                procedure_info["parameter_summary"] = {
                    "input_parameters": len(input_params),
                    "output_parameters": len(output_params),
                    "inout_parameters": len(inout_params)
                }
                
            except Exception as e:
                logger.warning(f"Could not get procedure parameters for {proc_name}: {e}")
                procedure_info["parameters"] = []
                procedure_info["parameter_count"] = 0
                procedure_info["parameter_summary"] = {
                    "input_parameters": 0,
                    "output_parameters": 0,
                    "inout_parameters": 0
                }
            
            return {
                "success": True,
                "resource_type": "stored_procedure",
                "procedure_info": procedure_info
            }
            
        except Exception as e:
            logger.error(f"Error getting procedure resource: {e}")
            return {
                "success": False,
                "error": f"Failed to get procedure resource: {str(e)}",
                "uri": uri
            }
    
    def get_procedure_list(self, database: str) -> List[Dict[str, Any]]:
        """
        Get list of stored procedures for a specific database.
        
        Args:
            database: Database name ('master' or 'datamgmt')
            
        Returns:
            List of procedure information
        """
        try:
            if database == 'master':
                return self.master_db.get_stored_procedures()
            elif database == 'datamgmt':
                return self.data_mgmt_db.get_stored_procedures()
            else:
                return []
        except Exception as e:
            logger.error(f"Error getting procedure list for {database}: {e}")
            return []
    
    def get_procedure_summary(self, database: str) -> Dict[str, Any]:
        """
        Get summary of stored procedures for a database.
        
        Args:
            database: Database name ('master' or 'datamgmt')
            
        Returns:
            Dictionary with procedure summary information
        """
        try:
            procedures = self.get_procedure_list(database)
            
            # Group by schema
            schemas = {}
            for proc in procedures:
                schema_name = proc['routine_schema']
                if schema_name not in schemas:
                    schemas[schema_name] = []
                schemas[schema_name].append(proc['routine_name'])
            
            return {
                "database": database,
                "total_procedures": len(procedures),
                "schemas": schemas,
                "schema_count": len(schemas)
            }
            
        except Exception as e:
            logger.error(f"Error getting procedure summary for {database}: {e}")
            return {
                "database": database,
                "error": str(e)
            }
