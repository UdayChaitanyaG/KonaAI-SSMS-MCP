# KonaAI SSMS MCP Server

A comprehensive Model Context Protocol (MCP) server for SQL Server Management Studio integration, providing enhanced database access capabilities through Python.

## Overview

This repository contains a Python-based MCP server that replaces the previous TypeScript implementation, offering enhanced features and better integration with SQL Server databases.

## Features

### 🔧 **Core Capabilities**
- **Dual Database Support**: Master Database (`KonaAI_Master`) and Data Management Database (`DIT_GDB`)
- **SQL Server Authentication**: Secure username/password authentication
- **Connection Pooling**: Efficient connection management with pyodbc
- **Parameterized Queries**: SQL injection prevention through parameterized execution
- **Comprehensive Schema Introspection**: Tables, views, stored procedures, triggers, indexes, and relationships

### 🛠️ **MCP Tools**
- **Query Execution**: Safe SELECT, INSERT, UPDATE, DELETE operations
- **CRUD Operations**: Insert, update, and delete data with validation
- **Schema Analysis**: Detailed database schema information and relationships
- **Stored Procedure Execution**: Execute procedures with input/output parameters
- **Advanced Analytics**: Table statistics, row counts, and performance metrics

### 📊 **MCP Resources**
- **Tables**: Complete table metadata, schema, and sample data
- **Stored Procedures**: Procedure definitions, parameters, and metadata
- **Triggers**: Trigger definitions and execution context
- **Views**: View definitions and dependencies

## Project Structure

```
KonaAI-SSMS-MCP/
├── mcp-server/               # MCP Server Implementation
│   ├── main.py              # Main entry point
│   ├── mcp_config.json     # MCP client configuration
│   ├── server/              # Core server implementation
│   │   ├── ssms_mcp_server.py  # Main MCP server class
│   │   ├── database/        # Database connection layer
│   │   ├── tools/           # MCP tools implementation
│   │   └── resources/       # MCP resources implementation
│   ├── config/              # Configuration management
│   │   ├── database_config.py
│   │   └── env.example
│   ├── docs/                # Documentation
│   │   ├── README.md
│   │   └── ARCHITECTURE_AND_STRUCTURE.md
│   ├── requirements.txt     # Python dependencies
│   └── pyproject.toml      # Project metadata
└── README.md               # This file
```

## Quick Start

### 1. Navigate to MCP Server
```bash
cd mcp-server
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp env.example .env
# Edit .env with your database credentials
```

### 4. Run the Server
```bash
python src/main.py
```

## Detailed Documentation

For comprehensive installation, configuration, and usage instructions, see the [MCP Server Documentation](mcp-server/docs/README.md).

For detailed architecture and project structure information, see the [Architecture & Structure Guide](mcp-server/docs/ARCHITECTURE_AND_STRUCTURE.md).

## Migration from TypeScript

This Python implementation replaces the previous TypeScript version with the following improvements:

- **Enhanced Security**: Better SQL injection prevention and input validation
- **Stored Procedure Support**: Full execution with input/output parameters
- **Advanced Schema Analysis**: Comprehensive database introspection
- **Better Error Handling**: Detailed error messages and logging
- **Performance Optimizations**: Connection pooling and query optimization
- **Transaction Support**: Multi-statement transaction execution

## Requirements

- **Python 3.8+**
- **Microsoft ODBC Driver 17 for SQL Server**
- **Database Access**: Valid credentials for both Master and Data Management databases

## Security

- All queries use parameterized execution (no string interpolation)
- Query type validation (whitelist approach)
- Connection credentials in environment variables only
- SQL injection prevention through pyodbc parameterization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes with tests
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section in the Python README
- Review the logs for error details
