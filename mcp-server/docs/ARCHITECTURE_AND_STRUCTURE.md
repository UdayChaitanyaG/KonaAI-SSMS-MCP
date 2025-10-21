# SSMS MCP Server - Complete Documentation

## 🎯 **Overview**

The SSMS MCP Server is a comprehensive Model Context Protocol (MCP) server that provides enhanced SQL Server database access capabilities through Python. It supports both Master and Data Management databases with Windows Authentication.

## 🚀 **Quick Start**

### **1. Test Database Connection**
```bash
cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
python tests/test_connection.py
```

### **2. Start MCP Server**
```bash
python main.py
```

### **3. Configure Cursor**
Add to your Cursor MCP configuration:
```json
{
  "mcpServers": {
    "konaai-ssms": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "C:\\Users\\UdayChaitanyaGurvind\\Desktop\\KonaAi\\KonaAI Web Application\\KonaAI-SSMS-MCP\\mcp-server",
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

## 📊 **Available Databases**

### **Master Database (KonaAI) - 29 Tables**
- **App Schema**: Client, User, UserAudit
- **Client Schema**: ClientLicense, ClientProject
- **ClientUserMetaData Schema**: Various audit tables

### **Data Management Database (DIT_GDB) - 367 Tables**
- **Analytics Schema**: COIDetails, COIHeader, CustomerAddress, CustomerMaster, DistributorMaster
- **Customer Schema**: Customer-related tables
- **Analytics Schema**: Analytics and reporting tables

## 🛠️ **MCP Tools**

### **Query Tool**
Execute SQL queries on both databases:
```
Query Master database: SELECT TOP 10 * FROM App.Client
Query Data Management database: SELECT TOP 10 * FROM Analytics.CustomerMaster
```

### **CRUD Tool**
Perform CRUD operations:
```
Create: Create a new record in App.Client with Name='Test Client'
Read: Read all records from App.Client where IsActive=1
Update: Update App.Client set Name='Updated Name' where Id=1
Delete: Delete from App.Client where Id=1
```

### **Schema Tool**
Analyze database schema:
```
Get table schema: Show schema for App.Client
List tables: List all tables in Master database
Get relationships: Show foreign keys for App.Client
```

### **Stored Procedure Tool**
Execute stored procedures:
```
Execute procedure: Execute sp_GetClientInfo with parameter @ClientId=1
List procedures: Show all stored procedures in Master database
```

## 📚 **MCP Resources**

### **Tables Resource**
Access table metadata:
```
List all tables in Master database
Show table metadata for App.Client
Get table statistics for Analytics.CustomerMaster
```

### **Procedures Resource**
Access stored procedure information:
```
List all stored procedures in Master database
Show procedure information for sp_GetClientInfo
Get procedure usage statistics
```

### **Triggers Resource**
Access trigger information:
```
List all triggers in Master database
Show trigger information for Client.ClientProject
Get trigger dependencies
```

### **Views Resource**
Access view information:
```
List all views in Data Management database
Show view definition for Analytics.CustomerView
Get view dependencies
```

## 🏗️ **Architecture**

### **System Architecture**
```
MCP Client (Cursor/Claude)
        ↓ MCP Protocol (JSON-RPC)
SSMS MCP Server
        ↓ Database Operations
Database Layer (Master DB + Data Mgmt DB)
        ↓ SQL Server Connection
