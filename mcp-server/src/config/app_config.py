#!/usr/bin/env python3
"""
Centralized Application Configuration
This file reads database credentials and settings from environment variables.
Loads from .env file if present, otherwise uses environment variables.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parent.parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # Try loading from current directory
    load_dotenv()

# Database Credentials - Read from environment variables
DATABASE_CREDENTIALS = {
    'username': os.getenv('MASTER_DB_USER', os.getenv('DATA_MGMT_DB_USER', '')),
    'password': os.getenv('MASTER_DB_PASSWORD', os.getenv('DATA_MGMT_DB_PASSWORD', ''))
}

# Database Server Configuration - Read from environment variables
DATABASE_SERVERS = {
    'master': {
        'server': os.getenv('MASTER_DB_SERVER', ''),
        'database': os.getenv('MASTER_DB_NAME', ''),
        'username': os.getenv('MASTER_DB_USER', ''),
        'password': os.getenv('MASTER_DB_PASSWORD', '')
    },
    'datamgmt': {
        'server': os.getenv('DATA_MGMT_DB_SERVER', ''),
        'database': os.getenv('DATA_MGMT_DB_NAME', ''),
        'username': os.getenv('DATA_MGMT_DB_USER', ''),
        'password': os.getenv('DATA_MGMT_DB_PASSWORD', '')
    }
}

# Application Settings - Read from environment variables
APP_SETTINGS = {
    'query_timeout': int(os.getenv('QUERY_TIMEOUT', '30')),
    'max_rows': int(os.getenv('MAX_ROWS', '1000')),
    'log_level': os.getenv('LOG_LEVEL', 'INFO'),
    'max_connections': int(os.getenv('MAX_CONNECTIONS', '10')),
    'connection_timeout': int(os.getenv('CONNECTION_TIMEOUT', '15'))
}

def setup_environment():
    """Set up environment variables for the application.
    
    This function ensures environment variables are set from .env file.
    The values are already loaded by load_dotenv() above, but this ensures
    they're available for backward compatibility.
    """
    # Environment variables are already loaded from .env file above
    # This function is kept for backward compatibility
    # Values are read directly from environment in DATABASE_SERVERS and APP_SETTINGS
    pass

def get_database_config():
    """Get database configuration dictionary."""
    return DATABASE_SERVERS

def get_app_settings():
    """Get application settings dictionary."""
    return APP_SETTINGS

def get_credentials():
    """Get database credentials dictionary."""
    return DATABASE_CREDENTIALS

if __name__ == "__main__":
    print("SSMS MCP Server Configuration")
    print("=" * 40)
    print(f"Configuration loaded from: {'Environment variables' if not env_path.exists() else str(env_path)}")
    print()
    print(f"Master DB Server: {DATABASE_SERVERS['master']['server']}")
    print(f"Master DB Name: {DATABASE_SERVERS['master']['database']}")
    print(f"Master DB User: {DATABASE_SERVERS['master']['username']}")
    print(f"Master DB Password: {'*' * len(DATABASE_SERVERS['master']['password']) if DATABASE_SERVERS['master']['password'] else '(not set)'}")
    print()
    print(f"Data Mgmt DB Server: {DATABASE_SERVERS['datamgmt']['server']}")
    print(f"Data Mgmt DB Name: {DATABASE_SERVERS['datamgmt']['database']}")
    print(f"Data Mgmt DB User: {DATABASE_SERVERS['datamgmt']['username']}")
    print(f"Data Mgmt DB Password: {'*' * len(DATABASE_SERVERS['datamgmt']['password']) if DATABASE_SERVERS['datamgmt']['password'] else '(not set)'}")
    print()
    print(f"Query Timeout: {APP_SETTINGS['query_timeout']}s")
    print(f"Max Rows: {APP_SETTINGS['max_rows']}")
    print(f"Log Level: {APP_SETTINGS['log_level']}")
    print()
    if not DATABASE_SERVERS['master']['server'] or not DATABASE_SERVERS['master']['database']:
        print("WARNING: Master database configuration is incomplete!")
        print("Please check your .env file or environment variables.")
    if not DATABASE_SERVERS['datamgmt']['server'] or not DATABASE_SERVERS['datamgmt']['database']:
        print("WARNING: Data Management database configuration is incomplete!")
        print("Please check your .env file or environment variables.")