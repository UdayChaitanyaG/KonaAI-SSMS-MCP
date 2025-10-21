# SSMS MCP Server - Configuration Update

## ✅ Database Configuration Updated

The SSMS MCP server has been updated to match the new database configuration from `appsettings.json`.

### Previous Configuration
- **Master DB**: `DC-L-0004\\MSSQLSERVER02` → `KonaAI_Master`
- **DataManagement DB**: `dc-l-` → `DIT_GDB`

### Updated Configuration
- **Server**: `dc-l-`
- **Database**: `KonaAI`
- **Authentication**: Windows Authentication
- **Connection String**: `Data Source=dc-l-;Initial Catalog=KonaAI;Integrated Security=True;Encrypt=True;Trust Server Certificate=True`

## 🔧 Changes Made

### 1. Configuration Files Updated
- ✅ `src/config.ts` - Updated default database settings
- ✅ `README.md` - Updated documentation
- ✅ `demo-client.js` - Updated examples

### 2. Database Connections
Both `master` and `datamgmt` database references now point to the same KonaAI database:
- **master**: `dc-l-` → `KonaAI`
- **datamgmt**: `dc-l-` → `KonaAI`

### 3. Environment Variables
```env
MASTER_DB_SERVER=dc-l-
MASTER_DB_NAME=KonaAI
DATA_MGMT_DB_SERVER=dc-l-
DATA_MGMT_DB_NAME=KonaAI
```

## 🚀 Ready to Use

The MCP server is now configured to connect to your updated KonaAI database setup. You can:

1. **List tables**: Ask Cursor to "list all tables in the master database"
2. **Explore schema**: Request "show me the schema for the Clients table"
3. **Execute queries**: Run queries like "get all clients from the database"
4. **CRUD operations**: Perform insert, update, delete operations

## 🔍 Testing the Connection

Run the demo to verify the configuration:
```bash
node demo-client.js
```

The server is ready to provide full access to your KonaAI database through the Model Context Protocol!
