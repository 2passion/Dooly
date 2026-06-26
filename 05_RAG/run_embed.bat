@echo off
cd /d C:\Obsidian\Dooly\05_RAG

echo ============================================
echo  Dooly Embedding Start
echo ============================================
echo.

python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found.
    pause
    exit /b 1
)

echo.
echo [Running] python embed.py ...
echo [Note] First run downloads model (few minutes)
echo.

python embed.py

echo.
if %errorlevel% equ 0 (
    echo ============================================
    echo  Embedding Done! Run run_server.bat next.
    echo ============================================
) else (
    echo ============================================
    echo  [ERROR] Check error message above.
    echo ============================================
)

pause
