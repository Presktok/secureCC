@echo off
set "PATH=C:\msys64\mingw64\bin;%PATH%"

echo Starting SecureCC Project (Backend and Frontend)...

:: Start backend in a new window
echo Launching Backend...
start "SecureCC Backend" cmd /c "cd backend && .\.venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

:: Start frontend in a new window
echo Launching Frontend...
start "SecureCC Frontend" cmd /c "cd frontend && npm start"

echo Both processes are launching in separate windows.
pause
