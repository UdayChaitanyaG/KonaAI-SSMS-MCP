#!/usr/bin/env python3
"""
KonaAI SSMS MCP Server - Main Entry Point

This is the main entry point for the KonaAI SQL Server Management Studio
Model Context Protocol (MCP) server. It provides enhanced database access
capabilities through the MCP protocol.

Usage:
    python main.py

Environment Variables:
    See config/env.example for required environment variables.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

# Import centralized configuration
from config.app_config import setup_environment

# Set up environment variables
setup_environment()

# Import and run the MCP server
from server.ssms_mcp_server import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
