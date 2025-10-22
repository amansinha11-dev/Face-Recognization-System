@echo off
setlocal
cd /d "%~dp0"
echo Starting Unified Launcher (Login -> Main)...

rem Prefer Python 3.12, then fallback to py -3 / python
py -3.12 "unified_launcher.py" 2>nul || py -3 "unified_launcher.py" 2>nul || python "unified_launcher.py"

endlocal
