@echo off
REM KonaAI SSMS MCP Server Launcher
REM This batch file starts the MCP server with proper environment settings

cd /d "%~dp0"

echo Starting KonaAI SSMS MCP Server...
echo ====================================
echo Working Directory: %CD%
echo Python Version:
python --version
echo.

REM Set environment variables for unbuffered output
set PYTHONUNBUFFERED=1
set PYTHONPATH=.

REM Start the MCP server
python -u main.py

REM If server exits with error, keep window open
if errorlevel 1 (
    echo.
    echo Server exited with error!
    echo Press any key to close...
    pause > nul
)





