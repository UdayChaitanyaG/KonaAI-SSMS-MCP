#!/usr/bin/env python3
"""
Quick Cursor Config Generator
Generates cursor_mcp_config.json with auto-detected paths.
"""

import json
import sys
import os
from pathlib import Path


def get_project_path():
    """Get absolute path to mcp-server directory."""
    return Path(__file__).parent.absolute()


def find_python():
    """Find Python executable."""
    # Use current Python interpreter
    python_exe = sys.executable
    
    # On Windows, ensure we use the .exe
    if sys.platform == "win32" and not python_exe.endswith('.exe'):
        # Try to find the actual executable
        if os.path.exists(python_exe + '.exe'):
            python_exe = python_exe + '.exe'
    
    return python_exe


def generate_config():
    """Generate Cursor MCP configuration."""
    project_path = get_project_path()
    python_exe = find_python()
    main_py = project_path / "main.py"
    
    # Use absolute paths for reliability
    config = {
        "mcpServers": {
            "konaai-ssms": {
                "command": python_exe,
                "args": ["-u", str(main_py)],
                "cwd": str(project_path),
                "env": {
                    "PYTHONPATH": str(project_path),
                    "PYTHONUNBUFFERED": "1"
                }
            }
        }
    }
    
    return config


def main():
    """Generate and save configuration."""
    print("Generating Cursor MCP configuration...")
    
    config = generate_config()
    config_file = get_project_path() / "cursor_mcp_config.json"
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration saved to: {config_file}")
    print("\nConfiguration:")
    print(json.dumps(config, indent=2))
    
    print("\n📝 Next steps:")
    print("1. Copy the configuration above")
    print("2. Open Cursor IDE")
    print("3. Press Ctrl+Shift+P and type 'MCP: Add Server Configuration'")
    print("4. Paste the configuration")
    print("5. Restart Cursor")


if __name__ == "__main__":
    main()
