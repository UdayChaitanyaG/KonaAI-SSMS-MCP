# Python SSMS MCP Server

A comprehensive Model Context Protocol (MCP) server for SQL Server Management Studio integration, providing enhanced database access capabilities through Python.

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

## Installation

### Prerequisites

1. **Python 3.8+**: Ensure you have Python 3.8 or higher installed
2. **SQL Server ODBC Driver**: Install Microsoft ODBC Driver 17 for SQL Server
3. **Database Access**: Valid credentials for both Master and Data Management databases

### ODBC Driver Installation

#### Windows
```bash
# Download and install Microsoft ODBC Driver 17 for SQL Server
# https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
```

#### Linux (Ubuntu/Debian)
```bash
# Add Microsoft repository
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Install ODBC driver
apt-get update
apt-get install msodbcsql17
```

#### macOS
```bash
# Install using Homebrew
brew install microsoft/mssql-release/msodbcsql17
```

### Python Dependencies

```bash
# Navigate to the python directory
cd KonaAI-SSMS-MCP/python

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

## Configuration

### Environment Setup

1. **Copy the environment template**:
   ```bash
   cp env.example .env
   ```

2. **Update `.env` with your database credentials**:
   ```env
   # Master Database Configuration
   MASTER_DB_SERVER=DC-L-0004\\MSSQLSERVER02
   MASTER_DB_NAME=KonaAI_Master
   MASTER_DB_USER=your_master_db_username
   MASTER_DB_PASSWORD=your_master_db_password

   # Data Management Database Configuration
   DATA_MGMT_DB_SERVER=dc-l-
   DATA_MGMT_DB_NAME=DIT_GDB
   DATA_MGMT_DB_USER=your_datamgmt_db_username
   DATA_MGMT_DB_PASSWORD=your_datamgmt_db_password

   # Application Settings
   QUERY_TIMEOUT=30
   MAX_ROWS=1000
   LOG_LEVEL=INFO
   ```

### Security Best Practices

- **Never commit `.env` files** to version control
- **Use strong passwords** for production environments
- **Create dedicated service accounts** with minimal required permissions
- **Enable SQL Server encryption** in production
- **Use Windows Authentication** for local development when possible

## Usage

### Starting the MCP Server

```bash
# Run the server directly
python src/main.py

# Or use the installed package
ssms-mcp
```

### Cursor/Claude Desktop Integration

1. **Add to Cursor MCP configuration**:
   ```json
   {
     "mcpServers": {
       "ssms-mcp": {
         "command": "python",
         "args": ["path/to/KonaAI-SSMS-MCP/python/src/main.py"],
         "env": {
           "PYTHONPATH": "path/to/KonaAI-SSMS-MCP/python/src"
         }
       }
     }
   }
   ```

2. **Restart Cursor** to load the new MCP server

### Available Tools

#### Query Execution
```python
# Execute a SELECT query
{
  "tool": "execute_query",
  "arguments": {
    "database": "master",
    "query": "SELECT * FROM Clients WHERE IsActive = 1",
    "max_rows": 100
  }
}
```

#### CRUD Operations
```python
# Insert data
{
  "tool": "insert_data",
  "arguments": {
    "database": "datamgmt",
    "table_name": "File_Detail",
    "data": {
      "FileName": "document.pdf",
      "FileSize": 1024000,
      "FileType": "application/pdf"
    }
  }
}

# Update data
{
  "tool": "update_data",
  "arguments": {
    "database": "datamgmt",
    "table_name": "File_Detail",
    "data": {"IsActive": 0},
    "where_clause": "FileName = ?",
    "where_parameters": {"FileName": "document.pdf"}
  }
}
```

#### Schema Analysis
```python
# Get table schema
{
  "tool": "get_table_schema",
  "arguments": {
    "database": "master",
    "table_name": "Clients",
    "include_indexes": true,
    "include_foreign_keys": true
  }
}
```

#### Stored Procedure Execution
```python
# Execute stored procedure
{
  "tool": "execute_procedure",
  "arguments": {
    "database": "master",
    "procedure_name": "sp_helpdb",
    "parameters": {},
    "output_parameters": []
  }
}
```

### Available Resources

#### Table Resources
- **URI Pattern**: `ssms://{database}/tables/{schema}/{table}`
- **Content**: Complete table metadata, schema, indexes, foreign keys, and sample data

