# Quick Start: Connect SSMS-MCP to Cursor

## ✅ Pre-Flight Check (All Verified)

- ✅ Python 3.10.10 installed
- ✅ MCP 1.16.0 installed
- ✅ Database connections working (29 + 367 tables)
- ✅ All MCP tools and resources registered
- ✅ Server initialization successful

**Your MCP server is ready! Just need to connect it to Cursor.**

---

## 🚀 3-Step Setup

### Step 1: Copy MCP Configuration

**Copy this JSON configuration:**

```json
{
  "mcpServers": {
    "konaai-ssms": {
      "command": "C:\\Program Files\\KonaAI_ML\\.pyenv\\pyenv-win\\shims\\python.bat",
      "args": ["-u", "main.py"],
      "cwd": "C:\\Users\\UdayChaitanyaGurvind\\Desktop\\KonaAi\\KonaAI Web Application\\KonaAI-SSMS-MCP\\mcp-server",
      "env": {
        "PYTHONPATH": ".",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**(OR use the file: `cursor_mcp_config.json` - already created for you)**

### Step 2: Add to Cursor Settings

**Option A: Via Cursor Settings UI**

1. Open Cursor
2. Press `Ctrl + ,` (Settings)
3. Search for "MCP" in the search bar
4. Look for "MCP Servers" or "Model Context Protocol" section
5. Click "Edit in settings.json"
6. Paste the configuration above
7. Save the file

**Option B: Via Command Palette**

1. Open Cursor
2. Press `Ctrl + Shift + P` (Command Palette)
3. Type: `Preferences: Open User Settings (JSON)`
4. Add the `mcpServers` configuration to your settings
5. Save the file

**Option C: Direct File Edit**

1. Navigate to: `%APPDATA%\Cursor\User\`
2. Open `settings.json` in any text editor
3. Add the `mcpServers` configuration
4. Save the file

### Step 3: Restart Cursor and Enable

1. **Close Cursor completely** (File → Exit)
2. **Restart Cursor**
3. Look for **"konaai-ssms"** in the bottom status bar or extensions panel
4. **Toggle the switch to ON** (as shown in your screenshot)
5. Wait a few seconds for connection

---

## ✅ Verify Connection

Once connected, you should see:

### Tools Available (11)
- ✅ execute_query - Execute SQL queries
- ✅ insert_data - Insert data into tables
- ✅ update_data - Update data in tables
- ✅ delete_data - Delete data from tables
- ✅ get_schema - Get database schema
- ✅ get_tables - List all tables
- ✅ get_table_schema - Get table details
- ✅ get_stored_procedures - List stored procedures
- ✅ get_triggers - List triggers
- ✅ get_views - List views
- ✅ execute_procedure - Execute stored procedures

### Resources Available
- ✅ Master Database (29 tables)
- ✅ Data Management Database (367 tables)
- ✅ Stored procedures, triggers, views

---

## 🎯 Test Your Connection

Once enabled, try these commands in Cursor:

### Test 1: List Tables
```
Show me all tables in the Master database
```

Expected: Should list 29 tables from App, Client, and ClientUserMetaData schemas

### Test 2: Query Data
```
Execute: SELECT TOP 5 * FROM App.Client
```

Expected: Should return first 5 rows from Client table

### Test 3: Get Schema
```
Show me the schema for App.Client table
```

Expected: Should show columns, data types, constraints

### Test 4: List Procedures
```
What stored procedures are available in the Master database?
```

Expected: Should list all stored procedures

---

## 🔧 Troubleshooting

### Issue: Still Shows "No tools, prompts, or resources"

**Solution 1: Check Cursor's Developer Console**
1. Press `Ctrl + Shift + I` (or `Cmd + Opt + I` on Mac)
2. Go to "Console" tab
3. Look for MCP-related errors
4. Check if server is starting

**Solution 2: Test Server Manually**
1. Open PowerShell
2. Run:
   ```powershell
   cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
   python main.py
   ```
3. If it starts without errors, server is working
4. Press `Ctrl + C` to stop

**Solution 3: Check MCP Server Status**
1. In Cursor, look at bottom status bar
2. Click on "konaai-ssms" if visible
3. Check connection status
4. Look for error messages

### Issue: Cursor Can't Start Server

**Solution: Use Batch File Launcher**
1. Use the provided `start_mcp.bat` file
2. Update Cursor configuration:
   ```json
   {
     "mcpServers": {
       "konaai-ssms": {
         "command": "C:\\Users\\UdayChaitanyaGurvind\\Desktop\\KonaAi\\KonaAI Web Application\\KonaAI-SSMS-MCP\\mcp-server\\start_mcp.bat",
         "args": [],
         "cwd": "C:\\Users\\UdayChaitanyaGurvind\\Desktop\\KonaAi\\KonaAI Web Application\\KonaAI-SSMS-MCP\\mcp-server"
       }
     }
   }
   ```

### Issue: MCP Server Crashes

**Check logs in Cursor:**
1. Open Command Palette: `Ctrl + Shift + P`
2. Type: "Developer: Show Logs"
3. Look for MCP server output/errors

**Or create a log file:**
```powershell
cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
python main.py 2>&1 | Tee-Object -FilePath mcp_server.log
```
Check `mcp_server.log` for detailed errors.

---

## 📊 Expected Results

### ✅ Success Indicators

1. **Status Bar**: Shows "konaai-ssms" as connected (green indicator)
2. **Tools Available**: Shows "11 tools" when you hover over or click the server
3. **Resources Available**: Shows tables from both databases
4. **Queries Work**: Can execute SQL queries through Cursor chat
5. **Schema Access**: Can view table schemas and metadata

### ❌ Failure Indicators

1. **"No tools, prompts, or resources"** - Server not connecting
2. **Red indicator** on server status - Server crashed or failed to start
3. **"Connection timeout"** - Server taking too long to respond
4. **No server in status bar** - Configuration not loaded

---

## 🎉 What You Can Do Once Connected

### Database Queries
- **Natural Language**: "Show me all clients"
- **SQL Direct**: "Execute: SELECT * FROM App.Client WHERE IsActive = 1"
- **Cross-Database**: "Compare tables in Master and Data Management databases"

### Schema Exploration
- **Table Discovery**: "What tables are in the Master database?"
- **Column Details**: "Show me all columns in App.Client"
- **Relationships**: "What are the foreign keys in Client.ClientProject?"

### Data Operations
- **Insert**: "Insert a new client with name 'Test Client'"
- **Update**: "Update the client with ID 123 to set IsActive = 0"
- **Delete**: "Delete the client with ID 456"

### Stored Procedures
- **List**: "What stored procedures are available?"
- **Execute**: "Execute sp_GetClientInfo with parameter ClientId = 1"
- **Info**: "Show me the parameters for sp_GetClientInfo"

### Advanced
- **Performance**: "Show me the largest tables in Data Management database"
- **Analysis**: "Analyze the Client.ClientProject table structure"
- **Metadata**: "Get all triggers on App.User table"

---

## 📞 Need Help?

If you're still having issues:

1. **Verify database connections work:**
   ```powershell
   cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
   python tests/test_connection.py
   ```
   Should show: 29 + 367 tables ✅

2. **Verify MCP server works:**
   ```powershell
   python tests/mcp/verify_mcp_server.py
   ```
   Should show: All components OK ✅

3. **Check Cursor logs** in Developer Console

4. **Review** `CURSOR_INTEGRATION_FIX.md` for detailed troubleshooting

---

## 🔑 Key Files Reference

- **Configuration**: `cursor_mcp_config.json` - Use this for Cursor settings
- **Launcher**: `start_mcp.bat` - Alternative server starter
- **Detailed Guide**: `CURSOR_INTEGRATION_FIX.md` - Comprehensive troubleshooting
- **Tests**: `tests/test_connection.py` - Verify database connections
- **Verification**: `tests/mcp/verify_mcp_server.py` - Verify MCP server

---

**Your SSMS-MCP server is fully functional and ready to use! Just follow the 3 steps above to connect it to Cursor. 🚀**

**Once connected, you'll have powerful SQL Server management capabilities directly in Cursor!**





