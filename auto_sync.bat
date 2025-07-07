@echo off
echo 自动同步 FastAPI 到 Apifox
echo 时间: %date% %time%

cd /d "%~dp0"
python sync_to_apifox.py

echo 同步完成，等待下次执行...
timeout /t 3600 /nobreak >nul
goto :eof 