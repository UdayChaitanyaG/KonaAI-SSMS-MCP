# KonaAI SSMS MCP Server - Architecture & Structure

## Overview

The KonaAI SSMS MCP Server is a comprehensive Model Context Protocol (MCP) server that provides enhanced SQL Server database access capabilities. It follows a modular architecture designed for maintainability, scalability, and security.

## Directory Structure

```
KonaAI-SSMS-MCP/
├── .gitignore                     # Git ignore rules for Python project
├── README.md                      # Main project documentation
└── mcp-server/                    # MCP Server Implementation
    ├── main.py                    # 🚀 Main entry point
    ├── mcp_config.json           # MCP client configuration
    ├── requirements.txt           # Python dependencies
    ├── pyproject.toml            # Project metadata
    │
    ├── server/                   # 🏗️ Core Server Implementation
    │   ├── __init__.py
    │   ├── ssms_mcp_server.py     # Main MCP server class
    │   │
    │   ├── database/             # 🗄️ Database Connection Layer
    │   │   ├── __init__.py
    │   │   ├── base.py           # Base database connection with pooling
    │   │   ├── master_db.py      # Master database operations
    │   │   └── datamgmt_db.py    # Data Management database operations
    │   │
    │   ├── tools/                # 🛠️ MCP Tools (Executable Operations)
    │   │   ├── __init__.py
    │   │   ├── query_tool.py     # SQL query execution
    │   │   ├── crud_tool.py      # CRUD operations (Insert/Update/Delete)
    │   │   ├── schema_tool.py    # Schema introspection and analysis
    │   │   └── sp_tool.py        # Stored procedure execution
    │   │
    │   └── resources/             # 📚 MCP Resources (Metadata)
    │       ├── __init__.py
    │       ├── tables.py         # Table metadata and schema
    │       ├── procedures.py     # Stored procedure metadata
    │       ├── triggers.py       # Trigger metadata
    │       └── views.py          # View metadata
    │
    ├── config/                   # ⚙️ Configuration Management
    │   ├── __init__.py
    │   ├── database_config.py    # Database configuration with Pydantic
    │   └── env.example          # Environment variables template
    │
    └── docs/                     # 📖 Documentation
        ├── __init__.py
        ├── README.md             # Detailed setup and usage guide
        └── ARCHITECTURE_AND_STRUCTURE.md  # This file
```

## Component Architecture

### 1. Entry Point (`main.py`)
- **Purpose**: Main entry point for the MCP server
- **Responsibilities**: 
  - Set up Python path
  - Import and execute the MCP server
  - Handle command-line arguments

### 2. MCP Server (`server/ssms_mcp_server.py`)
- **Purpose**: Core MCP server implementation
- **Responsibilities**:
  - Initialize MCP server with StdIO transport
  - Register all tools and resources
  - Handle tool execution requests
  - Handle resource read requests
  - Error handling and logging
  - Graceful shutdown with connection cleanup

### 3. Database Layer (`server/database/`)
- **Purpose**: Database connection and operation management
- **Components**:
  - **`base.py`**: Base database connection class with connection pooling
  - **`master_db.py`**: Master database specific operations
  - **`datamgmt_db.py`**: Data Management database specific operations

### 4. Tools Layer (`server/tools/`)
- **Purpose**: MCP tools that perform executable operations
- **Components**:
  - **`query_tool.py`**: Execute SQL queries (SELECT, INSERT, UPDATE, DELETE)
  - **`crud_tool.py`**: CRUD operations (Insert, Update, Delete)
  - **`schema_tool.py`**: Schema introspection and analysis
  - **`sp_tool.py`**: Stored procedure execution

### 5. Resources Layer (`server/resources/`)
- **Purpose**: MCP resources that expose metadata
- **Components**:
  - **`tables.py`**: Table metadata and schema information
  - **`procedures.py`**: Stored procedure metadata
  - **`triggers.py`**: Trigger metadata
  - **`views.py`**: View metadata

### 6. Configuration Layer (`config/`)
- **Purpose**: Configuration management and environment setup
- **Components**:
  - **`database_config.py`**: Database configuration using Pydantic Settings
  - **`env.example`**: Environment variables template

## File Descriptions

### 🚀 Core Files

| File | Purpose | Key Features |
|------|--------|--------------|
| `main.py` | Main entry point | Python path setup, server execution |
| `mcp_config.json` | MCP client config | Cursor/Claude Desktop integration |
| `requirements.txt` | Dependencies | Python package requirements |
| `pyproject.toml` | Project metadata | Build configuration, entry points |

### 🏗️ Server Implementation

| File | Purpose | Key Features |
|------|--------|--------------|
| `ssms_mcp_server.py` | Main MCP server | StdIO transport, tool/resource registration |
| `database/base.py` | Base database class | Connection pooling, parameterized queries |
| `database/master_db.py` | Master DB operations | Schema queries, CRUD operations |
| `database/datamgmt_db.py` | Data Mgmt DB operations | Schema queries, CRUD operations |

### 🛠️ MCP Tools

| File | Purpose | Key Features |
|------|--------|--------------|
| `query_tool.py` | SQL query execution | SELECT, INSERT, UPDATE, DELETE |
| `crud_tool.py` | CRUD operations | Insert, Update, Delete with validation |
| `schema_tool.py` | Schema analysis | Tables, views, procedures, relationships |
| `sp_tool.py` | Stored procedures | Execute with input/output parameters |

### 📚 MCP Resources

| File | Purpose | Key Features |
|------|--------|--------------|
| `tables.py` | Table metadata | Schema, columns, constraints, indexes |
| `procedures.py` | Procedure metadata | Definitions, parameters, dependencies |
| `triggers.py` | Trigger metadata | Definitions, execution context |
| `views.py` | View metadata | Definitions, dependencies, relationships |

