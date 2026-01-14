# Changelog

## [1.1.0] - 2025-01-14

### Added
- **Advanced Setup Script** (`setup_mcp.py`): Automated setup with Python detection, dependency checking, and configuration generation
- **Quick Config Generator** (`generate_cursor_config.py`): Fast configuration file generation
- **Setup Validator** (`validate_setup.py`): Validates environment before running
- **Enhanced Launcher** (`launch_mcp.bat`): Improved Windows launcher with Python detection
- **Comprehensive Documentation**: README.md and QUICK_START.md with detailed instructions
- **Better Error Handling**: Improved error messages and logging in main.py

### Improved
- **Python Detection**: Automatic detection of Python executable across different environments
- **Path Handling**: Better path normalization for Windows/Linux/Mac compatibility
- **Error Messages**: More descriptive error messages with troubleshooting hints
- **Configuration**: More flexible configuration with environment variable support

### Fixed
- **Hardcoded Paths**: Removed hardcoded Python paths that caused "path not found" errors
- **MCP Protocol**: Improved stdio communication with proper logging to stderr
- **Dependency Checking**: Better validation of required packages

### Changed
- **Config Generation**: `cursor_mcp_config.json` is now auto-generated with correct paths
- **Setup Process**: Simplified setup with automated scripts

## [1.0.0] - Initial Release

### Features
- SQL Server database access via MCP protocol
- Query execution tools
- CRUD operations
- Schema discovery
- Stored procedure execution
- Resource access for tables, views, procedures, and triggers
