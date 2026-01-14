# KonaAI SSMS MCP Server

A Model Context Protocol (MCP) server for SQL Server Management Studio integration, providing enhanced database access capabilities through Cursor IDE.

## Features

- 🔍 **Query Execution**: Execute SQL queries against Master and Data Management databases
- 📊 **CRUD Operations**: Insert, update, and delete data with validation
- 🗂️ **Schema Discovery**: Browse tables, views, stored procedures, and triggers
- 🔧 **Stored Procedures**: Execute and inspect stored procedures
- 📚 **Resources**: Access database objects as MCP resources
- 🔐 **Windows Authentication**: Secure connection using Windows Authentication

## Quick Start

### Prerequisites

- Python 3.8 or higher
- SQL Server with Windows Authentication enabled
- Access to KonaAI Master database (`KonaAI`)
- Access to Data Management database (`DIT_GDB`)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd KonaAI-SSMS-MCP/mcp-server
   ```

2. **Run the automated setup script:**
   ```bash
   python setup_mcp.py
   ```
   
   This script will:
   - ✅ Auto-detect Python executable
   - ✅ Check and install dependencies
   - ✅ Test server startup
   - ✅ Generate Cursor MCP configuration
   - ✅ Provide setup instructions

3. **Or install manually:**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Edit `src/config/app_config.py` to configure your database connections:

```python
DATABASE_SERVERS = {
    'master': {
        'server': 'YOUR_SERVER_NAME',
        'database': 'KonaAI',
    },
    'datamgmt': {
        'server': 'YOUR_SERVER_NAME',
        'database': 'DIT_GDB',
    }
}
```

**Note**: The server uses Windows Authentication by default (no username/password required).

### Testing

Test the server startup:

```bash
python test_mcp_startup.py
```

Or test the connection manually:

```bash
python main.py
```

## Cursor IDE Integration

### Automatic Setup

1. Run the setup script:
   ```bash
   python setup_mcp.py
   ```

2. Follow the printed instructions to add the configuration to Cursor

### Manual Setup

1. **Open Cursor IDE**

2. **Open MCP Settings:**
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
   - Type "MCP" and select "MCP: Add Server Configuration"

3. **Add Configuration:**
   
   Copy the configuration from `cursor_mcp_config.json`:
   
   ```json
   {
     "mcpServers": {
       "konaai-ssms": {
         "command": "python",
         "args": ["-u", "C:\\full\\path\\to\\mcp-server\\main.py"],
         "cwd": "C:\\full\\path\\to\\mcp-server",
         "env": {
           "PYTHONPATH": "C:\\full\\path\\to\\mcp-server",
           "PYTHONUNBUFFERED": "1"
         }
       }
     }
   }
   ```
   
   **Important**: Replace the paths with your actual project path!

4. **Restart Cursor IDE**

5. **Verify Connection:**
   - The `konaai-ssms` server should appear in Cursor's MCP server list
   - You can now use MCP tools and resources in your conversations

### Troubleshooting Cursor Integration

**Issue**: "The system cannot find the path specified"

**Solution**: 
- Run `python setup_mcp.py` to auto-detect Python
- Or manually edit `cursor_mcp_config.json` with the correct Python path
- Ensure the `cwd` path is correct and uses forward slashes or escaped backslashes

**Issue**: "Client error for command spawn"

**Solution**:
- Verify Python is installed and in PATH: `python --version`
- Check that the Python path in config is correct
- Try using `py` launcher on Windows instead of `python`

**Issue**: "No server info found"

**Solution**:
- Ensure the server can start: `python test_mcp_startup.py`
- Check database connection settings
- Verify all dependencies are installed: `pip list`

## Available Tools

### Query Tools
- `execute_query`: Execute SQL queries against databases

### CRUD Tools
- `insert_data`: Insert data into tables
- `update_data`: Update existing records
- `delete_data`: Delete records

### Schema Tools
- `get_schema`: Get database schema information
- `get_tables`: List all tables
- `get_table_schema`: Get detailed table schema
- `get_stored_procedures`: List stored procedures
- `get_triggers`: List triggers
- `get_views`: List views

### Stored Procedure Tools
- `execute_procedure`: Execute stored procedures
- `get_procedure_info`: Get stored procedure details

## Available Resources

- `ssms://master/tables/*`: Master database tables
- `ssms://datamgmt/tables/*`: Data Management database tables
- `ssms://master/procedures/*`: Master database stored procedures
- `ssms://datamgmt/procedures/*`: Data Management database stored procedures
- `ssms://master/triggers/*`: Master database triggers
- `ssms://datamgmt/triggers/*`: Data Management database triggers
- `ssms://master/views/*`: Master database views
- `ssms://datamgmt/views/*`: Data Management database views

## Development

### Project Structure

```
mcp-server/
├── main.py                 # Entry point
├── setup_mcp.py           # Advanced setup script
├── launch_mcp.bat         # Windows launcher
├── requirements.txt       # Dependencies
├── pyproject.toml         # Project metadata
├── src/
│   ├── config/           # Configuration
│   │   ├── app_config.py
│   │   └── database_config.py
│   └── server/           # MCP server implementation
│       ├── ssms_mcp_server.py
│       ├── database/     # Database connections
│       ├── tools/        # MCP tools
│       └── resources/    # MCP resources
└── tests/                # Test scripts
```

### Running Tests

```bash
python test_mcp_startup.py
```

### Manual Server Start

```bash
python main.py
```

Or on Windows:

```bash
launch_mcp.bat
```

## Troubleshooting

### Database Connection Issues

1. **Verify SQL Server is running**
2. **Check Windows Authentication is enabled**
3. **Verify database names are correct** in `src/config/app_config.py`
4. **Check server name** matches your SQL Server instance

### Python Issues

1. **Verify Python version**: `python --version` (should be 3.8+)
2. **Reinstall dependencies**: `pip install -r requirements.txt --force-reinstall`
3. **Check Python path** in `cursor_mcp_config.json`

### MCP Protocol Issues

1. **Check server logs** for error messages
2. **Verify MCP package version**: `pip show mcp`
3. **Test server startup**: `python test_mcp_startup.py`

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review error messages in Cursor's MCP logs
3. Run `python setup_mcp.py` to verify configuration

## License

MIT License - See LICENSE file for details