### ⚙️ Configuration

| File | Purpose | Key Features |
|------|--------|--------------|
| `database_config.py` | Database config | Pydantic Settings, environment variables |
| `env.example` | Environment template | All required environment variables |

## Data Flow

```
Client Request → MCP Server → Tool/Resource → Database Layer → SQL Server
                ↓
            Response ← Formatted Result ← Query Result ← Database Response
```

## Module Dependencies

```
main.py
└── server/ssms_mcp_server.py
    ├── config/database_config.py
    ├── server/database/base.py
    │   ├── server/database/master_db.py
    │   └── server/database/datamgmt_db.py
    ├── server/tools/query_tool.py
    ├── server/tools/crud_tool.py
    ├── server/tools/schema_tool.py
    ├── server/tools/sp_tool.py
    ├── server/resources/tables.py
    ├── server/resources/procedures.py
    ├── server/resources/triggers.py
    └── server/resources/views.py
```

## Security Architecture

### 1. Authentication
- **SQL Server Authentication**: Username/password based authentication
- **Environment Variables**: Credentials stored in environment variables
- **No Hardcoded Secrets**: All sensitive data externalized

### 2. SQL Injection Prevention
- **Parameterized Queries**: All queries use parameterized execution
- **Input Validation**: Query type validation and sanitization
- **No String Interpolation**: No direct string concatenation in SQL

### 3. Connection Security
- **Connection Pooling**: Secure connection management
- **Timeout Handling**: Prevents long-running connections
- **Error Handling**: Comprehensive error handling without information leakage

## Performance Architecture

### 1. Connection Management
- **Connection Pooling**: Efficient connection reuse
- **Connection Limits**: Configurable connection pool size
- **Connection Timeout**: Automatic connection cleanup

### 2. Query Optimization
- **Result Set Limits**: Configurable maximum rows
- **Query Timeout**: Prevents long-running queries
- **Caching**: Schema information caching for repeated requests

### 3. Resource Management
- **Memory Management**: Efficient memory usage for large result sets
- **Resource Cleanup**: Proper cleanup of database connections
- **Async-Ready**: Architecture prepared for async operations

## Error Handling Architecture

### 1. Database Errors
- **Connection Errors**: Retry logic with exponential backoff
- **Query Errors**: Detailed error messages with context
- **Timeout Errors**: Graceful timeout handling

### 2. MCP Errors
- **Tool Errors**: Proper error propagation to MCP clients
- **Resource Errors**: Graceful resource access failures
- **Server Errors**: Comprehensive server error handling

### 3. Logging
- **Structured Logging**: JSON-formatted logs
- **Log Levels**: Configurable logging levels
- **Error Tracking**: Comprehensive error tracking and reporting

## Key Design Principles

### 1. **Separation of Concerns**
- **Database Layer**: Pure database operations
- **Tools Layer**: MCP tool implementations
- **Resources Layer**: MCP resource implementations
- **Configuration Layer**: Environment and settings management

### 2. **Modular Architecture**
- Each component has a single responsibility
- Clear interfaces between layers
- Easy to extend and maintain

### 3. **Security First**
- Parameterized queries prevent SQL injection
- Environment variables for sensitive data
- Input validation and sanitization

### 4. **Performance Optimized**
- Connection pooling for database connections
- Configurable result set limits
- Efficient query execution

### 5. **MCP Compliance**
- Follows MCP protocol specifications
- Proper tool and resource registration
- StdIO transport for client integration

## Extension Points

### 1. New Tools
- Add new tool classes in `server/tools/`
- Implement MCP tool interface
- Register in main server

### 2. New Resources
- Add new resource classes in `server/resources/`
- Implement MCP resource interface
- Register in main server

### 3. New Database Support
- Extend `base.py` for new database types
- Create specific database classes
- Update configuration as needed

## Development Workflow

### 1. **Adding New Tools**
1. Create new tool class in `server/tools/`
2. Implement MCP tool interface
3. Register in `ssms_mcp_server.py`
4. Add tests and documentation

### 2. **Adding New Resources**
1. Create new resource class in `server/resources/`
2. Implement MCP resource interface
3. Register in `ssms_mcp_server.py`
4. Add tests and documentation

### 3. **Database Changes**
1. Update `database_config.py` if needed
2. Modify database classes as required
3. Update environment template
4. Test with both databases

## Deployment Architecture

### 1. Local Development
- Python virtual environment
- Environment variables from `.env` file
- Direct execution with `python main.py`

### 2. Production Deployment
- Docker containerization (future)
- Environment variables from secure store
- Process management with systemd/supervisor

### 3. MCP Integration
- StdIO transport for Cursor/Claude Desktop
- JSON-RPC protocol communication
- Configuration through MCP client settings

## Testing Strategy

### 1. **Unit Tests**
- Test individual components in isolation
- Mock database connections
- Test error scenarios

### 2. **Integration Tests**
- Test with real database connections
- Test MCP protocol compliance
- Test tool and resource functionality

### 3. **End-to-End Tests**
- Test with MCP clients (Cursor/Claude Desktop)
- Test complete workflows
- Test error handling and recovery

## Monitoring and Observability

### 1. Metrics
- Query execution time
- Connection pool statistics
- Error rates and types
- Resource usage

### 2. Logging
- Structured logging with correlation IDs
- Request/response logging
- Error tracking and alerting
- Performance monitoring

### 3. Health Checks
- Database connectivity checks
- MCP server health endpoints
- Resource availability monitoring

## Conclusion

This architecture provides a solid foundation for a scalable, secure, and maintainable MCP server for SQL Server database access. The modular design ensures easy maintenance and extension while following MCP best practices and Python conventions.
