@echo off
set "PATH=C:\msys64\mingw64\bin;%PATH%"
echo Starting SecureCC Backend...
cd backend
.\.venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
