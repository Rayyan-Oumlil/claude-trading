@echo off
REM Pre-market routine wrapper. Called by Windows Task Scheduler.
REM Logs to routines_pkg/logs/premarket.log

cd /d "%~dp0.."
set PYTHONPATH=%CD%
if not exist "routines_pkg\logs" mkdir "routines_pkg\logs"

echo [%date% %time%] Pre-market routine starting >> routines_pkg\logs\premarket.log
python routines_pkg\premarket.py >> routines_pkg\logs\premarket.log 2>&1
echo [%date% %time%] Pre-market routine finished with exit code %errorlevel% >> routines_pkg\logs\premarket.log
echo. >> routines_pkg\logs\premarket.log
