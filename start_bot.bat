@echo off
echo ╔════════════════════════════════════════════╗
echo ║       KENXI USERBOT - START SCRIPT         ║
echo ╚════════════════════════════════════════════╝
echo.

echo [STEP 1/3] Checking for running Python processes...
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [WARNING] Python process detected! Cleaning up...
    taskkill /F /IM python.exe >NUL 2>&1
    timeout /t 2 /nobreak >NUL
    echo [SUCCESS] Cleanup complete
) else (
    echo [SUCCESS] No conflicts detected
)

echo.
echo [STEP 2/3] Cleaning session locks...
if exist "database\helper_bot.session-journal" (
    del /F /Q "database\helper_bot.session-journal" >NUL 2>&1
    echo [SUCCESS] Removed session journal
)

echo.
echo [STEP 3/3] Starting KENXI Userbot...
echo ═══════════════════════════════════════════
echo.

python main.py

echo.
echo ═══════════════════════════════════════════
echo [INFO] Bot has stopped
echo.
pause
