# Environment Configuration Setup

The MCP server now reads all configuration from a `.env` file instead of hardcoded values.

## Configuration Files

### `.env` File
The `.env` file contains all sensitive database credentials and settings. This file is:
- ✅ **NOT committed to git** (already in `.gitignore`)
- ✅ **Loaded automatically** when the server starts
- ✅ **Easy to update** without changing code

### Location
The `.env` file should be in the `mcp-server` directory:
```
KonaAI-SSMS-MCP/mcp-server/.env
```

## Current Configuration

The `.env` file contains:
- **Master Database**: `KonaAI_Master` on server `17.0.1050.2`
- **Data Management Database**: `KonaAI_Master_001` on server `17.0.1050.2`
- **Username**: `SSMSLOGIN`
- **Password**: `LoginPassword123`

## How It Works

1. **On Server Start**: The `app_config.py` automatically loads the `.env` file using `python-dotenv`
2. **Configuration Reading**: All values are read from environment variables
3. **No Hardcoding**: No credentials are hardcoded in the source code

## Files Updated

### `src/config/app_config.py`
- ✅ Removed hardcoded credentials
- ✅ Reads from environment variables
- ✅ Automatically loads `.env` file

### `src/config/database_config.py`
- ✅ Uses Pydantic Settings (already supports `.env`)
- ✅ Removed hardcoded default values
- ✅ Reads from environment variables

## Verification

To verify your configuration is loaded correctly:

```bash
py verify_env.py
```

This will show:
- Which configuration source is being used
- All database settings
- Application settings
- Any missing configurations

## Updating Configuration

### Method 1: Edit .env File Directly
1. Open `mcp-server/.env` in a text editor
2. Update the values you need
3. Save the file
4. Restart the MCP server

### Method 2: Create New .env File
```bash
py create_env.py
```

This will create a `.env` file with the current default values.

## Environment Variables

The following environment variables are used:

### Master Database
- `MASTER_DB_SERVER` - SQL Server instance name/IP
- `MASTER_DB_NAME` - Database name
- `MASTER_DB_USER` - Username
- `MASTER_DB_PASSWORD` - Password

### Data Management Database
- `DATA_MGMT_DB_SERVER` - SQL Server instance name/IP
- `DATA_MGMT_DB_NAME` - Database name
- `DATA_MGMT_DB_USER` - Username
- `DATA_MGMT_DB_PASSWORD` - Password

### Application Settings
- `QUERY_TIMEOUT` - Query timeout in seconds (default: 30)
- `MAX_ROWS` - Maximum rows to return (default: 1000)
- `LOG_LEVEL` - Logging level (default: INFO)
- `MAX_CONNECTIONS` - Maximum connections in pool (default: 10)
- `CONNECTION_TIMEOUT` - Connection timeout in seconds (default: 15)

## Security Notes

1. **Never commit `.env` to git** - It's already in `.gitignore`
2. **Use strong passwords** in production
3. **Restrict file permissions** on `.env` file
4. **Use different credentials** for different environments (dev/staging/prod)

## Troubleshooting

### Configuration Not Loading

If configuration is not loading:

1. **Check .env file exists**:
   ```bash
   ls .env
   ```

2. **Verify .env file location**:
   The file should be in `mcp-server/.env` (same directory as `main.py`)

3. **Check file format**:
   - Use `KEY=VALUE` format
   - No spaces around `=`
   - One variable per line
   - No quotes needed (unless value contains spaces)

4. **Run verification**:
   ```bash
   py verify_env.py
   ```

### Missing Values

If values show as "(not set)":

1. Check `.env` file has all required variables
2. Verify variable names match exactly (case-sensitive in some systems)
3. Ensure no extra spaces or special characters
4. Restart the server after updating `.env`

## Example .env File

```env
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
MAX_CONNECTIONS=10
CONNECTION_TIMEOUT=15
```

## Benefits

✅ **Security**: No credentials in source code  
✅ **Flexibility**: Easy to change without code changes  
✅ **Environment-specific**: Different `.env` files for dev/staging/prod  
✅ **Version Control Safe**: `.env` is in `.gitignore`  
✅ **Standard Practice**: Follows 12-factor app principles
