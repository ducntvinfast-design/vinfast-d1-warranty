@echo off
py -m pip install -r "%~dp0requirements.txt" >nul
start "" pyw "%~dp0snapvf.py"
