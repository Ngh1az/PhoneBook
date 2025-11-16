# =========================================
# Build script for PhoneBook Application (PowerShell)
# Tạo file .exe từ Python code bằng PyInstaller
# =========================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PHONEBOOK - BUILD SCRIPT (PowerShell)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kích hoạt virtual environment
Write-Host "[1/5] Activating virtual environment..." -ForegroundColor Yellow
try {
    & ".\.venv\Scripts\Activate.ps1"
    Write-Host "OK - Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Cannot activate virtual environment!" -ForegroundColor Red
    Write-Host "Please run: python -m venv .venv" -ForegroundColor Red
    pause
    exit 1
}
Write-Host ""

# Kiểm tra PyInstaller
Write-Host "[2/5] Checking PyInstaller..." -ForegroundColor Yellow
try {
    python -c "import PyInstaller" 2>$null
    if ($LASTEXITCODE -ne 0) { throw }
    Write-Host "OK - PyInstaller ready" -ForegroundColor Green
} catch {
    Write-Host "PyInstaller not found. Installing..." -ForegroundColor Yellow
    pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Cannot install PyInstaller!" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host "OK - PyInstaller installed" -ForegroundColor Green
}
Write-Host ""

# Xóa build cũ
Write-Host "[3/5] Cleaning old build files..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "__pycache__") { Remove-Item -Recurse -Force "__pycache__" }
Write-Host "OK - Cleaned" -ForegroundColor Green
Write-Host ""

# Build
Write-Host "[4/5] Building with PyInstaller..." -ForegroundColor Yellow
Write-Host "This may take 2-5 minutes..." -ForegroundColor Gray
Write-Host ""
pyinstaller --clean --noconfirm PhoneBook.spec
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Build failed!" -ForegroundColor Red
    pause
    exit 1
}
Write-Host ""
Write-Host "OK - Build successful!" -ForegroundColor Green
Write-Host ""

# Kết quả
Write-Host "[5/5] Build completed!" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "OUTPUT FILE: dist\PhoneBook.exe" -ForegroundColor Green
Write-Host ""
Write-Host "To run the application:" -ForegroundColor White
Write-Host "  1. Navigate to: dist\" -ForegroundColor Gray
Write-Host "  2. Run: PhoneBook.exe" -ForegroundColor Gray
Write-Host ""
Write-Host "NOTE: Make sure MySQL server is running!" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

pause
