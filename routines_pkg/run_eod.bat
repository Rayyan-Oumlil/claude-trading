@echo off
REM EOD close routine wrapper. Called by Windows Task Scheduler.
REM Logs to routines_pkg/logs/eod.log

cd /d "%~dp0.."
set PYTHONPATH=%CD%
if not exist "routines_pkg\logs" mkdir "routines_pkg\logs"

echo [%date% %time%] EOD close routine starting >> routines_pkg\logs\eod.log
python routines_pkg\eod_close.py >> routines_pkg\logs\eod.log 2>&1
echo [%date% %time%] EOD close routine finished with exit code %errorlevel% >> routines_pkg\logs\eod.log
echo. >> routines_pkg\logs\eod.log
