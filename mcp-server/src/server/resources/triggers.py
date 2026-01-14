"""
Triggers resource provider for MCP server.
Provides read-only access to trigger metadata and definitions.
"""

import logging
from typing import Any, Dict, List, Optional

from mcp.types import Resource
from ..database.master_db import MasterDatabase
from ..database.datamgmt_db import DataManagementDatabase


logger = logging.getLogger(__name__)


class TriggersResource:
    """
    Resource provider for database triggers.
    """
    
    def __init__(self, master_db: MasterDatabase, data_mgmt_db: DataManagementDatabase):
        """
        Initialize triggers resource.
        
        Args:
            master_db: Master database connection
            data_mgmt_db: Data Management database connection
        """
        self.master_db = master_db
        self.data_mgmt_db = data_mgmt_db
    
    def get_resources(self) -> List[Resource]:
        """
        Get list of trigger resources for both databases.
        
        Returns:
            List of MCP Resource objects
        """
        resources = []
        
        # Get Master database triggers
        try:
            logger.info("Fetching Master database triggers for resources...")
            master_triggers = self.master_db.get_triggers()
            logger.info(f"Found {len(master_triggers)} triggers in Master database")
            
            for trigger in master_triggers:
                trigger_name = trigger.get('trigger_name', '')
                if trigger_name:
                    uri = f"ssms://master/triggers/{trigger_name}"
                    
                    resources.append(Resource(
                        uri=uri,
                        name=f"Master Trigger: {trigger_name}",
                        description=f"Trigger definition and metadata for {trigger_name} in Master database",
                        mimeType="application/json"
                    ))
        except Exception as e:
            logger.error(f"Error getting Master database trigger resources: {e}", exc_info=True)
            # Add a resource indicating the error
            resources.append(Resource(
                uri="ssms://master/triggers/error",
                name="Master Database Triggers (Error)",
                description=f"Error loading Master database triggers: {str(e)}",
                mimeType="text/plain"
            ))
        
        # Get Data Management database triggers
        try:
            logger.info("Fetching Data Management database triggers for resources...")
            data_mgmt_triggers = self.data_mgmt_db.get_triggers()
            logger.info(f"Found {len(data_mgmt_triggers)} triggers in Data Management database")
            
            for trigger in data_mgmt_triggers:
                trigger_name = trigger.get('trigger_name', '')
                if trigger_name:
                    uri = f"ssms://datamgmt/triggers/{trigger_name}"
                    
                    resources.append(Resource(
                        uri=uri,
                        name=f"Data Management Trigger: {trigger_name}",
                        description=f"Trigger definition and metadata for {trigger_name} in Data Management database",
                        mimeType="application/json"
                    ))
        except Exception as e:
            logger.error(f"Error getting Data Management database trigger resources: {e}", exc_info=True)
            # Add a resource indicating the error
            resources.append(Resource(
                uri="ssms://datamgmt/triggers/error",
                name="Data Management Database Triggers (Error)",
                description=f"Error loading Data Management database triggers: {str(e)}",
                mimeType="text/plain"
            ))
        
        logger.info(f"Returning {len(resources)} trigger resources")
        return resources
    
    async def get_trigger_resource(self, uri: str) -> Dict[str, Any]:
        """
        Get detailed trigger resource content.
        
        Args:
            uri: Resource URI in format ssms://{database}/triggers/{trigger}
            
        Returns:
            Dictionary with trigger resource content
        """
        try:
            # Parse URI
            parts = uri.split('/')
            if len(parts) < 4 or parts[0] != 'ssms:' or parts[1] != '' or parts[2] != 'triggers':
                return {
                    "error": "Invalid trigger resource URI format",
                    "expected_format": "ssms://{database}/triggers/{trigger}"
                }
            
            database = parts[3]
            trigger_name = parts[4] if len(parts) > 4 else None
            
            if not trigger_name:
                return {
                    "error": "Trigger name is required in URI"
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
            
            # Get comprehensive trigger information
            trigger_info = {
                "database": database,
                "trigger_name": trigger_name
            }
            
            # Get trigger definition
            try:
                definition = db.get_trigger_definition(trigger_name)
                trigger_info["definition"] = definition
            except Exception as e:
                logger.warning(f"Could not get trigger definition for {trigger_name}: {e}")
                trigger_info["definition"] = ""
            
            # Get trigger metadata
            try:
                triggers = db.get_triggers()
                trigger_metadata = next(
                    (t for t in triggers if t['trigger_name'] == trigger_name), 
                    None
                )
                
                if trigger_metadata:
                    trigger_info.update({
                        "table_name": trigger_metadata.get('table_name'),
                        "trigger_schema": trigger_metadata.get('trigger_schema'),
                        "is_disabled": trigger_metadata.get('is_disabled', False),
                        "is_not_for_replication": trigger_metadata.get('is_not_for_replication', False)
                    })
                else:
                    trigger_info.update({
                        "table_name": None,
                        "trigger_schema": None,
                        "is_disabled": None,
                        "is_not_for_replication": None
                    })
                    
            except Exception as e:
                logger.warning(f"Could not get trigger metadata for {trigger_name}: {e}")
                trigger_info.update({
                    "table_name": None,
                    "trigger_schema": None,
                    "is_disabled": None,
                    "is_not_for_replication": None
                })
            
            return {
                "success": True,
                "resource_type": "trigger",
                "trigger_info": trigger_info
            }
            
        except Exception as e:
            logger.error(f"Error getting trigger resource: {e}")
            return {
                "success": False,
                "error": f"Failed to get trigger resource: {str(e)}",
                "uri": uri
            }
    
    def get_trigger_list(self, database: str) -> List[Dict[str, Any]]:
        """
        Get list of triggers for a specific database.
        
        Args:
            database: Database name ('master' or 'datamgmt')
            
        Returns:
            List of trigger information
        """
        try:
            if database == 'master':
                return self.master_db.get_triggers()
            elif database == 'datamgmt':
                return self.data_mgmt_db.get_triggers()
            else:
                return []
        except Exception as e:
            logger.error(f"Error getting trigger list for {database}: {e}")
            return []
    
    def get_trigger_summary(self, database: str) -> Dict[str, Any]:
        """
        Get summary of triggers for a database.
        
        Args:
            database: Database name ('master' or 'datamgmt')
            
        Returns:
            Dictionary with trigger summary information
        """
        try:
            triggers = self.get_trigger_list(database)
            
            # Group by table
            tables = {}
            disabled_count = 0
            replication_count = 0
            
            for trigger in triggers:
                table_name = trigger.get('table_name', 'Unknown')
                if table_name not in tables:
                    tables[table_name] = []
                tables[table_name].append(trigger['trigger_name'])
                
                if trigger.get('is_disabled', False):
                    disabled_count += 1
                if trigger.get('is_not_for_replication', False):
                    replication_count += 1
            
            return {
                "database": database,
                "total_triggers": len(triggers),
                "tables": tables,
                "table_count": len(tables),
                "disabled_triggers": disabled_count,
                "replication_triggers": replication_count
            }
            
        except Exception as e:
            logger.error(f"Error getting trigger summary for {database}: {e}")
            return {
                "database": database,
                "error": str(e)
            }
