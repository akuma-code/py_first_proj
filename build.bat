@echo off
chcp 65001 >nul
echo === Сборка netCalculator ===
pyinstaller --onefile --windowed --name netCalculator --clean netCalculator.py
if errorlevel 1 (
    echo.
    echo ОШИБКА сборки. Проверь, установлен ли PyInstaller: pip install pyinstaller
    pause
    exit /b 1
)
echo.
echo Готово! Файл: dist\netCalculator.exe
pause