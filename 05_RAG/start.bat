@echo off
echo Dooly RAG 서버 시작 중...
echo.
echo 1. 임베딩 실행 (최초 1회 또는 데이터 변경 시)
echo    python embed.py
echo.
echo 2. 서버 실행
cd /d C:\Obsidian\Dooly\05_RAG
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
pause
