"""
Views resource provider for MCP server.
Provides read-only access to view metadata and definitions.
"""

import logging
from typing import Any, Dict, List, Optional

from mcp.types import Resource
from ..database.master_db import MasterDatabase
from ..database.datamgmt_db import DataManagementDatabase


logger = logging.getLogger(__name__)


class ViewsResource:
    """
    Resource provider for database views.
    """
    
    def __init__(self, master_db: MasterDatabase, data_mgmt_db: DataManagementDatabase):
        """
        Initialize views resource.
        
        Args:
            master_db: Master database connection
            data_mgmt_db: Data Management database connection
        """
        self.master_db = master_db
        self.data_mgmt_db = data_mgmt_db
    
    def get_resources(self) -> List[Resource]:
        """
        Get list of view resources for both databases.
        
        Returns:
            List of MCP Resource objects
        """
        resources = []
        
        try:
            # Get Master database views
            master_views = self.master_db.get_views()
            for view in master_views:
                view_name = view['table_name']
                schema_name = view['table_schema']
                uri = f"ssms://master/views/{schema_name}/{view_name}"
                
                resources.append(Resource(
                    uri=uri,
                    name=f"Master View: {schema_name}.{view_name}",
                    description=f"View definition and metadata for {schema_name}.{view_name} in Master database",
                    mimeType="application/json"
                ))
            
            # Get Data Management database views
            data_mgmt_views = self.data_mgmt_db.get_views()
            for view in data_mgmt_views:
                view_name = view['table_name']
                schema_name = view['table_schema']
                uri = f"ssms://datamgmt/views/{schema_name}/{view_name}"
                
                resources.append(Resource(
                    uri=uri,
                    name=f"Data Management View: {schema_name}.{view_name}",
                    description=f"View definition and metadata for {schema_name}.{view_name} in Data Management database",
                    mimeType="application/json"
                ))
            
        except Exception as e:
            logger.error(f"Error getting view resources: {e}")
        
        return resources
    
    async def get_view_resource(self, uri: str) -> Dict[str, Any]:
        """
        Get detailed view resource content.
        
        Args:
            uri: Resource URI in format ssms://{database}/views/{schema}/{view}
            
        Returns:
            Dictionary with view resource content
        """
        try:
            # Parse URI
            parts = uri.split('/')
            if len(parts) < 5 or parts[0] != 'ssms:' or parts[1] != '' or parts[2] != 'views':
                return {
                    "error": "Invalid view resource URI format",
                    "expected_format": "ssms://{database}/views/{schema}/{view}"
                }
            
            database = parts[3]
            schema_name = parts[4]
            view_name = parts[5] if len(parts) > 5 else None
            
            if not view_name:
                return {
                    "error": "View name is required in URI"
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
            
            # Get comprehensive view information
            view_info = {
                "database": database,
                "view_name": view_name,
                "schema_name": schema_name,
                "full_name": f"{schema_name}.{view_name}"
            }
            
            # Get view definition
            try:
                definition = db.get_view_definition(view_name, schema_name)
                view_info["definition"] = definition
            except Exception as e:
                logger.warning(f"Could not get view definition for {view_name}: {e}")
                view_info["definition"] = ""
            
            # Get view metadata
            try:
                views = db.get_views()
                view_metadata = next(
                    (v for v in views if v['table_name'] == view_name and v['table_schema'] == schema_name), 
                    None
                )
                
                if view_metadata:
                    view_info.update({
                        "view_definition": view_metadata.get('view_definition', ''),
                        "table_schema": view_metadata.get('table_schema'),
                        "table_name": view_metadata.get('table_name')
                    })
                else:
                    view_info.update({
                        "view_definition": "",
                        "table_schema": schema_name,
                        "table_name": view_name
                    })
                    
            except Exception as e:
                logger.warning(f"Could not get view metadata for {view_name}: {e}")
                view_info.update({
                    "view_definition": "",
                    "table_schema": schema_name,
                    "table_name": view_name
                })
            
            return {
                "success": True,
                "resource_type": "view",
                "view_info": view_info
            }
            
        except Exception as e:
            logger.error(f"Error getting view resource: {e}")
            return {
                "success": False,
                "error": f"Failed to get view resource: {str(e)}",
                "uri": uri
            }
    
    def get_view_list(self, database: str) -> List[Dict[str, Any]]:
        """
        Get list of views for a specific database.
        
        Args:
            database: Database name ('master' or 'datamgmt')
            
        Returns:
            List of view information
        """
        try:
            if database == 'master':
                return self.master_db.get_views()
            elif database == 'datamgmt':
                return self.data_mgmt_db.get_views()
            else:
                return []
        except Exception as e:
            logger.error(f"Error getting view list for {database}: {e}")
            return []
    
    def get_view_summary(self, database: str) -> Dict[str, Any]:
        """
        Get summary of views for a database.
        
        Args:
            database: Database name ('master' or 'datamgmt')
            
        Returns:
            Dictionary with view summary information
        """
        try:
            views = self.get_view_list(database)
            
            # Group by schema
            schemas = {}
            for view in views:
                schema_name = view['table_schema']
                if schema_name not in schemas:
                    schemas[schema_name] = []
                schemas[schema_name].append(view['table_name'])
            
            return {
                "database": database,
                "total_views": len(views),
                "schemas": schemas,
                "schema_count": len(schemas)
            }
            
        except Exception as e:
            logger.error(f"Error getting view summary for {database}: {e}")
            return {
                "database": database,
                "error": str(e)
            }