#### Procedure Resources
- **URI Pattern**: `ssms://{database}/procedures/{schema}/{procedure}`
- **Content**: Procedure definition, parameters, and metadata

#### Trigger Resources
- **URI Pattern**: `ssms://{database}/triggers/{trigger}`
- **Content**: Trigger definition and execution context

#### View Resources
- **URI Pattern**: `ssms://{database}/views/{schema}/{view}`
- **Content**: View definition and dependencies

## Architecture

### Project Structure
```
python/
├── src/
│   ├── main.py                 # MCP server entry point
│   ├── config.py               # Configuration management
│   ├── database/
│   │   ├── base.py            # Base database connection
│   │   ├── master_db.py       # Master database operations
│   │   └── datamgmt_db.py     # Data Management database operations
│   ├── tools/
│   │   ├── query_tool.py      # Query execution
│   │   ├── crud_tool.py       # CRUD operations
│   │   ├── schema_tool.py     # Schema introspection
│   │   └── sp_tool.py         # Stored procedure execution
│   └── resources/
│       ├── tables.py           # Tables resource provider
│       ├── procedures.py       # Procedures resource provider
│       ├── triggers.py         # Triggers resource provider
│       └── views.py            # Views resource provider
├── requirements.txt           # Python dependencies
├── pyproject.toml            # Project metadata
├── env.example               # Environment template
└── README.md                 # This file
```

### Security Features

- **SQL Injection Prevention**: All queries use parameterized execution
- **Query Validation**: Whitelist approach for allowed SQL keywords
- **Connection Security**: Encrypted connections with certificate validation
- **Input Sanitization**: Comprehensive validation of all inputs
- **Error Handling**: Secure error messages without sensitive information

### Performance Optimizations

- **Connection Pooling**: Efficient database connection management
- **Query Optimization**: Automatic row limiting for large result sets
- **Caching**: Schema information caching for repeated requests
- **Async Operations**: Non-blocking database operations

## Troubleshooting

### Common Issues

#### Connection Errors
```bash
# Check ODBC driver installation
python -c "import pyodbc; print(pyodbc.drivers())"

# Test connection manually
python -c "
import pyodbc
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server;DATABASE=your_db;UID=user;PWD=password')
print('Connection successful')
"
```

#### Permission Issues
- Ensure the database user has appropriate permissions
- Check SQL Server authentication settings
- Verify firewall rules for database access

#### Environment Issues
```bash
# Check environment variables
python -c "from src.config import config; print(config.master_db_server)"

# Validate configuration
python -c "from src.config import config; print('Config loaded successfully')"
```

### Logging

The server provides comprehensive logging at multiple levels:

```bash
# Set log level in .env
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Testing

```bash
# Test database connections
python -c "
from src.database.master_db import MasterDatabase
from src.database.datamgmt_db import DataManagementDatabase
from src.config import config

master_db = MasterDatabase(config.get_master_db_config())
data_mgmt_db = DataManagementDatabase(config.get_data_mgmt_db_config())

print('Master DB:', master_db.test_connection())
print('Data Mgmt DB:', data_mgmt_db.test_connection())
"
```

## Development

### Adding New Tools

1. Create a new tool class in `src/tools/`
2. Implement the tool interface with `get_tool()` and execution methods
3. Register the tool in `src/main.py`
4. Add comprehensive tests

### Adding New Resources

1. Create a new resource class in `src/resources/`
2. Implement resource discovery and content methods
3. Register the resource in `src/main.py`
4. Update documentation

### Testing

```bash
# Run unit tests (when implemented)
python -m pytest tests/

# Run integration tests
python -m pytest tests/integration/
```

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
- Check the troubleshooting section
- Review the logs for error details

---

**Note**: This MCP server is designed for KonaAI's specific database architecture. Modify the database classes and configuration as needed for your environment.
