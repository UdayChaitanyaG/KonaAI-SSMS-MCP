#!/usr/bin/env python3
"""
Database Connections Testing Script
Tests database connections and basic operations.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_dir))

# Import centralized configuration
from config.app_config import setup_environment

# Set up environment variables
setup_environment()

# Import database classes
from server.database.master_db import MasterDatabase
from server.database.datamgmt_db import DataManagementDatabase
from config.database_config import AppConfig

def test_database_connections():
    """Test database connections and basic operations."""
    print("Database Connections Testing")
    print("=" * 30)
    
    try:
        # Initialize configuration
        config = AppConfig()
        print("OK Configuration loaded")
        
        # Test Master Database
        print("\nTesting Master Database:")
        try:
            master_db = MasterDatabase(config.get_master_db_config())
            tables = master_db.get_tables()
            print(f"OK Master database connected")
            print(f"   Tables found: {len(tables)}")
            
            # Test a simple query
            if tables:
                first_table = tables[0]
                table_name = first_table['table_name']
                schema_name = first_table['table_schema']
                print(f"   Testing query on {schema_name}.{table_name}")
                
                # Test basic query
                result = master_db.execute_query(f"SELECT TOP 1 * FROM [{schema_name}].[{table_name}]")
                print(f"   Query successful: {len(result)} rows returned")
        except Exception as e:
            print(f"ERROR Master database failed: {str(e)}")
        
        # Test Data Management Database
        print("\nTesting Data Management Database:")
        try:
            datamgmt_db = DataManagementDatabase(config.get_data_mgmt_db_config())
            tables = datamgmt_db.get_tables()
            print(f"OK Data Management database connected")
            print(f"   Tables found: {len(tables)}")
            
            # Test a simple query
            if tables:
                first_table = tables[0]
                table_name = first_table['table_name']
                schema_name = first_table['table_schema']
                print(f"   Testing query on {schema_name}.{table_name}")
                
                # Test basic query
                result = datamgmt_db.execute_query(f"SELECT TOP 1 * FROM [{schema_name}].[{table_name}]")
                print(f"   Query successful: {len(result)} rows returned")
        except Exception as e:
            print(f"ERROR Data Management database failed: {str(e)}")
        
        print("\nDatabase connections testing completed!")
        return True
        
    except Exception as e:
        print(f"Error testing database connections: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_database_connections()
    sys.exit(0 if success else 1)
