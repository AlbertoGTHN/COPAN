@echo off
SET EXPOSE_RAW_FEATURES=true
cd /d "%~dp0"
py -m uvicorn app.main:app --host 127.0.0.1 --port 8000
