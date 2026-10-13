@echo off
python -m pip install -r "%~dp0requirements.txt" >nul
start "" pythonw "%~dp0snapvf.py"
