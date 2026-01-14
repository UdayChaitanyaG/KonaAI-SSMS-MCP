"""
Configuration module for SSMS MCP Server.
Uses Pydantic Settings for type-safe configuration management.
"""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    """Database connection configuration."""
    
    server: str = Field(..., description="SQL Server instance name or IP address")
    database: str = Field(..., description="Database name")
    username: str = Field(..., description="SQL Server username")
    password: str = Field(..., description="SQL Server password")
    port: int = Field(default=1433, description="SQL Server port")
    timeout: int = Field(default=30, description="Connection timeout in seconds")
    encrypt: bool = Field(default=True, description="Use encryption for connection")
    trust_server_certificate: bool = Field(default=True, description="Trust server certificate")
    
    model_config = SettingsConfigDict(
        env_prefix="",
        case_sensitive=False,
        extra="ignore"
    )


class AppConfig(BaseSettings):
    """Application configuration.
    
    Reads from .env file or environment variables.
    Defaults are provided but should be overridden via .env file.
    """
    
    # Master Database Configuration
    master_db_server: str = Field(default="", description="Master DB server (from MASTER_DB_SERVER env var)")
    master_db_name: str = Field(default="", description="Master database name (from MASTER_DB_NAME env var)")
    master_db_user: str = Field(default="", description="Master DB username (from MASTER_DB_USER env var)")
    master_db_password: str = Field(default="", description="Master DB password (from MASTER_DB_PASSWORD env var)")
    
    # Data Management Database Configuration
    data_mgmt_db_server: str = Field(default="", description="Data Management DB server (from DATA_MGMT_DB_SERVER env var)")
    data_mgmt_db_name: str = Field(default="", description="Data Management database name (from DATA_MGMT_DB_NAME env var)")
    data_mgmt_db_user: str = Field(default="", description="Data Management DB username (from DATA_MGMT_DB_USER env var)")
    data_mgmt_db_password: str = Field(default="", description="Data Management DB password (from DATA_MGMT_DB_PASSWORD env var)")
    
    # Application Settings
    query_timeout: int = Field(default=30, description="Query timeout in seconds")
    max_rows: int = Field(default=1000, description="Maximum rows to return")
    log_level: str = Field(default="INFO", description="Logging level")
    
    # Connection Pool Settings
    max_connections: int = Field(default=10, description="Maximum connections in pool")
    connection_timeout: int = Field(default=15, description="Connection timeout in seconds")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    def get_master_db_config(self) -> DatabaseConfig:
        """Get Master database configuration."""
        return DatabaseConfig(
            server=self.master_db_server,
            database=self.master_db_name,
            username=self.master_db_user,
            password=self.master_db_password,
            timeout=self.query_timeout
        )
    
    def get_data_mgmt_db_config(self) -> DatabaseConfig:
        """Get Data Management database configuration."""
        return DatabaseConfig(
            server=self.data_mgmt_db_server,
            database=self.data_mgmt_db_name,
            username=self.data_mgmt_db_user,
            password=self.data_mgmt_db_password,
            timeout=self.query_timeout
        )


def normalize_server_name(server: str) -> str:
    """
    Normalize SQL Server name to handle different formats.
    
    Handles:
    - IP addresses: 192.168.1.100
    - Server names: SERVERNAME
    - Named instances: SERVERNAME\\INSTANCENAME or SERVERNAME/INSTANCENAME
    - With port: SERVERNAME,PORT or SERVERNAME:PORT
    
    Args:
        server: Server name in various formats
        
    Returns:
        Normalized server name for connection string
    """
    if not server:
        return server
    
    # Remove any protocol prefixes
    server = server.replace("tcp:", "").replace("TCP:", "")
    
    # Handle port notation (convert : to ,)
    if ":" in server and "," not in server:
        server = server.replace(":", ",")
    
    # Normalize instance separator (both \ and / work, but \ is standard)
    if "/" in server and "\\" not in server:
        server = server.replace("/", "\\")
    
    return server


def get_connection_string(db_config: DatabaseConfig) -> str:
    """
    Build SQL Server connection string from configuration.
    
    Args:
        db_config: Database configuration object
        
    Returns:
        Connection string for pyodbc
    """
    # Normalize server name
    server = normalize_server_name(db_config.server)
    
    # Use Windows Authentication if username is empty
    if not db_config.username or not db_config.password:
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={db_config.database};"
            f"Trusted_Connection=yes;"
            f"Encrypt={'yes' if db_config.encrypt else 'no'};"
            f"TrustServerCertificate={'yes' if db_config.trust_server_certificate else 'no'};"
            f"Connection Timeout={db_config.timeout};"
        )
    else:
        # Use SQL Server Authentication
        # Don't add port explicitly - let SQL Server use default port or dynamic port
        # Only add port if explicitly specified in server name (e.g., "localhost,1433")
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={db_config.database};"
            f"UID={db_config.username};"
            f"PWD={db_config.password};"
            f"Encrypt={'yes' if db_config.encrypt else 'no'};"
            f"TrustServerCertificate={'yes' if db_config.trust_server_certificate else 'no'};"
            f"Connection Timeout={db_config.timeout};"
            f"Login Timeout={db_config.timeout};"
        )
    
    return conn_str


# Global configuration instance
config = AppConfig()