SQL Server (DC-L-)
```

### **Component Structure**
```
mcp-server/
├── src/
│   ├── config/           # Configuration management
│   │   ├── app_config.py      # Centralized application configuration
│   │   └── database_config.py # Database configuration with Windows Auth
│   └── server/           # MCP server implementation
│       ├── ssms_mcp_server.py # Main MCP server class
│       ├── database/          # Database connection classes
│       │   ├── base.py        # Base database class with connection pooling
│       │   ├── master_db.py   # Master database operations (KonaAI)
│       │   └── datamgmt_db.py # Data management database operations (DIT_GDB)
│       ├── tools/             # MCP tools implementation
│       │   ├── query_tool.py  # SQL query execution tool
│       │   ├── crud_tool.py   # CRUD operations tool
│       │   ├── schema_tool.py # Schema introspection tool
│       │   └── sp_tool.py     # Stored procedure execution tool
│       └── resources/         # MCP resources implementation
│           ├── tables.py      # Tables resource (metadata)
│           ├── procedures.py # Stored procedures resource
│           ├── triggers.py   # Database triggers resource
│           └── views.py      # Database views resource
├── tests/                # Test files directory
│   └── test_connection.py # Database connection test
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
└── mcp_config.json      # MCP client configuration
```

## 🔧 **Configuration**

### **Database Configuration**
The server uses Windows Authentication with the following databases:
- **Master Database**: KonaAI (29 tables)
- **Data Management Database**: DIT_GDB (367 tables)

### **Connection Settings**
- **Server**: DC-L-
- **Authentication**: Windows Authentication (Trusted Connection)
- **Connection Pooling**: Enabled for efficient connection management

## 🔒 **Security Features**

### **Authentication**
- **Windows Authentication**: Primary authentication method
- **Trusted Connection**: Secure database access without password storage
- **No Credential Storage**: Credentials not stored in application code

### **Data Protection**
- **Parameterized Queries**: All queries use parameterization to prevent SQL injection
- **Input Validation**: All inputs validated before processing
- **Error Handling**: Secure error reporting without information leakage
- **Connection Security**: Encrypted connections with certificate trust

## 📈 **Performance Features**

### **Connection Management**
- **Connection Pooling**: Efficient database connection management
- **Pool Configuration**: Configurable pool size and timeouts
- **Connection Reuse**: Reuse connections for multiple operations
- **Automatic Cleanup**: Automatic connection cleanup and recovery

### **Query Optimization**
- **Parameterized Queries**: Optimized query execution
- **Result Limiting**: Configurable row limits to prevent memory issues
- **Query Caching**: Intelligent caching for frequently accessed data
- **Performance Monitoring**: Query execution time tracking

## 🧪 **Testing**

### **Connection Test**
```bash
python tests/test_connection.py
```

### **Expected Output**
```
SSMS MCP Server - Database Connection Test
============================================================
Testing Master Database Connection...
Master Database: 29 tables found
First 5 tables in Master Database:
   1. Client (Schema: App)
   2. User (Schema: App)
   3. UserAudit (Schema: App)
   4. ClientLicense (Schema: Client)
   5. ClientProject (Schema: Client)

Testing Data Management Database Connection...
Data Management Database: 367 tables found
First 5 tables in Data Management Database:
   1. COIDetails (Schema: Analytics)
   2. COIHeader (Schema: Analytics)
   3. CustomerAddress (Schema: Analytics)
   4. CustomerMaster (Schema: Analytics)
   5. DistributorMaster (Schema: Analytics)

Database connection test completed successfully!
```

## 🚀 **Usage Examples**

### **Database Queries**
```
Query Master database: SELECT TOP 5 * FROM App.Client
Query Data Management database: SELECT TOP 5 * FROM Analytics.CustomerMaster
Count active users: SELECT COUNT(*) FROM App.User WHERE IsActive=1
```

### **Schema Exploration**
```
List all tables: SELECT TABLE_NAME, TABLE_SCHEMA FROM INFORMATION_SCHEMA.TABLES
Get table schema: Show schema for App.Client
Get relationships: Show foreign keys for App.Client
```

### **Natural Language Queries**
```
Show me all clients from the App schema
Get the first 10 customers from the Analytics schema
Count how many users are active
Show me the schema for the Client table
```

## 🔍 **Troubleshooting**

### **Common Issues**

#### **MCP Server Not Starting**
```bash
# Check if Python is in PATH
python --version

# Check if dependencies are installed
pip list | grep mcp

# Test the server manually
python main.py
```

#### **Database Connection Issues**
```bash
# Test database connection
python tests/test_connection.py

# Check SQL Server is running
# Verify Windows Authentication is enabled
```

#### **Cursor Not Recognizing MCP Server**
- Check Cursor's MCP settings
- Verify the configuration JSON is correct
- Restart Cursor after configuration changes
- Check Cursor's logs for MCP errors

### **Debug Steps**

#### **Check Server Logs**
```bash
# Run server with verbose logging
python main.py --verbose
```

#### **Test Individual Components**
```bash
# Test database connection
python tests/test_connection.py

# Test MCP server initialization
python -c "from src.server.ssms_mcp_server import SSMSServer; server = SSMSServer(); print('Server initialized successfully')"
```

## 📞 **Support**

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Test the connection with `python tests/test_connection.py`
4. Check Cursor's MCP server status
5. Review the logs for any error messages

---

**Your SSMS MCP Server is now ready to use with Cursor! You can query your databases using natural language directly in the IDE! 🚀**