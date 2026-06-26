@echo off
cd /d C:\Obsidian\Dooly\05_RAG

echo ============================================
echo  Dooly RAG Server Start
echo  URL: http://localhost:8001
echo  Stop: Close this window or Ctrl+C
echo ============================================
echo.

echo [Check] Ollama running...
curl -s http://localhost:11434 >nul 2>&1
if %errorlevel% neq 0 (
    echo [Info] Starting Ollama...
    start "" "C:\Users\%USERNAME%\AppData\Local\Programs\Ollama\ollama.exe" serve
    timeout /t 3 /nobreak >nul
)

echo [Check] VectorDB exists...
if not exist "C:\Obsidian\Dooly\05_RAG\db\chroma.sqlite3" (
    echo [Info] DB not found. Running embed.py first...
    python embed.py
    echo.
)

echo.
echo [Starting] uvicorn server...
echo.

python -m uvicorn server:app --host 0.0.0.0 --port 8001

pause
