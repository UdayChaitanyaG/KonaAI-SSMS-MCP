# KonaAI SSMS MCP Server

A Model Context Protocol (MCP) server that provides programmatic access to KonaAI SQL Server databases with full CRUD operations on tables, triggers, stored procedures, and views.

## Overview

This MCP server enables AI assistants and development tools to interact with your KonaAI databases through a standardized protocol. It supports both the KonaAI.Master database and the DataManagement database (DIT_GDB) with comprehensive database operations.

## Features

- **Database Access**: Connect to both KonaAI.Master and DIT_GDB databases
- **Table Operations**: List, query, insert, update, and delete table data
- **Stored Procedures**: List, view definitions, and execute stored procedures
- **Triggers**: List and view trigger definitions
- **Views**: List, view definitions, and query view data
- **Schema Exploration**: Comprehensive database schema information
- **Security**: Windows Authentication with SQL injection protection
- **MCP Resources**: Database objects exposed as MCP resources
- **MCP Tools**: Database operations exposed as MCP tools

## Prerequisites

- Node.js 18.0.0 or higher
- Access to KonaAI.Master and DIT_GDB databases
- Windows Authentication enabled

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd KonaAI-SSMS-MCP
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Build the project:**
   ```bash
   npm run build
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root with your database configuration:

```env
# Database Configuration (Updated to match appsettings.json)
MASTER_DB_SERVER=dc-l-
MASTER_DB_NAME=KonaAI
DATA_MGMT_DB_SERVER=dc-l-
DATA_MGMT_DB_NAME=KonaAI

# Query Configuration
QUERY_TIMEOUT=30000
MAX_ROWS=1000

# Logging
LOG_LEVEL=info
```

### Database Connections

The server connects to the KonaAI database:

1. **KonaAI Database**
   - Server: `dc-l-`
   - Database: `KonaAI`
   - Authentication: Windows Authentication
   - Connection String: `Data Source=dc-l-;Initial Catalog=KonaAI;Integrated Security=True;Encrypt=True;Trust Server Certificate=True`

## Usage

### Starting the Server

```bash
npm start
```

### Development Mode

```bash
npm run dev
```

### Watch Mode

```bash
npm run watch
```

## MCP Resources

The server exposes database objects as MCP resources:

### Tables
- **URI Pattern**: `mcp://ssms/{database}/tables/{schema}.{tableName}`
- **Examples**:
  - `mcp://ssms/master/tables/dbo.Clients`
  - `mcp://ssms/datamgmt/tables/dbo.File_Detail`

### Stored Procedures
- **URI Pattern**: `mcp://ssms/{database}/procedures/{schema}.{procedureName}`
- **Examples**:
  - `mcp://ssms/master/procedures/dbo.GetClientData`
  - `mcp://ssms/datamgmt/procedures/dbo.ProcessFile`

### Triggers
- **URI Pattern**: `mcp://ssms/{database}/triggers/{triggerName}`
- **Examples**:
  - `mcp://ssms/master/triggers/ClientAuditTrigger`
  - `mcp://ssms/datamgmt/triggers/FileUpdateTrigger`

### Views
- **URI Pattern**: `mcp://ssms/{database}/views/{schema}.{viewName}`
- **Examples**:
  - `mcp://ssms/master/views/dbo.ClientSummary`
  - `mcp://ssms/datamgmt/views/dbo.FileStatistics`

## MCP Tools

The server provides the following tools for database operations:

### Query Execution
- **Tool**: `executeQuery`
- **Description**: Execute SQL queries on the specified database
- **Parameters**:
  - `database`: 'master' | 'datamgmt'
  - `query`: SQL query string
  - `parameters`: Optional query parameters

### CRUD Operations
- **Tool**: `insertData`
- **Description**: Insert data into a table
- **Parameters**:
  - `database`: 'master' | 'datamgmt'
  - `tableName`: Name of the table
  - `schema`: Schema name (default: 'dbo')
  - `data`: Data to insert

