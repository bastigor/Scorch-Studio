@echo off
REM Scorch Windows Launcher - Portable AI Studio
REM Usage: windows.bat [--reset] [--backend cuda|rocm|vulkan|cpu]

setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Parse arguments
if "%~1"=="--reset" set RESET=1

REM Set backend type (default to cpu)
if "%~2"=="cuda" set BACKEND=cuda
if "%~2"=="rocm" set BACKEND=rocm
if "%~2"=="vulkan" set BACKEND=vulkan
if "%~2"=="cpu" set BACKEND=cpu
if not defined BACKEND set BACKEND=cpu

REM Download Python portable binary if needed
echo.
echo [1/5] Checking for portable Python...

set PYTHON_EXISTS=0
for /f "delims=" %%i in ('python --version 2^>nul') do (
    if not errorlevel 1 (
        set PYTHON_EXISTS=1
        echo Portable Python found: %%i
    )
)

if not defined PYTHON_EXISTS (
    echo Downloading portable Python binary...
    set DOWNLOAD_URL=https://github.com/João-Pedro/python-build-standalone/releases/download/v0.29.0/python-build-standalone-win-x86_64.zip
    echo Downloading: %DOWNLOAD_URL%
    
    curl -L -o "python-portable-win-x86_64.zip" "%DOWNLOAD_URL%"
    
    if errorlevel 1 (
        echo Failed to download portable Python. Please install Python manually and skip this step.
    ) else (
        echo Extracting...
        tar xf python-portable-win-x86_64.zip /python.exe
        
        REM Find Python executable path
        for %%a in ("python.exe") do (
            set PYTHON_PATH="%%~f"
        )
        
        if exist "%PYTHON_PATH%" (
            echo Portable Python installed at: %PYTHON_PATH%
            
            REM Create virtual environment in runtime/
            set VENV_DIR=runtimeenv
            
            if not exist "%VENV_DIR%" (
                echo Creating virtual environment...
                
                REM Try to use system Python for venv creation first
                python -m venv %VENV_DIR% 2>nul || (
                    echo System Python failed, trying with explicit path...
                    call "%PYTHON_PATH%" -m venv %VENV_DIR%
                )
                
                if errorlevel 1 (
                    echo Failed to create venv. Continuing without it...
                ) else (
                    echo Virtual environment created at: %VENV_DIR%
                )
            ) else (
                echo Venv already exists at: %VENV_DIR%
            )
        ) else (
            echo Python executable not found after extraction!
        )
        
        del python-portable-win-x86_64.zip 2>nul
    )
)

REM Install dependencies if venv doesn't exist or needs upgrade
if defined VENV_DIR (
    echo.
    echo [2/5] Installing dependencies...
    
    call "%PYTHON_PATH%" -m pip install --upgrade pip
    
    call "%PYTHON_PATH%" -m pip install -r requirements.txt
    
    REM Also install textual-image for image preview support
    call "%PYTHON_PATH%" -m pip install textual-image>=1.3.0
    
    if errorlevel 1 (
        echo Some packages failed to install. Continuing anyway...
    ) else (
        echo Dependencies installed successfully!
    )
)

REM Download backends and verify
if defined RESET (
    REM Full reset - download all backends from scratch
    call "%PYTHON_PATH%" scripts/setup/bootstrap.py --reset
) else (
    REM Normal bootstrap - check if backends exist
    call "%PYTHON_PATH%" scripts/setup/bootstrap.py --backend %BACKEND%
)

echo.
echo Scorch is ready! Run: python scorchpp.py
