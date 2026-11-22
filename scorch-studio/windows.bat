@echo off
setlocal enabledelayedexpansion

REM Scorch Windows Launcher - Portable AI Studio
REM Downloads Python portable binary, installs dependencies, fetches backends, launches TUI

if not exist runtime\python.exe (
    echo [1/6] Downloading portable Python 3.12...
    curl -L https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe -o python-installer.exe
    if errorlevel 1 (
        echo ERROR: Failed to download Python installer
        pause
        exit /b 1
    )
    start /wait python-3.12.9-amd64.exe install --yes
    del python-installer.exe
)

if not exist runtime\python.exe (
    echo [2/6] Extracting portable Python...
    if not exist runtime\python.tar.gz curl -L https://www.python.org/ftp/python/3.12.9/Python-3.12.9-amd64.tar.gz -o python.tar.gz
    tar xvf python.tar.gz
)

if not exist "runtime\Scripts" (
    echo [3/6] Creating virtual environment...
    cd runtime
    if not exist Scripts python.exe -m venv Scripts
    cd ..
    
    if not exist Scripts (
        echo ERROR: Failed to create virtual environment
        del runtime\python.tar.gz 2>nul
        pause
        exit /b 1
    )
)

echo [4/6] Installing dependencies...
cd runtime\Scripts
pip install --upgrade pip >nul 2>&1
pip install -q textual pydantic httpx psutil markdown textual-image pytest pytest-asyncio pilot tqdm tqdm-client ^
             llama-cpp-python stable-diffusion-pytorch torchvision torchaudio torch 2>nul

if not exist Scripts (
    echo ERROR: Failed to install dependencies
    del runtime\Scripts\pip.exe 2>nul
    pause
    exit /b 1
)
cd ..

echo [5/6] Detecting GPU backend...
set BACKEND=cpu
for /f "tokens=*" %%i in ('nvidia-smi 2^>^&1') do (
    if defined SMID set BACKEND=cuda
    break
)

if not defined BACKEND for /f "tokens=*" %%i in ('rocminfo 2^>^&1') do (
    if not defined BACKED set BACKEND=rocm
    break
)

if not defined BACKEND for /f "tokens=*" %%i in ('vulkaninfo --version 2^>^&1') do (
    if not defined BACKED set BACKEND=vulkan
    break
)

if not defined BACKED set BACKEND=cpu

echo [6/6] Launching Scorch...
cd backend\%BACKEND%\..
start "" "%~dp0scorch.exe" --backend %BACKEND%

pause