- **Tool**: `updateData`
- **Description**: Update data in a table
- **Parameters**:
  - `database`: 'master' | 'datamgmt'
  - `tableName`: Name of the table
  - `schema`: Schema name (default: 'dbo')
  - `data`: Data to update
  - `whereClause`: WHERE clause for the update
  - `whereParameters`: Parameters for the WHERE clause

- **Tool**: `deleteData`
- **Description**: Delete data from a table
- **Parameters**:
  - `database`: 'master' | 'datamgmt'
  - `tableName`: Name of the table
  - `schema`: Schema name (default: 'dbo')
  - `whereClause`: WHERE clause for the delete
  - `whereParameters`: Parameters for the WHERE clause

### Schema Exploration
- **Tool**: `getSchema`
- **Description**: Get database schema information
- **Parameters**:
  - `database`: 'master' | 'datamgmt'
  - `objectType`: 'tables' | 'procedures' | 'triggers' | 'views' | 'all'

- **Tool**: `getTables`
- **Description**: Get list of tables in the database
- **Parameters**:
  - `database`: 'master' | 'datamgmt'

- **Tool**: `getTableSchema`
- **Description**: Get detailed schema for a specific table
- **Parameters**:
  - `database`: 'master' | 'datamgmt'
  - `tableName`: Name of the table
  - `schema`: Schema name (default: 'dbo')

- **Tool**: `getStoredProcedures`
- **Description**: Get list of stored procedures in the database
- **Parameters**:
  - `database`: 'master' | 'datamgmt'

- **Tool**: `getTriggers`
- **Description**: Get list of triggers in the database
- **Parameters**:
  - `database`: 'master' | 'datamgmt'

- **Tool**: `getViews`
- **Description**: Get list of views in the database
- **Parameters**:
  - `database`: 'master' | 'datamgmt'

## Cursor Integration

To use this MCP server with Cursor, add the following to your workspace `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "ssms": {
      "command": "node",
      "args": ["KonaAI-SSMS-MCP/dist/index.js"],
      "env": {}
    }
  }
}
```

## Security Features

- **Windows Authentication**: Uses integrated security, no credentials in code
- **SQL Injection Protection**: Parameterized queries and input validation
- **Query Timeouts**: Configurable timeouts to prevent long-running queries
- **Operation Logging**: Comprehensive logging of database operations
- **Permission-based Access**: Respects database user permissions

## Error Handling

The server provides comprehensive error handling:

- **Connection Errors**: Database connection failures
- **Query Errors**: SQL syntax and execution errors
- **Permission Errors**: Access denied scenarios
- **Timeout Errors**: Query timeout handling
- **Validation Errors**: Input parameter validation

## Development

### Project Structure

```
KonaAI-SSMS-MCP/
├── src/
│   ├── index.ts              # Main MCP server
│   ├── config.ts             # Database configuration
│   ├── database/
│   │   ├── master-db.ts      # KonaAI.Master connection
│   │   └── data-mgmt-db.ts   # DIT_GDB connection
│   ├── resources/
│   │   ├── tables.ts         # Table resources
│   │   ├── procedures.ts     # Stored procedure resources
│   │   ├── triggers.ts       # Trigger resources
│   │   └── views.ts          # View resources
│   └── tools/
│       ├── query.ts          # Execute SQL queries
│       ├── crud.ts           # CRUD operations
│       └── schema.ts         # Schema exploration
├── dist/                     # Compiled JavaScript
├── package.json
├── tsconfig.json
└── README.md
```

### Building

```bash
npm run build
```

### Development

```bash
npm run dev
```

### Watching Changes

```bash
npm run watch
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Verify server names and database names
   - Check Windows Authentication permissions
   - Ensure SQL Server is running and accessible

2. **Build Errors**
   - Run `npm install` to ensure all dependencies are installed
   - Check TypeScript configuration in `tsconfig.json`

3. **Permission Errors**
   - Verify database user has appropriate permissions
   - Check Windows Authentication settings

4. **Query Timeouts**
   - Adjust `QUERY_TIMEOUT` in environment variables
   - Optimize queries for better performance

### Logs

The server logs all operations to the console. Check the output for detailed error information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review the logs for error details
- Ensure all prerequisites are met
- Verify database connectivity
