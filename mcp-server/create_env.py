#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create .env File
Creates a .env file with database configuration template.
"""

from pathlib import Path

ENV_CONTENT = """# KonaAI SSMS MCP Server Configuration
# Database credentials and connection settings
# 
# IMPORTANT: This file contains sensitive information and should NOT be committed to version control.
# The .env file is already in .gitignore

# Master Database Configuration
MASTER_DB_SERVER=17.0.1050.2
MASTER_DB_NAME=KonaAI_Master
MASTER_DB_USER=SSMSLOGIN
MASTER_DB_PASSWORD=LoginPassword123

# Data Management Database Configuration
DATA_MGMT_DB_SERVER=17.0.1050.2
DATA_MGMT_DB_NAME=KonaAI_Master_001
DATA_MGMT_DB_USER=SSMSLOGIN
DATA_MGMT_DB_PASSWORD=LoginPassword123

# Application Settings
QUERY_TIMEOUT=30
MAX_ROWS=1000
LOG_LEVEL=INFO

# Connection Pool Settings
MAX_CONNECTIONS=10
CONNECTION_TIMEOUT=15
"""


def main():
    """Create .env file."""
    project_path = Path(__file__).parent
    env_file = project_path / ".env"
    
    if env_file.exists():
        print(f"[INFO] .env file already exists at {env_file}")
        print("[INFO] Skipping creation. Edit the existing file if needed.")
        return True
    
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(ENV_CONTENT)
        
        print(f"[OK] .env file created at: {env_file}")
        print("\nConfiguration:")
        print("  Master DB Server: 17.0.1050.2")
        print("  Master DB Name: KonaAI_Master")
        print("  Master DB User: SSMSLOGIN")
        print("  Data Mgmt DB Server: 17.0.1050.2")
        print("  Data Mgmt DB Name: KonaAI_Master_001")
        print("  Data Mgmt DB User: SSMSLOGIN")
        print("\nYou can edit the .env file to change these values.")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to create .env file: {e}")
        return False


if __name__ == "__main__":
    main()
