#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced MCP Server Setup Script
Automatically detects Python, validates environment, and generates Cursor configuration.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Tuple

# Fix Windows console encoding for emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def find_python_executable() -> Optional[str]:
    """Find the best Python executable to use."""
    # Try multiple methods to find Python
    candidates = [
        sys.executable,  # Current Python interpreter
        shutil.which("python3"),
        shutil.which("python"),
        shutil.which("py"),
    ]
    
    # On Windows, also check common locations
    if sys.platform == "win32":
        windows_paths = [
            r"C:\Python3*\python.exe",
            r"C:\Program Files\Python3*\python.exe",
            r"C:\Users\{}\AppData\Local\Programs\Python\Python3*\python.exe".format(os.getenv("USERNAME", "")),
        ]
        # Try to find Python in Windows paths
        import glob
        for pattern in windows_paths:
            matches = glob.glob(pattern)
            if matches:
                # Get the latest version
                candidates.extend(sorted(matches, reverse=True))
    
    # Test each candidate
    for python_path in candidates:
        if python_path and os.path.exists(python_path):
            try:
                result = subprocess.run(
                    [python_path, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    version = result.stdout.strip()
                    print(f"[OK] Found Python: {python_path} ({version})")
                    return python_path
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                continue
    
    return None


def validate_dependencies(python_path: str) -> Tuple[bool, list]:
    """Validate that all required dependencies are installed."""
    required_packages = [
        "mcp",
        "pyodbc",
        "python-dotenv",
        "pydantic",
        "pydantic-settings"
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            result = subprocess.run(
                [python_path, "-m", "pip", "show", package],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                missing.append(package)
        except Exception:
            missing.append(package)
    
    return len(missing) == 0, missing


def safe_print(text: str):
    """Print text safely, handling encoding issues."""
    try:
        print(text)
    except UnicodeEncodeError:
        # Fallback: remove emojis and special characters
        import re
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        print(text)


def install_dependencies(python_path: str) -> bool:
    """Install required dependencies."""
    print("\n[INFO] Installing dependencies...")
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"❌ Requirements file not found: {requirements_file}")
        return False
    
    try:
        result = subprocess.run(
            [python_path, "-m", "pip", "install", "-r", str(requirements_file)],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print("[OK] Dependencies installed successfully")
            return True
        else:
            print(f"[ERROR] Failed to install dependencies:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"[ERROR] Error installing dependencies: {e}")
        return False


def get_project_path() -> Path:
    """Get the absolute path to the mcp-server directory."""
    return Path(__file__).parent.absolute()


def create_cursor_config(python_path: str, use_relative_paths: bool = True) -> dict:
    """Create Cursor MCP configuration."""
    project_path = get_project_path()
    main_py = project_path / "main.py"
    
    # Always use absolute paths for reliability
    # Cursor needs absolute paths to work correctly
    main_py_arg = str(main_py)
    
    # Normalize path separators for Windows
    if sys.platform == "win32":
        main_py_arg = main_py_arg.replace("\\", "/")
        project_path_str = str(project_path).replace("\\", "/")
    else:
        project_path_str = str(project_path)
    
    config = {
        "mcpServers": {
            "konaai-ssms": {
                "command": python_path,
                "args": ["-u", main_py_arg],
                "cwd": project_path_str,
                "env": {
                    "PYTHONPATH": project_path_str,
                    "PYTHONUNBUFFERED": "1"
                }
            }
        }
    }
    
    return config


def save_cursor_config(python_path: str) -> Path:
    """Save Cursor MCP configuration to file."""
    config = create_cursor_config(python_path, use_relative_paths=True)
    config_file = get_project_path() / "cursor_mcp_config.json"
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    return config_file


def test_server_startup(python_path: str) -> bool:
    """Test if the MCP server can start."""
    print("\n[TEST] Testing MCP server startup...")
    project_path = get_project_path()
    test_script = project_path / "test_mcp_startup.py"
    
    if not test_script.exists():
        print("⚠️  Test script not found, skipping startup test")
        return True
    
    try:
        result = subprocess.run(
            [python_path, str(test_script)],
            cwd=str(project_path),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("[OK] Server startup test passed")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("[WARN] Server startup test failed")
            if result.stderr:
                print(result.stderr)
            if result.stdout:
                print(result.stdout)
            return False
    except subprocess.TimeoutExpired:
        print("[WARN] Test timed out (this may be normal if waiting for input)")
        return True
    except Exception as e:
        print(f"[WARN] Error running test: {e}")
        return True  # Don't fail setup if test fails


def print_setup_instructions(config_file: Path, python_path: str):
    """Print setup instructions for the user."""
    print("\n" + "=" * 70)
    print("SETUP INSTRUCTIONS")
    print("=" * 70)
    print(f"\n[OK] Configuration saved to: {config_file}")
    print(f"[OK] Python executable: {python_path}")
    
    print("\nNext Steps:")
    print("1. Open Cursor IDE")
    print("2. Press Ctrl+Shift+P (or Cmd+Shift+P on Mac)")
    print("3. Type 'MCP' and select 'MCP: Add Server Configuration'")
    print("4. Copy the configuration from cursor_mcp_config.json:")
    print()
    
    config = create_cursor_config(python_path)
    print(json.dumps(config, indent=2))
    
    print("\n5. Paste the configuration into Cursor's MCP settings")
    print("6. Restart Cursor IDE")
    print("7. The 'konaai-ssms' server should appear in Cursor's MCP list")
    
    print("\nAlternative: Manual Configuration")
    print("   You can also manually edit Cursor's MCP settings file:")
    if sys.platform == "win32":
        print("   %APPDATA%\\Cursor\\User\\globalStorage\\mcp.json")
    elif sys.platform == "darwin":
        print("   ~/Library/Application Support/Cursor/User/globalStorage/mcp.json")
    else:
        print("   ~/.config/Cursor/User/globalStorage/mcp.json")
    
    print("\n" + "=" * 70)


def main():
    """Main setup function."""
    print("=" * 70)
    print("KonaAI SSMS MCP Server - Advanced Setup")
    print("=" * 70)
    
    # Get project path
    project_path = get_project_path()
    print(f"\n[INFO] Project path: {project_path}")
    
    # Find Python
    print("\n[INFO] Detecting Python executable...")
    python_path = find_python_executable()
    
    if not python_path:
        print("[ERROR] Python not found!")
        print("\nPlease install Python 3.8+ and try again.")
        print("Or set PYTHON environment variable to your Python executable.")
        return False
    
    # Validate dependencies
    print("\n[INFO] Checking dependencies...")
    deps_ok, missing = validate_dependencies(python_path)
    
    if not deps_ok:
        print(f"[WARN] Missing dependencies: {', '.join(missing)}")
        response = input("\nInstall missing dependencies? (y/n): ").strip().lower()
        if response == 'y':
            if not install_dependencies(python_path):
                return False
            # Re-validate
            deps_ok, missing = validate_dependencies(python_path)
            if not deps_ok:
                print(f"[ERROR] Still missing: {', '.join(missing)}")
                return False
        else:
            print("Please install dependencies manually:")
            print(f"  {python_path} -m pip install -r requirements.txt")
            return False
    else:
        print("[OK] All dependencies installed")
    
    # Test server startup
    if not test_server_startup(python_path):
        print("\n[WARN] Server startup test failed, but continuing with setup...")
        print("   You may need to check your database configuration.")
    
    # Create Cursor configuration
    print("\n[INFO] Creating Cursor MCP configuration...")
    config_file = save_cursor_config(python_path)
    print(f"[OK] Configuration saved")
    
    # Print instructions
    print_setup_instructions(config_file, python_path)
    
    print("\n[OK] Setup completed successfully!")
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[WARN] Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
