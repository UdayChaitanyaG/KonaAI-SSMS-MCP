# SSMS-MCP Cursor Setup Checklist

## ✅ Pre-Setup Verification (Already Completed)

- [x] Python 3.10.10 installed and accessible
- [x] MCP library (1.16.0) installed
- [x] Pydantic (2.12.3) installed
- [x] PyODBC (5.3.0) installed
- [x] ODBC Driver 17 for SQL Server available
- [x] Master Database connection working (29 tables)
- [x] Data Management Database connection working (367 tables)
- [x] MCP server initializes successfully
- [x] All 11 tools registered
- [x] All 4 resources registered
- [x] Configuration files created

**All pre-requisites complete! ✅**

---

## 🚀 Cursor Integration Setup (Your Action Required)

### Step 1: Prepare Configuration (2 minutes)

- [ ] **Open File Explorer**
- [ ] **Navigate to:** 
  ```
  C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server
  ```
- [ ] **Open:** `cursor_mcp_config.json`
- [ ] **Copy entire contents** (Ctrl+A, Ctrl+C)

**Configuration to Copy:**
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

---

### Step 2: Add to Cursor (3 minutes)

#### Option A: Via Settings UI (Recommended)

- [ ] **Open Cursor IDE**
- [ ] **Press:** `Ctrl + ,` (Settings)
- [ ] **Search for:** "MCP" in search bar
- [ ] **Look for:** "MCP Servers" or "Model Context Protocol" section
- [ ] **Click:** "Edit in settings.json" button
- [ ] **Paste configuration** from Step 1
- [ ] **Save file:** `Ctrl + S`

#### Option B: Via Command Palette

- [ ] **Open Cursor IDE**
- [ ] **Press:** `Ctrl + Shift + P` (Command Palette)
- [ ] **Type:** "Preferences: Open User Settings (JSON)"
- [ ] **Press:** Enter
- [ ] **Add the `mcpServers` section** (paste from Step 1)
- [ ] **Ensure JSON is valid** (no extra commas, brackets match)
- [ ] **Save file:** `Ctrl + S`

#### Option C: Direct File Edit

