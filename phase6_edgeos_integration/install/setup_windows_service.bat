@echo off
echo ?? Edge TinyML Assistant - Windows Service Setup
echo ===============================================

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ? Please run this script as Administrator
    pause
    exit /b 1
)

echo ? Running as Administrator - Proceeding with installation...

REM Install Python service
echo.
echo ?? Installing Windows Service...
python "%~dp0..\service\assistant_service.py" install

if %errorLevel% equ 0 (
    echo ? Service installed successfully!
) else (
    echo ? Service installation failed
    pause
    exit /b 1
)

echo.
echo ?? Starting Service...
python "%~dp0..\service\assistant_service.py" start

if %errorLevel% equ 0 (
    echo ? Service started successfully!
) else (
    echo ? Service start failed
    pause
    exit /b 1
)

echo.
echo ?? EDGE TINYML ASSISTANT SERVICE INSTALLED!
echo.
echo ?? Service Information:
echo    Name: EdgeTinyMLAssistant
echo    Display: Edge TinyML AI Assistant  
echo    Status: Running
echo    Auto-start: Yes
echo.
echo ???  Management Commands:
echo    Stop: python "%~dp0..\service\assistant_service.py" stop
echo    Start: python "%~dp0..\service\assistant_service.py" start
echo    Remove: python "%~dp0..\service\assistant_service.py" remove
echo.
echo ?? To verify: Open Services.msc and look for "Edge TinyML AI Assistant"
echo.

pause
