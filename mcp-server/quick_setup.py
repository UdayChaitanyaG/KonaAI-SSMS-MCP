#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Setup Script - Non-interactive version
Automatically installs dependencies and generates Cursor configuration.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def get_project_path():
    """Get absolute path to mcp-server directory."""
    return Path(__file__).parent.absolute()


def find_python():
    """Find Python executable."""
    return sys.executable


def install_dependencies(python_path: str) -> bool:
    """Install required dependencies."""
    print("[INFO] Installing dependencies...")
    requirements_file = get_project_path() / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"[ERROR] Requirements file not found: {requirements_file}")
        return False
    
    try:
        result = subprocess.run(
            [python_path, "-m", "pip", "install", "-r", str(requirements_file), "--quiet"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print("[OK] Dependencies installed successfully")
            return True
        else:
            print(f"[ERROR] Failed to install dependencies")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"[ERROR] Error installing dependencies: {e}")
        return False


def generate_config():
    """Generate Cursor MCP configuration."""
    project_path = get_project_path()
    python_exe = find_python()
    main_py = project_path / "main.py"
    
    # Normalize paths for Windows
    if sys.platform == "win32":
        main_py_str = str(main_py).replace("\\", "/")
        project_path_str = str(project_path).replace("\\", "/")
    else:
        main_py_str = str(main_py)
        project_path_str = str(project_path)
    
    config = {
        "mcpServers": {
            "konaai-ssms": {
                "command": python_exe,
                "args": ["-u", main_py_str],
                "cwd": project_path_str,
                "env": {
                    "PYTHONPATH": project_path_str,
                    "PYTHONUNBUFFERED": "1"
                }
            }
        }
    }
    
    return config


def main():
    """Main setup function."""
    print("=" * 70)
    print("KonaAI SSMS MCP Server - Quick Setup")
    print("=" * 70)
    
    project_path = get_project_path()
    python_path = find_python()
    
    print(f"\n[INFO] Project path: {project_path}")
    print(f"[INFO] Python: {python_path}")
    
    # Install dependencies
    print("\n[INFO] Installing dependencies...")
    if not install_dependencies(python_path):
        print("[WARN] Some dependencies may not be installed. Continuing...")
    
    # Generate configuration
    print("\n[INFO] Generating Cursor MCP configuration...")
    config = generate_config()
    config_file = project_path / "cursor_mcp_config.json"
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    print(f"[OK] Configuration saved to: {config_file}")
    
    # Print configuration
    print("\n" + "=" * 70)
    print("CURSOR MCP CONFIGURATION")
    print("=" * 70)
    print(json.dumps(config, indent=2))
    
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("1. Open Cursor IDE")
    print("2. Press Ctrl+Shift+P (or Cmd+Shift+P on Mac)")
    print("3. Type 'MCP' and select 'MCP: Add Server Configuration'")
    print("4. Copy the configuration above and paste it into Cursor")
    print("5. Restart Cursor IDE")
    print("6. The 'konaai-ssms' server should appear in Cursor's MCP list")
    print("\n[OK] Setup completed!")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
