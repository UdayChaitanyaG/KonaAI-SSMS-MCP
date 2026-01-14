#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Different Server Name Formats
Tests various SQL Server connection string formats to find the correct one.
"""

import pyodbc
import sys

# Test configurations
SERVER_CANDIDATES = [
    "17.0.1050.2",                    # Direct name/IP
    "17.0.1050.2,1433",               # With port
    "localhost\\17.0.1050.2",         # Named instance format
    "17.0.1050.2\\MSSQLSERVER",       # Default instance
    "17.0.1050.2\\SQLEXPRESS",        # Express instance
    "tcp:17.0.1050.2,1433",          # TCP protocol
    "(local)\\17.0.1050.2",           # Local named instance
]

DATABASE = "KonaAI_Master"
USERNAME = "SSMSLOGIN"
PASSWORD = "LoginPassword123"


def test_connection(server_name: str):
    """Test a connection string format."""
    connection_strings = [
        # Format 1: With UID/PWD
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server_name};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
        f"Connection Timeout=5;",
        
        # Format 2: Without encryption (for testing)
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server_name};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        f"Encrypt=no;"
        f"Connection Timeout=5;",
        
        # Format 3: With port explicitly
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server_name};"
        f"PORT=1433;"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
        f"Connection Timeout=5;",
    ]
    
    for i, conn_str in enumerate(connection_strings, 1):
        try:
            print(f"  Trying format {i}...", end=" ")
            conn = pyodbc.connect(conn_str, timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            conn.close()
            print(f"[OK] SUCCESS!")
            print(f"      Connection string: {conn_str}")
            print(f"      SQL Server version: {version[:50]}...")
            return True, conn_str
        except pyodbc.Error as e:
            print(f"[FAILED] {str(e)[:80]}")
        except Exception as e:
            print(f"[ERROR] {str(e)[:80]}")
    
    return False, None


def main():
    """Test all server name formats."""
    print("=" * 70)
    print("SQL Server Connection Format Tester")
    print("=" * 70)
    print()
    print(f"Testing server: 17.0.1050.2")
    print(f"Database: {DATABASE}")
    print(f"Username: {USERNAME}")
    print()
    
    success_count = 0
    working_configs = []
    
    for server_format in SERVER_CANDIDATES:
        print(f"\nTesting: {server_format}")
        print("-" * 70)
        success, conn_str = test_connection(server_format)
        if success:
            success_count += 1
            working_configs.append((server_format, conn_str))
    
    print()
    print("=" * 70)
    if success_count > 0:
        print(f"[OK] Found {success_count} working configuration(s)!")
        print()
        print("Working server name format(s):")
        for server_format, conn_str in working_configs:
            print(f"  - {server_format}")
            print(f"    Use this in your config: server='{server_format}'")
    else:
        print("[ERROR] No working configuration found.")
        print()
        print("Troubleshooting:")
        print("1. Verify the server name/IP address is correct")
        print("2. Check if SQL Server is running and accessible")
        print("3. Verify SQL Server allows remote connections")
        print("4. Check firewall settings")
        print("5. Verify the username and password are correct")
        print("6. Check if the database names exist")
        print()
        print("Common server name formats:")
        print("  - SERVERNAME (for default instance)")
        print("  - SERVERNAME\\INSTANCENAME (for named instance)")
        print("  - IP_ADDRESS (e.g., 192.168.1.100)")
        print("  - IP_ADDRESS,PORT (e.g., 192.168.1.100,1433)")
    
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