- [ ] **Close Cursor completely**
- [ ] **Open File Explorer**
- [ ] **Navigate to:** `%APPDATA%\Cursor\User\`
  ```
  C:\Users\UdayChaitanyaGurvind\AppData\Roaming\Cursor\User\
  ```
- [ ] **Open:** `settings.json` in Notepad++/VS Code
- [ ] **Add the `mcpServers` section** (paste from Step 1)
- [ ] **Save file**
- [ ] **Start Cursor**

---

### Step 3: Restart and Enable (2 minutes)

- [ ] **Close Cursor completely**
  - [ ] File → Exit (or Alt+F4)
  - [ ] Ensure Cursor process is not running in Task Manager
- [ ] **Wait 5 seconds**
- [ ] **Start Cursor again**
- [ ] **Wait for Cursor to fully load** (10-15 seconds)
- [ ] **Check bottom status bar** for "konaai-ssms"
- [ ] **Click the toggle switch** to turn ON (if it's OFF)
- [ ] **Wait for connection** (5-10 seconds)
- [ ] **Check for "11 tools available"** when hovering

---

### Step 4: Verify Connection (2 minutes)

#### Visual Checks

- [ ] **Status bar shows:** "konaai-ssms" with green indicator
- [ ] **Hover over server:** Shows "11 tools, X resources"
- [ ] **No red indicators or error messages**
- [ ] **No "No tools, prompts, or resources" message**

#### Functional Tests

- [ ] **Open Cursor Chat**
- [ ] **Type:** "Show me all tables in the Master database"
- [ ] **Expected:** List of 29 tables appears
- [ ] **Type:** "Execute: SELECT TOP 5 * FROM App.Client"
- [ ] **Expected:** Query results appear
- [ ] **Type:** "What columns are in App.Client table?"
- [ ] **Expected:** Table schema displayed

---

## 🔍 Troubleshooting Checklist

### If "No tools, prompts, or resources" Still Shows

- [ ] **Check 1: Configuration Location**
  - [ ] Open Cursor settings
  - [ ] Verify `mcpServers` section exists
  - [ ] Verify JSON syntax is correct (no red underlines)
  
- [ ] **Check 2: Python Path**
  - [ ] Open PowerShell
  - [ ] Run: `(Get-Command python).Path`
  - [ ] Verify path matches config: 
    ```
    C:\Program Files\KonaAI_ML\.pyenv\pyenv-win\shims\python.bat
    ```
  
- [ ] **Check 3: Server Can Start**
  - [ ] Open PowerShell
  - [ ] Run:
    ```powershell
    cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
    python test_mcp_startup.py
    ```
  - [ ] Verify: All checks pass ✅
  
- [ ] **Check 4: Cursor Logs**
  - [ ] In Cursor: `Ctrl + Shift + P`
  - [ ] Type: "Developer: Toggle Developer Tools"
  - [ ] Go to Console tab
  - [ ] Look for MCP-related errors
  - [ ] Screenshot any errors

### If Server Won't Start

- [ ] **Try Batch File Launcher**
  - [ ] Update config to use `start_mcp.bat`
  - [ ] Configuration:
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

### If Database Errors Occur

- [ ] **Test database connection:**
  ```powershell
  cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
  python tests/test_connection.py
  ```
- [ ] **Expected:** 29 + 367 tables found
- [ ] **If failed:** Check SQL Server is running

---

## 📋 Quick Reference

### Files Created for You

| File | Purpose |
|------|---------|
| `cursor_mcp_config.json` | Configuration to copy into Cursor |
| `start_mcp.bat` | Alternative server launcher |
| `QUICK_START_CURSOR.md` | Detailed setup instructions |
| `CURSOR_INTEGRATION_FIX.md` | Comprehensive troubleshooting |
| `CONNECTION_STATUS_SUMMARY.md` | Current status overview |
| `test_mcp_startup.py` | Verify server works |

### Test Commands

```powershell
# Navigate to MCP server directory
cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"

# Test database connections
python tests/test_connection.py

# Test MCP server initialization  
python test_mcp_startup.py

# Verify all components
python tests/mcp/verify_mcp_server.py

# Start server manually (for debugging)
python main.py
```

---

## 🎯 Expected Final State

### Status Bar
```
[●] konaai-ssms (11 tools, 396 resources)
```

### Hover Tooltip
```
konaai-ssms
Connected
11 tools available:
  • execute_query
  • insert_data
  • update_data
  • delete_data
  • get_schema
  • get_tables
  • get_table_schema
  • get_stored_procedures
  • get_triggers
  • get_views
  • execute_procedure
```

### Functional
- ✅ Can list tables in both databases
- ✅ Can execute SQL queries
- ✅ Can view table schemas
- ✅ Can access stored procedures
- ✅ Can insert/update/delete data

---

## 🎉 Success Criteria

You'll know it's working when:

1. ✅ **Status bar shows:** Green indicator for "konaai-ssms"
2. ✅ **Hover shows:** "11 tools available"
3. ✅ **Can query:** Tables from both databases
4. ✅ **Can view:** Schema information
5. ✅ **No errors:** In Cursor console

---

## ⏱️ Estimated Time

- **Total Time:** 7-10 minutes
- **Step 1:** 2 minutes (Copy configuration)
- **Step 2:** 3 minutes (Add to Cursor)
- **Step 3:** 2 minutes (Restart and enable)
- **Step 4:** 2 minutes (Verify)
- **Troubleshooting:** 0-10 minutes (if needed)

---

## 📞 Need Help?

If you complete all steps and still have issues:

1. **Run all test commands** above
2. **Check Cursor Developer Console** for errors
3. **Review** `CURSOR_INTEGRATION_FIX.md`
4. **Take screenshots** of any error messages
5. **Check** that SQL Server is running and accessible

---

**Everything is ready! Just follow Steps 1-4 above to complete the setup. 🚀**

**Your SSMS-MCP server will be fully integrated with Cursor in less than 10 minutes!**





