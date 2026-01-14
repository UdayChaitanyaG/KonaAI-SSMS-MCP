@echo off
REM KonaAI SSMS MCP Server Launcher
REM Advanced launcher with Python detection and error handling

setlocal enabledelayedexpansion

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo ========================================
echo KonaAI SSMS MCP Server Launcher
echo ========================================
echo.

REM Try to find Python
set "PYTHON_EXE="

REM Check if Python is in PATH
python --version >nul 2>&1
if %errorlevel% == 0 (
    set "PYTHON_EXE=python"
    goto :found_python
)

REM Check for python3
python3 --version >nul 2>&1
if %errorlevel% == 0 (
    set "PYTHON_EXE=python3"
    goto :found_python
)

REM Check for py launcher
py --version >nul 2>&1
if %errorlevel% == 0 (
    set "PYTHON_EXE=py"
    goto :found_python
)

REM Check common Python installation paths
if exist "C:\Python3*\python.exe" (
    for /f "delims=" %%i in ('dir /b /ad "C:\Python3*" 2^>nul') do (
        if exist "C:\%%i\python.exe" (
            set "PYTHON_EXE=C:\%%i\python.exe"
            goto :found_python
        )
    )
)

REM Check Program Files
if exist "C:\Program Files\Python3*\python.exe" (
    for /f "delims=" %%i in ('dir /b /ad "C:\Program Files\Python3*" 2^>nul') do (
        if exist "C:\Program Files\%%i\python.exe" (
            set "PYTHON_EXE=C:\Program Files\%%i\python.exe"
            goto :found_python
        )
    )
)

REM Check user AppData
if exist "%LOCALAPPDATA%\Programs\Python\Python3*\python.exe" (
    for /f "delims=" %%i in ('dir /b /ad "%LOCALAPPDATA%\Programs\Python\Python3*" 2^>nul') do (
        if exist "%LOCALAPPDATA%\Programs\Python\%%i\python.exe" (
            set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\%%i\python.exe"
            goto :found_python
        )
    )
)

REM Python not found
echo ERROR: Python not found!
echo.
echo Please install Python 3.8+ or set PYTHON environment variable.
echo.
echo You can also run the setup script to auto-configure:
echo   python setup_mcp.py
echo.
pause
exit /b 1

:found_python
echo Found Python: %PYTHON_EXE%
%PYTHON_EXE% --version
echo.
echo Working Directory: %CD%
echo.

REM Set environment variables
set "PYTHONUNBUFFERED=1"
set "PYTHONPATH=%CD%"

REM Check if dependencies are installed
echo Checking dependencies...
%PYTHON_EXE% -c "import mcp" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo WARNING: MCP dependencies not found!
    echo Installing dependencies...
    %PYTHON_EXE% -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
)

echo.
echo Starting MCP Server...
echo ========================================
echo.

REM Start the MCP server
%PYTHON_EXE% -u main.py

REM Check exit code
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo Server exited with error code: %errorlevel%
    echo ========================================
    echo.
    echo Troubleshooting:
    echo 1. Check database connection settings in src/config/app_config.py
    echo 2. Ensure SQL Server is running
    echo 3. Verify Windows Authentication is enabled
    echo 4. Check that all dependencies are installed
    echo.
    pause
)

endlocal
