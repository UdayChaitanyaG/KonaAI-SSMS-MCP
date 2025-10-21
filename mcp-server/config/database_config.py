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
    """Application configuration."""
    
    # Master Database Configuration
    master_db_server: str = Field(default="DC-L-0004\\MSSQLSERVER02", description="Master DB server")
    master_db_name: str = Field(default="KonaAI_Master", description="Master database name")
    master_db_user: str = Field(..., description="Master DB username")
    master_db_password: str = Field(..., description="Master DB password")
    
    # Data Management Database Configuration
    data_mgmt_db_server: str = Field(default="dc-l-", description="Data Management DB server")
    data_mgmt_db_name: str = Field(default="DIT_GDB", description="Data Management database name")
    data_mgmt_db_user: str = Field(..., description="Data Management DB username")
    data_mgmt_db_password: str = Field(..., description="Data Management DB password")
    
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


def get_connection_string(db_config: DatabaseConfig) -> str:
    """
    Build SQL Server connection string from configuration.
    
    Args:
        db_config: Database configuration object
        
    Returns:
        Connection string for pyodbc
    """
    return (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={db_config.server};"
        f"DATABASE={db_config.database};"
        f"UID={db_config.username};"
        f"PWD={db_config.password};"
        f"PORT={db_config.port};"
        f"Encrypt={'yes' if db_config.encrypt else 'no'};"
        f"TrustServerCertificate={'yes' if db_config.trust_server_certificate else 'no'};"
        f"Connection Timeout={db_config.timeout};"
        f"Login Timeout={db_config.timeout};"
    )


# Global configuration instance
config = AppConfig()
