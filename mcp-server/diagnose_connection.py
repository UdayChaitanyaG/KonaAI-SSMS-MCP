#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Connection Diagnostics Tool
Helps diagnose SQL Server connection issues and find the correct server name format.
"""

import sys
import pyodbc
from pathlib import Path

# Add src to path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from config.database_config import AppConfig, normalize_server_name


def test_connection_format(server_name: str, database: str, username: str, password: str):
    """Test a specific server name format."""
    normalized = normalize_server_name(server_name)
    
    formats_to_try = [
        # Format 1: Direct with encryption
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={normalized};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
        f"Connection Timeout=5;",
        
        # Format 2: Without encryption
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={normalized};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Encrypt=no;"
        f"Connection Timeout=5;",
        
        # Format 3: With explicit port
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={normalized},1433;"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
        f"Connection Timeout=5;",
    ]
    
    for i, conn_str in enumerate(formats_to_try, 1):
        try:
            print(f"  Format {i}...", end=" ")
            conn = pyodbc.connect(conn_str, timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION, DB_NAME()")
            result = cursor.fetchone()
            conn.close()
            print("[OK] SUCCESS!")
            print(f"      SQL Server Version: {result[0][:60]}...")
            print(f"      Connected to Database: {result[1]}")
            print(f"      Working connection string:")
            print(f"      {conn_str}")
            return True, conn_str
        except pyodbc.Error as e:
            error_code = str(e).split("]")[0] if "]" in str(e) else ""
            print(f"[FAILED] {error_code}")
        except Exception as e:
            print(f"[ERROR] {str(e)[:60]}")
    
    return False, None


def suggest_server_formats(original_server: str):
    """Suggest alternative server name formats to try."""
    suggestions = []
    
    # If it looks like a version number, suggest it might be wrong
    if "." in original_server and len(original_server.split(".")) >= 3:
        parts = original_server.split(".")
        if all(p.isdigit() for p in parts):
            suggestions.append("This looks like a version number, not a server name!")
            suggestions.append("Common server name formats:")
            suggestions.append("  - IP Address: 192.168.1.100")
            suggestions.append("  - Hostname: SERVERNAME")
            suggestions.append("  - Named Instance: SERVERNAME\\INSTANCENAME")
            suggestions.append("  - With Port: SERVERNAME,1433")
    
    # Try common variations
    if "\\" not in original_server and "/" not in original_server:
        suggestions.append(f"Try as named instance: {original_server}\\MSSQLSERVER")
        suggestions.append(f"Try as named instance: {original_server}\\SQLEXPRESS")
    
    if "," not in original_server:
        suggestions.append(f"Try with port: {original_server},1433")
    
    return suggestions


def main():
    """Main diagnostic function."""
    print("=" * 70)
    print("SQL Server Connection Diagnostics")
    print("=" * 70)
    print()
    
    try:
        # Load configuration
        config = AppConfig()
        
        print("Current Configuration:")
        print("-" * 70)
        print(f"  Master DB Server: {config.master_db_server}")
        print(f"  Master DB Name: {config.master_db_name}")
        print(f"  Master DB User: {config.master_db_user}")
        print(f"  Data Mgmt DB Server: {config.data_mgmt_db_server}")
        print(f"  Data Mgmt DB Name: {config.data_mgmt_db_name}")
        print()
        
        # Test Master Database
        print("Testing Master Database Connection...")
        print("-" * 70)
        master_config = config.get_master_db_config()
        success, conn_str = test_connection_format(
            master_config.server,
            master_config.database,
            master_config.username,
            master_config.password
        )
        
        if not success:
            print("\n[WARN] Connection failed with current server name format")
            print("\nSuggestions:")
            suggestions = suggest_server_formats(master_config.server)
            for suggestion in suggestions:
                print(f"  - {suggestion}")
        
        print()
        
        # Test Data Management Database
        print("Testing Data Management Database Connection...")
        print("-" * 70)
        datamgmt_config = config.get_data_mgmt_db_config()
        success, conn_str = test_connection_format(
            datamgmt_config.server,
            datamgmt_config.database,
            datamgmt_config.username,
            datamgmt_config.password
        )
        
        if not success:
            print("\n[WARN] Connection failed with current server name format")
            print("\nSuggestions:")
            suggestions = suggest_server_formats(datamgmt_config.server)
            for suggestion in suggestions:
                print(f"  - {suggestion}")
        
        print()
        print("=" * 70)
        print("Diagnostics Complete")
        print("=" * 70)
        print()
        print("Next Steps:")
        print("1. If connection failed, check the suggestions above")
        print("2. Verify the actual server name/IP address")
        print("3. Update .env file with the correct server name")
        print("4. Ensure SQL Server is running and accessible")
        print("5. Check firewall and network settings")
        
    except Exception as e:
        print(f"\n[ERROR] Diagnostic error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
