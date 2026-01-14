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
import logging
from pathlib import Path

# Configure logging to stderr (for MCP stdio communication)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # Log to stderr to avoid interfering with MCP protocol
)

logger = logging.getLogger(__name__)

# Add the src directory to the Python path
src_dir = Path(__file__).parent / "src"
if src_dir.exists():
    sys.path.insert(0, str(src_dir))
else:
    logger.error(f"Source directory not found: {src_dir}")
    sys.exit(1)

try:
    # Import centralized configuration
    from config.app_config import setup_environment
    
    # Set up environment variables
    setup_environment()
    
    # Import and run the MCP server
    from server.ssms_mcp_server import main
    
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    logger.error("Please ensure all dependencies are installed:")
    logger.error("  pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    logger.error(f"Failed to initialize server: {e}")
    import traceback
    logger.error(traceback.format_exc())
    sys.exit(1)

if __name__ == "__main__":
    try:
        import asyncio
        logger.info("Starting KonaAI SSMS MCP Server...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)
