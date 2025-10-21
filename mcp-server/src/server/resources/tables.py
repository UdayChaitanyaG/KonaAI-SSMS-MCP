"""
Tables resource provider for MCP server.
Provides read-only access to table metadata and schema information.
"""

import logging
from typing import Any, Dict, List, Optional

from mcp.types import Resource
from ..database.master_db import MasterDatabase
from ..database.datamgmt_db import DataManagementDatabase


logger = logging.getLogger(__name__)


class TablesResource:
    """
    Resource provider for database tables.
    """
    
    def __init__(self, master_db: MasterDatabase, data_mgmt_db: DataManagementDatabase):
        """
        Initialize tables resource.
        
        Args:
            master_db: Master database connection
            data_mgmt_db: Data Management database connection
        """
        self.master_db = master_db
        self.data_mgmt_db = data_mgmt_db
    
    def get_resources(self) -> List[Resource]:
        """
        Get list of table resources for both databases.
        
        Returns:
            List of MCP Resource objects
        """
        resources = []
        
        try:
            # Get Master database tables
            master_tables = self.master_db.get_tables()
            for table in master_tables:
                table_name = table['table_name']
                schema_name = table['table_schema']
                uri = f"ssms://master/tables/{schema_name}/{table_name}"
                
                resources.append(Resource(
                    uri=uri,
                    name=f"Master Table: {schema_name}.{table_name}",
                    description=f"Table schema and metadata for {schema_name}.{table_name} in Master database",
                    mimeType="application/json"
                ))
            
            # Get Data Management database tables
            data_mgmt_tables = self.data_mgmt_db.get_tables()
            for table in data_mgmt_tables:
                table_name = table['table_name']
                schema_name = table['table_schema']
                uri = f"ssms://datamgmt/tables/{schema_name}/{table_name}"
                
                resources.append(Resource(
                    uri=uri,
                    name=f"Data Management Table: {schema_name}.{table_name}",
                    description=f"Table schema and metadata for {schema_name}.{table_name} in Data Management database",
                    mimeType="application/json"
                ))
            
        except Exception as e:
            logger.error(f"Error getting table resources: {e}")
        
        return resources
    
    async def get_table_resource(self, uri: str) -> Dict[str, Any]:
        """
        Get detailed table resource content.
        
        Args:
            uri: Resource URI in format ssms://{database}/tables/{schema}/{table}
            
        Returns:
            Dictionary with table resource content
        """
        try:
            # Parse URI
            parts = uri.split('/')
            if len(parts) < 5 or parts[0] != 'ssms:' or parts[1] != '' or parts[2] != 'tables':
                return {
                    "error": "Invalid table resource URI format",
                    "expected_format": "ssms://{database}/tables/{schema}/{table}"
                }
            
            database = parts[3]
            schema_name = parts[4]
            table_name = parts[5] if len(parts) > 5 else None
            
            if not table_name:
                return {
                    "error": "Table name is required in URI"
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
            
            # Get comprehensive table information
            table_info = {
                "database": database,
                "table_name": table_name,
                "schema_name": schema_name,
                "full_name": f"{schema_name}.{table_name}"
            }
            
            # Get table schema
            try:
                columns = db.get_table_schema(table_name, schema_name)
                table_info["columns"] = columns
                table_info["column_count"] = len(columns)
            except Exception as e:
                logger.warning(f"Could not get table schema for {table_name}: {e}")
                table_info["columns"] = []
                table_info["column_count"] = 0
            
            # Get primary keys
            try:
                primary_keys = db.get_primary_keys(table_name, schema_name)
                table_info["primary_keys"] = primary_keys
            except Exception as e:
                logger.warning(f"Could not get primary keys for {table_name}: {e}")
                table_info["primary_keys"] = []
            
            # Get foreign keys
            try:
                foreign_keys = db.get_foreign_keys(table_name, schema_name)
                table_info["foreign_keys"] = foreign_keys
            except Exception as e:
                logger.warning(f"Could not get foreign keys for {table_name}: {e}")
                table_info["foreign_keys"] = []
            
            # Get indexes
            try:
                indexes = db.get_indexes(table_name, schema_name)
                table_info["indexes"] = indexes
            except Exception as e:
                logger.warning(f"Could not get indexes for {table_name}: {e}")
                table_info["indexes"] = []
            
            # Get row count
            try:
                row_count = db.get_table_row_count(table_name, schema_name)
                table_info["row_count"] = row_count
            except Exception as e:
                logger.warning(f"Could not get row count for {table_name}: {e}")
                table_info["row_count"] = None
            
            # Get sample data (first 5 rows)
            try:
                sample_data = db.get_table_data(table_name, schema_name, limit=5, offset=0)
                table_info["sample_data"] = sample_data
                table_info["sample_count"] = len(sample_data)
            except Exception as e:
                logger.warning(f"Could not get sample data for {table_name}: {e}")
                table_info["sample_data"] = []
                table_info["sample_count"] = 0
            
            return {
                "success": True,
                "resource_type": "table",
                "table_info": table_info
            }
            
        except Exception as e:
            logger.error(f"Error getting table resource: {e}")
            return {
                "success": False,
                "error": f"Failed to get table resource: {str(e)}",
                "uri": uri
            }
    
    def get_table_list(self, database: str) -> List[Dict[str, Any]]:
        """
        Get list of tables for a specific database.
        
        Args:
            database: Database name ('master' or 'datamgmt')
            
        Returns:
            List of table information
        """
        try:
            if database == 'master':
                return self.master_db.get_tables()
            elif database == 'datamgmt':
                return self.data_mgmt_db.get_tables()
            else:
                return []
        except Exception as e:
            logger.error(f"Error getting table list for {database}: {e}")
            return []
    
    def get_table_summary(self, database: str) -> Dict[str, Any]:
        """
        Get summary of tables for a database.
        
        Args:
            database: Database name ('master' or 'datamgmt')
            
        Returns:
            Dictionary with table summary information
        """
        try:
            tables = self.get_table_list(database)
            
            # Group by schema
            schemas = {}
            for table in tables:
                schema_name = table['table_schema']
                if schema_name not in schemas:
                    schemas[schema_name] = []
                schemas[schema_name].append(table['table_name'])
            
            return {
                "database": database,
                "total_tables": len(tables),
                "schemas": schemas,
                "schema_count": len(schemas)
            }
            
        except Exception as e:
            logger.error(f"Error getting table summary for {database}: {e}")
            return {
                "database": database,
                "error": str(e)
            }
