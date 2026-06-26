# 26_Order_RAG_StartBat_v1.0.md
# KING Assistant OS — RAG 서버 원클릭 실행 bat 파일 개선

---

# 작업 개요
현재 start.bat은 서버만 실행함.
아래 2개 bat 파일로 개선:
- run_embed.bat : 임베딩 전용 (데이터 변경 시 실행)
- run_server.bat : 서버 실행 전용 (매일 실행)

---

# 수정 대상
C:\Obsidian\Dooly\05_RAG\start.bat     ← 내용 교체
C:\Obsidian\Dooly\05_RAG\run_embed.bat ← 신규 생성
C:\Obsidian\Dooly\05_RAG\run_server.bat ← 신규 생성

---

# [작업 1] start.bat 내용 교체

기존 start.bat 전체 내용을 아래로 교체한다:

```bat
@echo off
chcp 65001 >nul
echo =============================================
echo   Dooly RAG 시스템 안내
echo =============================================
echo.
echo [최초 실행 또는 데이터 변경 시]
echo   run_embed.bat 더블클릭
echo.
echo [매일 서버 실행 시]
echo   run_server.bat 더블클릭
echo.
echo =============================================
pause
```

---

# [작업 2] run_embed.bat 신규 생성

아래 내용으로 C:\Obsidian\Dooly\05_RAG\run_embed.bat 파일을 생성한다:

```bat
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
```

---

# [작업 3] run_server.bat 신규 생성

아래 내용으로 C:\Obsidian\Dooly\05_RAG\run_server.bat 파일을 생성한다:

```bat
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
```

---

# [작업 4] README_RAG.txt 신규 생성

아래 내용으로 C:\Obsidian\Dooly\05_RAG\README_RAG.txt 파일을 생성한다:

```
=============================================
  Dooly RAG 시스템 사용 방법
=============================================

[처음 설치 후]
1. run_embed.bat 더블클릭 → 임베딩 완료 대기
2. run_server.bat 더블클릭 → 서버 실행
3. 브라우저에서 index.html 열기 → Dooly 탭

[매일 사용할 때]
1. run_server.bat 더블클릭
2. 브라우저에서 index.html 열기 → Dooly 탭

[SOP/FAQ 데이터 변경 후]
1. run_embed.bat 더블클릭 → 재임베딩
2. run_server.bat 더블클릭 → 서버 재실행

[docs 폴더에 새 파일 추가 방법]
- C:\Obsidian\Dooly\05_RAG\docs\ 에 txt 파일 추가
- run_embed.bat 다시 실행
- 자동으로 검색 대상에 포함됨

[폴더 구조]
05_RAG\
├── docs\
│   ├── sop_data.txt     ← SOP 22개
│   └── faq_data.txt     ← FAQ 22개
│   └── (추가 txt 파일)  ← 자유롭게 추가 가능
├── db\                  ← 벡터DB (자동 생성)
├── embed.py             ← 임베딩 스크립트
├── server.py            ← FastAPI 서버
├── run_embed.bat        ← 임베딩 실행 (더블클릭)
├── run_server.bat       ← 서버 실행 (더블클릭)
└── README_RAG.txt       ← 이 파일

[서버 주소]
로컬: http://localhost:8000
같은 와이파이 스마트폰: http://[PC_IP]:8000
예) http://192.168.0.10:8000

[PC IP 확인 방법]
cmd에서: ipconfig
IPv4 주소 확인
=============================================
```

---

# 작업 완료 후

```
git add 05_RAG/ && git commit -m "feat: RAG one-click bat files, README_RAG" && git push
```
