# SSMS MCP Server - Cursor Quick Reference

## 🚀 **Quick Setup (Already Done!)**

Your MCP server is ready! Here's the configuration for Cursor:

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

## 🎯 **How to Use in Cursor**

### **1. Database Queries**
```
Query Master database: SELECT TOP 10 * FROM App.Client
Query Data Management database: SELECT TOP 10 * FROM Analytics.CustomerMaster
Get table count: SELECT COUNT(*) FROM App.Client
```

### **2. CRUD Operations**
```
Create: Create a new record in App.Client with Name='Test Client'
Read: Read all records from App.Client where IsActive=1
Update: Update App.Client set Name='Updated Name' where Id=1
Delete: Delete from App.Client where Id=1
```

### **3. Schema Operations**
```
Get table schema: Show schema for App.Client
List tables: List all tables in Master database
Get columns: Show columns for App.Client table
Get relationships: Show foreign keys for App.Client
```

### **4. Stored Procedures**
```
Execute procedure: Execute sp_GetClientInfo with parameter @ClientId=1
List procedures: Show all stored procedures in Master database
Get procedure info: Show parameters for sp_GetClientInfo
```

## 📊 **Available Databases**

### **Master Database (KonaAI) - 29 Tables**
- **App Schema**: Client, User, UserAudit
- **Client Schema**: ClientLicense, ClientProject
- **ClientUserMetaData Schema**: ClientProjectAuditResponsibility, etc.

### **Data Management Database (DIT_GDB) - 367 Tables**
- **Analytics Schema**: COIDetails, COIHeader, CustomerAddress, CustomerMaster, DistributorMaster
- **Customer Schema**: Customer-related tables
- **Analytics Schema**: Analytics and reporting tables

## 🔧 **Common Commands**

### **Quick Queries**
```
Show first 5 clients: SELECT TOP 5 * FROM App.Client
Count active users: SELECT COUNT(*) FROM App.User WHERE IsActive=1
Get customer data: SELECT TOP 10 * FROM Analytics.CustomerMaster
List all schemas: SELECT DISTINCT TABLE_SCHEMA FROM INFORMATION_SCHEMA.TABLES
```

### **Data Analysis**
```
Get table sizes: SELECT 
    t.NAME AS TableName,
    s.Name AS SchemaName,
    p.rows AS RowCounts
FROM sys.tables t
INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
INNER JOIN sys.partitions p ON t.object_id = p.object_id
WHERE p.index_id IN (0,1)
ORDER BY p.rows DESC

Get column information: SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE,
    CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Client'
```

### **Schema Exploration**
```
List all tables: SELECT TABLE_NAME, TABLE_SCHEMA FROM INFORMATION_SCHEMA.TABLES
Get foreign keys: SELECT 
    fk.name AS ForeignKeyName,
    tp.name AS ParentTable,
    cp.name AS ParentColumn,
    tr.name AS ReferencedTable,
    cr.name AS ReferencedColumn
FROM sys.foreign_keys fk
INNER JOIN sys.tables tp ON fk.parent_object_id = tp.object_id
INNER JOIN sys.tables tr ON fk.referenced_object_id = tr.object_id
INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
INNER JOIN sys.columns cp ON fkc.parent_column_id = cp.column_id AND fkc.parent_object_id = cp.object_id
INNER JOIN sys.columns cr ON fkc.referenced_column_id = cr.column_id AND fkc.referenced_object_id = cr.object_id
```

## 🎯 **Pro Tips**

### **1. Use Natural Language**
Instead of: `SELECT * FROM App.Client`
Try: `Show me all clients from the App schema`

### **2. Ask for Explanations**
- `Explain the App.Client table structure`
- `What are the relationships for the Client table?`
- `Show me the indexes on the User table`

### **3. Get Help with Queries**
- `Help me write a query to find active clients`
- `How do I join the Client and User tables?`
- `What's the best way to query customer data?`

### **4. Explore Your Data**
- `What tables are available in the Master database?`
- `Show me the largest tables in the Data Management database`
- `What stored procedures are available?`

## 🔍 **Troubleshooting**

### **If MCP Server Doesn't Work:**
1. Check Cursor's MCP server status
2. Verify the server is listed as "konaai-ssms"
3. Restart Cursor if needed
4. Test manually: `python tests/test_connection.py`

### **If Queries Fail:**
1. Check table names and schemas
2. Verify you're using the correct database
3. Check for typos in column names
4. Use `SELECT TOP 1 * FROM [table]` to test

### **Common Issues:**
- **Table not found**: Check schema name (App.Client, not just Client)
- **Permission denied**: Verify Windows Authentication
- **Connection timeout**: Check SQL Server is running

## 📞 **Quick Help**

### **Test Your Setup:**
```bash
cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
python tests/test_connection.py
```

### **Start Server Manually:**
```bash
cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
python main.py
```

### **Check Server Status:**
Look for "konaai-ssms" in Cursor's MCP server list

---

**You're all set! Start exploring your databases with natural language in Cursor! 🚀**