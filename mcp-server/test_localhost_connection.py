#!/usr/bin/env python3
"""
Test different localhost connection formats to find the working one.
"""

import pyodbc
import sys

# Test different server name formats
formats_to_try = [
    "localhost",
    "127.0.0.1",
    "(local)",
    ".\\MSSQLSERVER",
    ".\\SQLEXPRESS",
    "localhost\\MSSQLSERVER",
    "localhost,1433",
    "127.0.0.1,1433",
    "(local)\\MSSQLSERVER",
]

database = "KonaAI_Master"
username = "SSMSLOGIN"
password = "LoginPassword123"

print("=" * 70)
print("Testing SQL Server Connection Formats")
print("=" * 70)
print()

for server_name in formats_to_try:
    print(f"Testing: {server_name}...", end=" ")
    
    # Try with SQL Server Authentication
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server_name};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
        f"Connection Timeout=5;"
    )
    
    try:
        conn = pyodbc.connect(conn_str, timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION, DB_NAME()")
        result = cursor.fetchone()
        conn.close()
        print("[SUCCESS]")
        print(f"  SQL Server Version: {result[0][:60]}...")
        print(f"  Connected to Database: {result[1]}")
        print(f"  Working connection string:")
        print(f"  SERVER={server_name}")
        print()
        print("=" * 70)
        print("FOUND WORKING SERVER NAME!")
        print("=" * 70)
        print(f"Update your .env file with: MASTER_DB_SERVER={server_name}")
        print(f"Update your .env file with: DATA_MGMT_DB_SERVER={server_name}")
        sys.exit(0)
    except pyodbc.Error as e:
        error_code = str(e).split("]")[0] if "]" in str(e) else ""
        print(f"[FAILED] {error_code}")
    except Exception as e:
        print(f"[ERROR] {str(e)[:50]}")

print()
print("=" * 70)
print("None of the tested formats worked.")
print("=" * 70)
print()
print("Next steps:")
print("1. Check SQL Server Configuration Manager")
print("2. Verify TCP/IP protocol is enabled")
print("3. Check if SQL Server is using a different port")
print("4. Try connecting from SQL Server Management Studio and note the server name")
sys.exit(1)
