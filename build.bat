@echo off
REM =========================================
REM Build script for PhoneBook Application
REM Tạo file .exe từ Python code bằng PyInstaller
REM =========================================

echo ========================================
echo PHONEBOOK - BUILD SCRIPT
echo ========================================
echo.

REM Kích hoạt virtual environment
echo [1/5] Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Cannot activate virtual environment!
    echo Please run: python -m venv .venv
    pause
    exit /b 1
)
echo OK - Virtual environment activated
echo.

REM Kiểm tra PyInstaller đã cài chưa
echo [2/5] Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ERROR: Cannot install PyInstaller!
        pause
        exit /b 1
    )
)
echo OK - PyInstaller ready
echo.

REM Xóa build cũ
echo [3/5] Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
echo OK - Cleaned
echo.

REM Build với PyInstaller
echo [4/5] Building with PyInstaller...
echo This may take 2-5 minutes...
echo.
pyinstaller --clean --noconfirm PhoneBook.spec
if %errorlevel% neq 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)
echo.
echo OK - Build successful!
echo.

REM Hiển thị kết quả
echo [5/5] Build completed!
echo ========================================
echo.
echo OUTPUT FILE: dist\PhoneBook.exe
echo.
echo To run the application:
echo   1. Navigate to: dist\
echo   2. Run: PhoneBook.exe
echo.
echo NOTE: Make sure MySQL server is running!
echo ========================================
echo.

pause
