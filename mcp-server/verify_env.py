#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify Environment Configuration
Tests that configuration is properly loaded from .env file.
"""

import sys
from pathlib import Path

# Add src to path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from config.app_config import DATABASE_SERVERS, APP_SETTINGS, env_path


def main():
    """Verify configuration."""
    print("=" * 70)
    print("Environment Configuration Verification")
    print("=" * 70)
    print()
    
    print(f"Configuration source: {env_path if env_path.exists() else 'Environment variables'}")
    print()
    
    # Check Master DB
    print("Master Database Configuration:")
    print("-" * 70)
    master = DATABASE_SERVERS['master']
    print(f"  Server: {master['server'] or '(not set)'}")
    print(f"  Database: {master['database'] or '(not set)'}")
    print(f"  Username: {master['username'] or '(not set)'}")
    print(f"  Password: {'*' * len(master['password']) if master['password'] else '(not set)'}")
    
    if not master['server'] or not master['database']:
        print("  [WARN] Master database configuration is incomplete!")
    else:
        print("  [OK] Master database configuration is complete")
    print()
    
    # Check Data Mgmt DB
    print("Data Management Database Configuration:")
    print("-" * 70)
    datamgmt = DATABASE_SERVERS['datamgmt']
    print(f"  Server: {datamgmt['server'] or '(not set)'}")
    print(f"  Database: {datamgmt['database'] or '(not set)'}")
    print(f"  Username: {datamgmt['username'] or '(not set)'}")
    print(f"  Password: {'*' * len(datamgmt['password']) if datamgmt['password'] else '(not set)'}")
    
    if not datamgmt['server'] or not datamgmt['database']:
        print("  [WARN] Data Management database configuration is incomplete!")
    else:
        print("  [OK] Data Management database configuration is complete")
    print()
    
    # Check App Settings
    print("Application Settings:")
    print("-" * 70)
    print(f"  Query Timeout: {APP_SETTINGS['query_timeout']}s")
    print(f"  Max Rows: {APP_SETTINGS['max_rows']}")
    print(f"  Log Level: {APP_SETTINGS['log_level']}")
    print(f"  Max Connections: {APP_SETTINGS['max_connections']}")
    print(f"  Connection Timeout: {APP_SETTINGS['connection_timeout']}s")
    print()
    
    # Summary
    print("=" * 70)
    master_ok = master['server'] and master['database'] and master['username'] and master['password']
    datamgmt_ok = datamgmt['server'] and datamgmt['database'] and datamgmt['username'] and datamgmt['password']
    
    if master_ok and datamgmt_ok:
        print("[OK] All configurations are properly loaded from .env file!")
        return True
    else:
        print("[WARN] Some configurations are missing!")
        print()
        print("To fix:")
        print("1. Ensure .env file exists in the mcp-server directory")
        print("2. Run: py create_env.py (to create/update .env file)")
        print("3. Or manually create .env with the required variables")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
