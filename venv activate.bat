@echo off
cd /d %~dp0
powershell -NoExit -ExecutionPolicy Bypass -File ".\venv\Scripts\activate.ps1"