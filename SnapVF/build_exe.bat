@echo off
chcp 65001 >nul
echo === Cai thu vien ===
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller || goto :err
echo === Dong goi SnapVF.exe ===
python -m PyInstaller --noconfirm --onefile --windowed --name SnapVF ^
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
