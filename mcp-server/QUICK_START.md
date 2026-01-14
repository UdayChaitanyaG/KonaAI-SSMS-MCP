# Quick Start Guide

Get the KonaAI SSMS MCP Server running in Cursor IDE in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Configure Database (Optional)

If you need to change database settings, edit `src/config/app_config.py`:

```python
DATABASE_SERVERS = {
    'master': {
        'server': 'YOUR_SERVER',  # Change this
        'database': 'KonaAI',
    },
    'datamgmt': {
        'server': 'YOUR_SERVER',  # Change this
        'database': 'DIT_GDB',
    }
}
```

**Note**: Windows Authentication is used by default (no username/password needed).

## Step 3: Test the Server

```bash
python test_mcp_startup.py
```

If this works, you're ready for Cursor!

## Step 4: Generate Cursor Configuration

### Option A: Automated Setup (Recommended)

```bash
python setup_mcp.py
```

This will:
- ✅ Auto-detect Python
- ✅ Check dependencies
- ✅ Test the server
- ✅ Generate configuration
- ✅ Show you exactly what to do next

### Option B: Quick Config Generation

```bash
python generate_cursor_config.py
```

This generates `cursor_mcp_config.json` with auto-detected paths.

## Step 5: Add to Cursor

1. **Open Cursor IDE**
2. **Press `Ctrl+Shift+P`** (or `Cmd+Shift+P` on Mac)
3. **Type "MCP"** and select **"MCP: Add Server Configuration"**
4. **Copy the entire JSON** from `cursor_mcp_config.json`:

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

5. **Paste into Cursor's MCP settings**
6. **Restart Cursor IDE**
7. **Done!** The server should appear in Cursor's MCP list

## Troubleshooting

### "The system cannot find the path specified"

**Fix**: Run `python setup_mcp.py` to auto-detect Python, or manually edit `cursor_mcp_config.json` with the correct Python path.

### "Client error for command spawn"

**Fix**: 
- Verify Python: `python --version`
- Check Python path in config is correct
- Try using `py` on Windows instead of `python`

### "No server info found"

**Fix**:
- Test server: `python test_mcp_startup.py`
- Check database settings
- Verify dependencies: `pip list | grep mcp`

### Server won't start

**Fix**:
1. Check database connection: Edit `src/config/app_config.py`
2. Ensure SQL Server is running
3. Verify Windows Authentication is enabled
4. Check server name is correct

## Need Help?

1. Run `python setup_mcp.py` for automated diagnostics
2. Check `README.md` for detailed documentation
3. Review error messages in Cursor's MCP logs

## What's Next?

Once connected, you can:
- Execute SQL queries
- Browse database schema
- Run stored procedures
- Access tables, views, and triggers as resources

Try asking Cursor: "Show me all tables in the Master database"
