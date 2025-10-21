# SSMS MCP Server - Cursor Setup Guide

## 🎯 **Setting up SSMS MCP Server with Cursor**

This guide will help you configure the SSMS MCP Server to work with Cursor IDE.

## 📋 **Prerequisites**

### 1. **Python Environment**
- Python 3.10+ installed
- All dependencies installed (`pip install -r requirements.txt`)

### 2. **Database Access**
- SQL Server running on `DC-L-`
- Windows Authentication enabled
- Access to `KonaAI` and `DIT_GDB` databases

### 3. **Cursor IDE**
- Cursor IDE installed
- MCP support enabled

## 🔧 **Step 1: Verify MCP Server Works**

### Test the Connection
```bash
cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
python tests/test_connection.py
```

**Expected Output:**
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

## 🔧 **Step 2: Configure Cursor MCP Settings**

### 1. **Open Cursor Settings**
- Press `Ctrl + ,` (or `Cmd + ,` on Mac)
- Go to **Settings**
- Search for **"MCP"** or **"Model Context Protocol"**

### 2. **Add MCP Server Configuration**
In Cursor's MCP settings, add the following configuration:

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

### 3. **Alternative: Use Configuration File**
You can also use the provided `mcp_config.json` file:

1. Copy the contents of `mcp_config.json`
2. Paste into Cursor's MCP server configuration
3. Save the settings

## 🔧 **Step 3: Start the MCP Server**

### Method 1: Manual Start
```bash
cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
python main.py
```

### Method 2: Let Cursor Start It
- Cursor will automatically start the MCP server when needed
- The server will run in the background

## 🔧 **Step 4: Verify MCP Integration**

### 1. **Check MCP Server Status**
- Look for MCP server status in Cursor's status bar
- Should show "konaai-ssms" as connected

### 2. **Test MCP Tools**
In Cursor, you can now use the following MCP tools:

#### **Query Tool**
```
Execute SQL query on Master database: SELECT TOP 5 * FROM App.Client
Execute SQL query on Data Management database: SELECT TOP 5 * FROM Analytics.CustomerMaster
```

#### **CRUD Tool**
```
Create a new record in App.Client table
Read records from Analytics.CustomerMaster table
Update a record in Client.ClientProject table
Delete a record from App.User table
```

#### **Schema Tool**
```
Get schema information for App.Client table
List all columns in Analytics.CustomerMaster table
Show relationships for Client.ClientProject table
```

#### **Stored Procedure Tool**
```
Execute stored procedure: sp_GetClientInfo
List all stored procedures in Master database
Show stored procedure parameters for sp_GetUserData
```

### 3. **Test MCP Resources**
You can also access MCP resources:

#### **Tables Resource**
```
List all tables in Master database
Show table metadata for App.Client
Get table statistics for Analytics.CustomerMaster
```

#### **Procedures Resource**
```
List all stored procedures in Master database
Show procedure information for sp_GetClientInfo
Get procedure usage statistics
```

#### **Triggers Resource**
```
List all triggers in Master database
Show trigger information for Client.ClientProject
Get trigger dependencies
```

#### **Views Resource**
```
List all views in Data Management database
Show view definition for Analytics.CustomerView
Get view dependencies
```

## 🚀 **Step 5: Using the MCP Server**

### **Available Commands in Cursor**

#### **Database Queries**
- **Query Master Database**: `Execute SQL query on Master database: [your query]`
- **Query Data Management Database**: `Execute SQL query on Data Management database: [your query]`
- **Cross-Database Queries**: Use both databases in your queries

#### **Data Operations**
- **Create Records**: `Create a new record in [table] with [data]`
- **Read Records**: `Read records from [table] where [conditions]`
- **Update Records**: `Update record in [table] set [changes] where [conditions]`
- **Delete Records**: `Delete record from [table] where [conditions]`

#### **Schema Operations**
- **Get Table Schema**: `Get schema for [table] in [database]`
- **List Tables**: `List all tables in [database]`
- **Get Relationships**: `Show relationships for [table]`
- **Get Indexes**: `Show indexes for [table]`

#### **Stored Procedures**
- **Execute Procedures**: `Execute stored procedure [name] with parameters [params]`
- **List Procedures**: `List all stored procedures in [database]`
- **Get Procedure Info**: `Show information for stored procedure [name]`

## 🔍 **Troubleshooting**

### **Common Issues**

#### 1. **MCP Server Not Starting**
```bash
# Check if Python is in PATH
python --version

# Check if dependencies are installed
pip list | grep mcp

# Test the server manually
python main.py
```

#### 2. **Database Connection Issues**
```bash
# Test database connection
python tests/test_connection.py

# Check SQL Server is running
# Verify Windows Authentication is enabled
```

#### 3. **Cursor Not Recognizing MCP Server**
- Check Cursor's MCP settings
- Verify the configuration JSON is correct
- Restart Cursor after configuration changes
- Check Cursor's logs for MCP errors

### **Debug Steps**

#### 1. **Check Server Logs**
```bash
# Run server with verbose logging
python main.py --verbose
```

#### 2. **Test Individual Components**
```bash
# Test database connection
python tests/test_connection.py

# Test MCP server initialization
python -c "from src.server.ssms_mcp_server import SSMSServer; server = SSMSServer(); print('Server initialized successfully')"
```

#### 3. **Verify Cursor Configuration**
- Check Cursor's MCP server list
- Verify the server is listed as "konaai-ssms"
- Check if the server status shows as "Connected"

## 📊 **Expected Results**

### **Successful Setup Indicators**
- ✅ MCP server starts without errors
- ✅ Database connections work (29 + 367 tables)
- ✅ Cursor shows MCP server as connected
- ✅ You can use MCP tools in Cursor
- ✅ Database queries work through Cursor

### **Available Databases**
- **Master Database (KonaAI)**: 29 tables
  - App.Client, App.User, App.UserAudit
  - Client.ClientLicense, Client.ClientProject
  - ClientUserMetaData.* tables

- **Data Management Database (DIT_GDB)**: 367 tables
  - Analytics.COIDetails, Analytics.COIHeader
  - Analytics.CustomerAddress, Analytics.CustomerMaster
  - Analytics.DistributorMaster

## 🎉 **Success!**

Once configured, you can use the SSMS MCP Server directly in Cursor to:

- **Query your databases** using natural language
- **Perform CRUD operations** on your data
- **Explore database schemas** and relationships
- **Execute stored procedures** with parameters
- **Access database metadata** and statistics

**Your SSMS MCP Server is now integrated with Cursor! 🚀**

## 📞 **Support**

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Test the connection with `python tests/test_connection.py`
4. Check Cursor's MCP server status
5. Review the logs for any error messages

---

**Happy coding with your SSMS MCP Server in Cursor! 🎯**