#!/usr/bin/env python3
"""
Setup Validation Script
Validates that the MCP server is properly configured and ready to run.
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if required packages are installed."""
    required = [
        "mcp",
        "pyodbc",
        "python-dotenv",
        "pydantic",
        "pydantic-settings"
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing.append(package)
    
    return len(missing) == 0, missing


def check_files():
    """Check if required files exist."""
    project_path = Path(__file__).parent
    required_files = [
        "main.py",
        "requirements.txt",
        "src/server/ssms_mcp_server.py",
        "src/config/app_config.py",
        "src/config/database_config.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = project_path / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (missing)")
            all_exist = False
    
    return all_exist


def check_config():
    """Check if configuration files exist."""
    project_path = Path(__file__).parent
    config_file = project_path / "src" / "config" / "app_config.py"
    
    if not config_file.exists():
        print("❌ Configuration file not found")
        return False
    
    # Try to import and validate config
    try:
        sys.path.insert(0, str(project_path / "src"))
        from config.app_config import DATABASE_SERVERS
        
        print("✅ Configuration file found")
        
        # Check if server names are configured
        master_server = DATABASE_SERVERS.get('master', {}).get('server', '')
        datamgmt_server = DATABASE_SERVERS.get('datamgmt', {}).get('server', '')
        
        if not master_server or master_server == 'DC-L-':
            print("⚠️  Master database server not configured (using default)")
        else:
            print(f"✅ Master DB server: {master_server}")
        
        if not datamgmt_server or datamgmt_server == 'DC-L-':
            print("⚠️  Data Management database server not configured (using default)")
        else:
            print(f"✅ Data Management DB server: {datamgmt_server}")
        
        return True
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return False


def main():
    """Run all validation checks."""
    print("=" * 60)
    print("KonaAI SSMS MCP Server - Setup Validation")
    print("=" * 60)
    print()
    
    checks = []
    
    print("1. Python Version:")
    checks.append(check_python_version())
    print()
    
    print("2. Required Files:")
    checks.append(check_files())
    print()
    
    print("3. Dependencies:")
    deps_ok, missing = check_dependencies()
    checks.append(deps_ok)
    if missing:
        print(f"\n   Install missing packages:")
        print(f"   pip install {' '.join(missing)}")
    print()
    
    print("4. Configuration:")
    checks.append(check_config())
    print()
    
    print("=" * 60)
    if all(checks):
        print("✅ All checks passed! Server is ready to run.")
        print("\nNext steps:")
        print("1. Run: python setup_mcp.py")
        print("2. Follow the instructions to add to Cursor")
        return True
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
