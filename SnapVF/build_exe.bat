@echo off
chcp 65001 >nul
set PY=
where py >nul 2>nul && set PY=py
if not defined PY (python --version >nul 2>nul && set PY=python)
if not defined PY (
  echo Chua cai Python. Tai tai https://www.python.org/downloads/ va tick "Add python.exe to PATH".
  start https://www.python.org/downloads/
  pause
  exit /b 1
)
echo === Cai thu vien ===
%PY% -m pip install --upgrade pip
%PY% -m pip install -r requirements.txt pyinstaller || goto :err
echo === Dong goi SnapVF.exe ===
%PY% -m PyInstaller --noconfirm --onefile --windowed --name SnapVF ^
  --hidden-import pystray._win32 ^
  --hidden-import pynput.keyboard._win32 ^
  --hidden-import pynput.mouse._win32 ^
  snapvf.py || goto :err
echo.
echo XONG! File chay: %cd%\dist\SnapVF.exe
pause
exit /b 0
:err
echo Co loi xay ra, xem thong bao phia tren.
pause
exit /b 1
