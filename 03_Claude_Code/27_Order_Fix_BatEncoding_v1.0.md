# 27_Order_Fix_BatEncoding_v1.0.md
# KING Assistant OS — bat 파일 한글 인코딩 오류 수정

---

# 문제
run_embed.bat, run_server.bat 실행 시
한글이 깨져서 명령어 오류 발생

# 원인
bat 파일 내 한글 문자열이 인코딩 충돌로 명령어로 인식됨

# 해결
한글 echo 문자열을 모두 영문으로 교체

---

# [수정 1] run_embed.bat 전체 교체

기존 파일 전체를 아래 내용으로 교체한다:

```bat
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
```

---

# [수정 2] run_server.bat 전체 교체

기존 파일 전체를 아래 내용으로 교체한다:

```bat
@echo off
cd /d C:\Obsidian\Dooly\05_RAG

echo ============================================
echo  Dooly RAG Server Start
echo  URL: http://localhost:8000
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

python -m uvicorn server:app --host 0.0.0.0 --port 8000

pause
```

---

# [수정 3] start.bat 전체 교체

기존 파일 전체를 아래 내용으로 교체한다:

```bat
@echo off
echo ============================================
echo  Dooly RAG System
echo ============================================
echo.
echo  First time or data changed:
echo    run_embed.bat
echo.
echo  Daily use:
echo    run_server.bat
echo.
echo ============================================
pause
```

---

# 작업 완료 후

```
git add 05_RAG/ && git commit -m "fix: bat file encoding - replace Korean with English" && git push
```
