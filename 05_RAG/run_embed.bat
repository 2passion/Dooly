@echo off
chcp 65001 >nul
echo =============================================
echo   Dooly 임베딩 실행
echo   docs 폴더의 txt 파일을 벡터DB에 저장합니다
echo =============================================
echo.

cd /d C:\Obsidian\Dooly\05_RAG

echo [1/2] Python 버전 확인 중...
python --version
if %errorlevel% neq 0 (
    echo Python이 설치되지 않았습니다.
    pause
    exit /b 1
)

echo.
echo [2/2] 임베딩 실행 중... (처음 실행 시 모델 다운로드로 수 분 소요)
python embed.py

echo.
if %errorlevel% equ 0 (
    echo =============================================
    echo   임베딩 완료!
    echo   이제 run_server.bat 을 실행하세요.
    echo =============================================
) else (
    echo =============================================
    echo   오류가 발생했습니다.
    echo   위의 오류 메시지를 확인하세요.
    echo =============================================
)

pause
