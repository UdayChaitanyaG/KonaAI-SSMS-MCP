# Cursor MCP Integration Fix Guide

## Issue
Cursor shows "konaai-ssms" with "No tools, prompts, or resources"

## Root Cause
The MCP server is working correctly (verified), but Cursor needs proper configuration to connect to it.

## Verification Status
✅ Database connections working (29 + 367 tables)
✅ MCP server initialized successfully
✅ All tools and resources registered
❌ Cursor not showing tools/resources

## Solution Steps

### Step 1: Locate Cursor MCP Settings

1. **Option A: Via Cursor UI**
   - Open Cursor
   - Press `Ctrl + Shift + P` (Command Palette)
   - Type "Preferences: Open Settings (JSON)"
   - Look for MCP configuration section

2. **Option B: Direct File Edit**
   - Navigate to: `%APPDATA%\Cursor\User\`
   - Look for `settings.json` or `mcp_servers.json`
   - Or check: `%APPDATA%\Cursor\User\globalStorage\`

### Step 2: Add/Update MCP Server Configuration

Add this configuration to your Cursor settings:

```json
{
  "mcpServers": {
    "konaai-ssms": {
      "command": "python",
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

**Key Changes:**
- Added `-u` flag to Python for unbuffered output
- Added `PYTHONUNBUFFERED=1` environment variable
- This ensures Cursor can properly read MCP server output

### Step 3: Verify Python Path

Open PowerShell and verify:
```powershell
python --version
# Should show Python 3.10+

python -c "import mcp; print('MCP installed')"
# Should print "MCP installed"
```

If MCP is not installed:
```powershell
cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
pip install -r requirements.txt
```

### Step 4: Test Server Manually

Before restarting Cursor, test the server manually:
```powershell
cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
python main.py
```

**Expected Behavior:**
- Server should start
- Should show initialization messages
- Should NOT crash or show errors
- Press `Ctrl+C` to stop

### Step 5: Restart Cursor

1. **Completely close Cursor** (not just the window, but exit the application)
2. **Restart Cursor**
3. **Check MCP Server Status**:
   - Look at the bottom status bar
   - Should see "konaai-ssms" indicator
   - Click on it to see connection status

### Step 6: Enable MCP Server

1. In Cursor, look for the MCP server toggle switch (like in your screenshot)
2. **Toggle it ON** if it's OFF
3. Wait for Cursor to connect to the server

### Step 7: Verify Tools and Resources

Once connected, you should see:

**Tools (11 total):**
- execute_query
- insert_data
- update_data
- delete_data
- get_schema
- get_tables
- get_table_schema
- get_stored_procedures
- get_triggers
- get_views
- execute_procedure

**Resources:**
- Master Database tables (29 tables)
- Data Management Database tables (367 tables)
- Stored procedures
- Triggers
- Views

## Troubleshooting

### Issue: Server Not Starting

**Check 1: Python Environment**
```powershell
cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
python -c "import sys; print(sys.executable)"
```

**Check 2: Dependencies**
```powershell
pip list | Select-String mcp
pip list | Select-String pydantic
pip list | Select-String pyodbc
```

**Check 3: ODBC Driver**
Ensure "ODBC Driver 17 for SQL Server" is installed:
- Open: `Control Panel > Administrative Tools > ODBC Data Sources`
- Check for "ODBC Driver 17 for SQL Server"

### Issue: "No Module Named 'mcp'"

```powershell
cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
pip install mcp
# Or
pip install -r requirements.txt
```

### Issue: Cursor Can't Find Python

Update MCP configuration to use full Python path:
```json
{
  "mcpServers": {
    "konaai-ssms": {
      "command": "C:\\Users\\UdayChaitanyaGurvind\\AppData\\Local\\Programs\\Python\\Python312\\python.exe",
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

To find your Python path:
```powershell
(Get-Command python).Path
```

### Issue: Server Crashes Immediately

**Check logs:**
1. In Cursor, open Command Palette (`Ctrl+Shift+P`)
2. Type "Developer: Toggle Developer Tools"
3. Check Console tab for MCP-related errors

**Manual test:**
```powershell
cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
python main.py 2>&1 | Tee-Object -FilePath server.log
```
Check `server.log` for errors.

## Alternative: Use Absolute Python Path

If Cursor can't find Python, create a batch file launcher:

**File: `C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server\start_mcp.bat`**
```batch
@echo off
cd /d "%~dp0"
python -u main.py
```

Then update Cursor config:
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

## Quick Checklist

- [ ] Python 3.10+ installed and accessible
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] ODBC Driver 17 for SQL Server installed
- [ ] Database connections tested successfully
- [ ] MCP server configuration added to Cursor
- [ ] Cursor completely restarted
- [ ] MCP server toggle enabled in Cursor
- [ ] Tools and resources visible in Cursor

## Success Indicators

When everything is working:
1. ✅ Cursor status bar shows "konaai-ssms" as connected
2. ✅ MCP server shows 11 tools available
3. ✅ Resources show tables from both databases
4. ✅ You can execute queries through Cursor
5. ✅ Schema information is accessible

## Next Steps After Success

Once connected, try these commands in Cursor:

1. **List tables:**
   ```
   Show me all tables in the Master database
   ```

2. **Query data:**
   ```
   Execute: SELECT TOP 5 * FROM App.Client
   ```

3. **Get schema:**
   ```
   Show me the schema for App.Client table
   ```

4. **List procedures:**
   ```
   What stored procedures are available in the Master database?
   ```

## Support

If you still encounter issues after following all steps:
1. Check `tests/test_connection.py` output (should show 29 + 367 tables)
2. Check `tests/mcp/verify_mcp_server.py` output (should show all OK)
3. Provide Cursor's developer console logs
4. Check Windows Event Viewer for SQL Server connection issues

---

**Your MCP server is working correctly - we just need Cursor to connect to it properly! 🚀**





