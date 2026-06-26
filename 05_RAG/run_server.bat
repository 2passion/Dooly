@echo off
chcp 65001 >nul
echo =============================================
echo   Dooly RAG 서버 실행
echo =============================================
echo.

cd /d C:\Obsidian\Dooly\05_RAG

echo [확인] Ollama 실행 중인지 확인...
curl -s http://localhost:11434 >nul 2>&1
if %errorlevel% neq 0 (
    echo Ollama가 실행되지 않았습니다. 자동 시작 시도 중...
    start "" "C:\Users\%USERNAME%\AppData\Local\Programs\Ollama\ollama.exe" serve
    timeout /t 3 /nobreak >nul
)

echo.
echo [확인] 벡터DB 존재 여부 확인...
if not exist "C:\Obsidian\Dooly\05_RAG\db\chroma.sqlite3" (
    echo 벡터DB가 없습니다. 임베딩을 먼저 실행합니다...
    python embed.py
    echo.
)

echo.
echo =============================================
echo   서버 시작: http://localhost:8000
echo   Dooly 챗봇: index.html 열고 Dooly 탭 클릭
echo   서버 종료: 이 창을 닫거나 Ctrl+C
echo =============================================
echo.

python -m uvicorn server:app --host 0.0.0.0 --port 8000

pause
