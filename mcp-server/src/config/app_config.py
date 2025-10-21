#!/usr/bin/env python3
"""
Centralized Application Configuration
This file contains all database credentials and settings for the SSMS MCP Server.
"""

import os

# Database Credentials - Using Windows Authentication
DATABASE_CREDENTIALS = {
    'username': '',  # Empty for Windows Authentication
    'password': ''   # Empty for Windows Authentication
}

# Database Server Configuration
DATABASE_SERVERS = {
    'master': {
        'server': 'DC-L-',
        'database': 'KonaAI',
        'username': DATABASE_CREDENTIALS['username'],
        'password': DATABASE_CREDENTIALS['password']
    },
    'datamgmt': {
        'server': 'DC-L-',
        'database': 'DIT_GDB',
        'username': DATABASE_CREDENTIALS['username'],
        'password': DATABASE_CREDENTIALS['password']
    }
}

# Application Settings
APP_SETTINGS = {
    'query_timeout': 30,
    'max_rows': 1000,
    'log_level': 'INFO',
    'max_connections': 10,
    'connection_timeout': 15
}

def setup_environment():
    """Set up environment variables for the application."""
    # Master Database Configuration
    os.environ.update({
        'MASTER_DB_SERVER': DATABASE_SERVERS['master']['server'],
        'MASTER_DB_NAME': DATABASE_SERVERS['master']['database'],
        'MASTER_DB_USER': DATABASE_SERVERS['master']['username'],
        'MASTER_DB_PASSWORD': DATABASE_SERVERS['master']['password'],
        
        # Data Management Database Configuration
        'DATA_MGMT_DB_SERVER': DATABASE_SERVERS['datamgmt']['server'],
        'DATA_MGMT_DB_NAME': DATABASE_SERVERS['datamgmt']['database'],
        'DATA_MGMT_DB_USER': DATABASE_SERVERS['datamgmt']['username'],
        'DATA_MGMT_DB_PASSWORD': DATABASE_SERVERS['datamgmt']['password'],
        
        # Application Settings
        'QUERY_TIMEOUT': str(APP_SETTINGS['query_timeout']),
        'MAX_ROWS': str(APP_SETTINGS['max_rows']),
        'LOG_LEVEL': APP_SETTINGS['log_level'],
        'MAX_CONNECTIONS': str(APP_SETTINGS['max_connections']),
        'CONNECTION_TIMEOUT': str(APP_SETTINGS['connection_timeout'])
    })

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
    print("🔧 SSMS MCP Server Configuration")
    print("=" * 40)
    print(f"Username: {DATABASE_CREDENTIALS['username']}")
    print(f"Password: {'*' * len(DATABASE_CREDENTIALS['password'])}")
    print(f"Master DB: {DATABASE_SERVERS['master']['server']}/{DATABASE_SERVERS['master']['database']}")
    print(f"Data Mgmt DB: {DATABASE_SERVERS['datamgmt']['server']}/{DATABASE_SERVERS['datamgmt']['database']}")
    print(f"Query Timeout: {APP_SETTINGS['query_timeout']}s")
    print(f"Max Rows: {APP_SETTINGS['max_rows']}")
    print(f"Log Level: {APP_SETTINGS['log_level']}")
