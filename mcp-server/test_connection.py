#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Database Connection
Tests connection to both Master and Data Management databases.
"""

import sys
from pathlib import Path

# Add src to path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from config.database_config import AppConfig, get_connection_string
from server.database.master_db import MasterDatabase
from server.database.datamgmt_db import DataManagementDatabase


def test_connection():
    """Test database connections."""
    print("=" * 70)
    print("Database Connection Test")
    print("=" * 70)
    print()
    
    try:
        # Load configuration
        config = AppConfig()
        
        print("Configuration:")
        print(f"  Master DB Server: {config.master_db_server}")
        print(f"  Master DB Name: {config.master_db_name}")
        print(f"  Master DB User: {config.master_db_user}")
        print(f"  Data Mgmt DB Server: {config.data_mgmt_db_server}")
        print(f"  Data Mgmt DB Name: {config.data_mgmt_db_name}")
        print(f"  Data Mgmt DB User: {config.data_mgmt_db_user}")
        print()
        
        # Test Master Database
        print("Testing Master Database Connection...")
        print("-" * 70)
        master_config = config.get_master_db_config()
        master_db = MasterDatabase(master_config)
        
        try:
            tables = master_db.get_tables()
            print(f"[OK] Master Database connected successfully!")
            print(f"     Found {len(tables)} tables")
            if tables:
                print("     Sample tables:")
                for table in tables[:5]:
                    print(f"       - {table.get('table_schema', 'dbo')}.{table.get('table_name', 'N/A')}")
        except Exception as e:
            print(f"[ERROR] Master Database connection failed: {e}")
            return False
        finally:
            master_db.close_all_connections()
        
        print()
        
        # Test Data Management Database
        print("Testing Data Management Database Connection...")
        print("-" * 70)
        datamgmt_config = config.get_data_mgmt_db_config()
        datamgmt_db = DataManagementDatabase(datamgmt_config)
        
        try:
            tables = datamgmt_db.get_tables()
            print(f"[OK] Data Management Database connected successfully!")
            print(f"     Found {len(tables)} tables")
            if tables:
                print("     Sample tables:")
                for table in tables[:5]:
                    print(f"       - {table.get('table_schema', 'dbo')}.{table.get('table_name', 'N/A')}")
        except Exception as e:
            print(f"[ERROR] Data Management Database connection failed: {e}")
            return False
        finally:
            datamgmt_db.close_all_connections()
        
        print()
        print("=" * 70)
        print("[OK] All database connections successful!")
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"[ERROR] Configuration error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
