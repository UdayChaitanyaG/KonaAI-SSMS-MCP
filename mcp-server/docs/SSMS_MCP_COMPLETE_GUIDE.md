## SSMS MCP Complete Guide

### 1) Overview
The KonaAI SSMS MCP (Model Context Protocol) server exposes SQL Server metadata and execution capabilities to IDE agents (e.g., Cursor) via a local stdio server. It provides:
- Tools (execute queries, CRUD, schema inspection, stored procedures)
- Read-only Resources (tables, views, procedures, triggers) discoverable by the client

Repo location: `KonaAI-SSMS-MCP/mcp-server`
Entry point: `mcp-server/main.py`
Server name/id: `konaai-ssms`

### 2) Architecture
- Transport: MCP stdio (`mcp.server.stdio.stdio_server`)
- Core: `src/server/ssms_mcp_server.py` registers handlers:
  - list_tools, call_tool, list_resources, read_resource
- Databases: two connections via pooling layer
  - `MasterDatabase` → KonaAI Master DB
  - `DataManagementDatabase` → DIT_GDB Data Management DB
- Tools (in `src/server/tools`):
  - QueryTool: `execute_query`
  - CrudTool: `insert_data`, `update_data`, `delete_data`
  - SchemaTool: `get_schema`, `get_tables`, `get_table_schema`, `get_stored_procedures`, `get_triggers`, `get_views`
  - StoredProcedureTool: `execute_procedure`, `get_procedure_info`
- Resources (in `src/server/resources`): `tables`, `views`, `procedures`, `triggers`

### 3) Configuration
File: `src/config/database_config.py`
- AppConfig (env-backed via `.env`):
  - Master: `master_db_server`, `master_db_name`, `master_db_user`, `master_db_password`
  - DataMgmt: `data_mgmt_db_server`, `data_mgmt_db_name`, `data_mgmt_db_user`, `data_mgmt_db_password`
  - Timeouts, pool sizes, logging
- Connection strings built with Windows Auth if user/pass empty, else SQL Auth. Driver: ODBC Driver 17 for SQL Server.

Example `.env`:
```
master_db_server=DC-L-
master_db_name=KonaAI
data_mgmt_db_server=DC-L-
data_mgmt_db_name=DIT_GDB
# Optional SQL auth
# master_db_user=sa
# master_db_password=***
```

### 4) Installation & Requirements
- Python (as provided by KonaAI_ML pyenv shim)
- ODBC Driver 17 for SQL Server
- Network access to SQL Server instance(s)

### 5) Starting the Server
Manual (for debugging):
```powershell
cd "KonaAI-SSMS-MCP/mcp-server"
"C:\Program Files\KonaAI_ML\.pyenv\pyenv-win\shims\python.bat" -u .\main.py
```

Via Cursor (recommended): Settings → MCP Servers → enable `user-konaai-ssms`.

Restart: toggle server off/on in Cursor, or restart Cursor window.

### 6) Tools Reference
- execute_query
  - Input: `{ database: "master"|"datamgmt", query: string, max_rows?: number }`
  - Output: `{ data: object[], row_count: number, execution_time: number }`
- insert_data / update_data / delete_data
  - Input: `{ database, table_name, schema?, values?/set?/where }`
  - Output: rows affected
- get_schema
  - Input: `{ database }`
  - Output: high-level schema summary
- get_tables
  - Input: `{ database }`
  - Output: tables list with schema
- get_table_schema
  - Input: `{ database, table_name, schema? }`
  - Output: columns (type, nullability, defaults), indexes, fks (if enabled)
- get_stored_procedures
  - Input: `{ database }`
  - Output: procedures list
- get_triggers
  - Input: `{ database }`
  - Output: triggers list (name, table, schema, flags)
- get_views
  - Input: `{ database }`
  - Output: views list and definitions (where applicable)
- execute_procedure
  - Input: `{ database, name, schema?, params: object }`
  - Output: result sets and return status
- get_procedure_info
  - Input: `{ database, name, schema? }`
  - Output: parameters metadata, definition when available

### 7) Resources Reference
Resource URIs (read-only):
- `ssms://master/tables/<schema>.<table>`
- `ssms://datamgmt/tables/<schema>.<table>`
- `ssms://master/views/<schema>.<view>`
- `ssms://datamgmt/views/<schema>.<view>`
- `ssms://master/procedures/<schema>.<proc>`
- `ssms://datamgmt/procedures/<schema>.<proc>`
- `ssms://master/triggers/<trigger>`
- `ssms://datamgmt/triggers/<trigger>`

### 8) Known Behaviors & Fixes
- MCP list handlers must be async. Implemented in `ssms_mcp_server.py`.
- Trigger schema: use `OBJECT_SCHEMA_NAME(t.object_id)` (not `t.schema_id`). Fixed in `master_db.py` and `datamgmt_db.py`.
- Datetime serialization: prefer returning simple types in tool outputs; where needed, format datetimes to ISO8601.

### 9) Logging
- Standard Python logging; level controlled by `AppConfig.log_level`.
- On shutdown, the server closes DB pools and logs “Database connections closed”.

### 10) Security
- Windows Auth by default (Trusted_Connection=yes). For SQL Auth, set user/password in `.env`.
- No secrets committed; use `.env`.
- Read operations default to `AsNoTracking` style queries at the DB layer; writes via CRUD tools should be guarded.

### 11) Troubleshooting
- Server connects but shows no tools/resources: ensure list handlers are async and then restart the server.
- SQL errors on triggers: verify `OBJECT_SCHEMA_NAME` fix deployed.
- Cursor cannot start server: use `start_mcp.bat` or run `main.py` directly and inspect console output.
- Datetime not JSON serializable: cast to string/ISO in tool outputs.

### 12) Examples
- List App tables in DataManagement:
```sql
SELECT TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'App'
ORDER BY TABLE_NAME;
```
- Get schema for `App.Questionnaire`:
```sql
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'App' AND TABLE_NAME = 'Questionnaire'
ORDER BY ORDINAL_POSITION;
```
- Procedure definition:
```sql
SELECT OBJECT_DEFINITION(OBJECT_ID('App.GetQuestionnaire'));
```

### 13) Maintenance
- Add new tools/resources under `src/server/tools` and `src/server/resources` and register in `ssms_mcp_server.py`.
- Keep SQL compatible with SQL Server and ODBC Driver 17.
- Update docs and README links when adding capabilities.

### 14) Change Log (Recent)
- Async MCP list handlers to fix await-on-list error
- Correct trigger schema using `OBJECT_SCHEMA_NAME(t.object_id)`

### 15) Contacts
- Owner: KonaAI Data Platform Team


