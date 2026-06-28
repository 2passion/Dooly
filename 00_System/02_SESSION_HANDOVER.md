# 02_SESSION_HANDOVER.md v6.0

작성일: 2026-06-28
세션: 2026-06-28
프로젝트 버전: King Assistant OS v1.0
현재 마일스톤: Phase 8 진행 중 (Task API + 스마트폰 테스트)

---

# 0. AI 인수인계 규칙

새 세션의 AI는 반드시 다음 순서로 시작한다.

1. 이 파일 (02_SESSION_HANDOVER.md) 읽기
2. 04_PROJECT_GUIDE_v1.0.md 읽기
3. 05_WORKFLOW_GUIDE_v1.0.md 읽기
4. 현재 마일스톤 파악
5. 작업지시서 번호 순서대로 작업 진행

이미 완료된 작업은 다시 구현하지 않는다.
작업지시서 번호는 반드시 순서를 유지한다. (현재 48번까지 진행 중)
다음 작업은 49번부터 시작한다.

---

# 1. 워크플로우 원칙 (반드시 준수)

- claude.ai: 검토 + 작업지시서 md 파일 생성 (다운로드 제공)
- Claude Code (VS Code): md 파일 읽고 실행 + git push
- 인수인계 md 파일 작성도 동일하게 claude.ai에서 생성 → Claude Code에서 저장/push
- claude.ai에서 직접 파일을 실행하거나 git 명령을 수행하지 않음

---

# 2. 현재 시스템 구조

```
사용자 (스마트폰/PC)
        │
        ▼
https://2passion.github.io/Dooly/
(GitHub Pages - 24시간 무료)
        │
        ▼
HTML + data.js (브라우저 캐시)
        │
        ├── Mock 모드 (기본)
        │   → data.js 키워드 매칭
        │   → FAQ/SOP 즉시 답변
        │
        └── Task API (48번 추가)
            → 학원 내부 와이파이 전용
            → 자습실 PC FastAPI → tasks.json
```

---

# 3. 완료된 작업 (이번 세션)

| 번호 | 작업 | 커밋 | 상태 |
|------|------|------|------|
| 46 | 인수인계 파일 업데이트 | - | ✅ |
| 47 | 아이폰 PWA 설치 가이드 | cfcb795 | ✅ |
| 48A | 자습실 PC FastAPI Task API 추가 | - | ✅ |
| 48B | PWA Task 화면 FastAPI 연동 | d9769a8 | ✅ |
| 48B-fix | IP 주소 수정 (219.100 → 0.10) | d9769a8 포함 | ✅ |

---

# 4. 환경 정보

| 항목 | 내용 |
|------|------|
| GitHub Pages URL | https://2passion.github.io/Dooly/ |
| 자습실 PC IP | 192.168.0.10 |
| 자습실 PC FastAPI 포트 | 8001 |
| FastAPI 파일 위치 | C:\Obsidian\Dooly\05_RAG\server.py |
| tasks.json 경로 | C:\★공유폴더★\Sync\Dooly\tasks.json |
| run_server.bat | C:\Obsidian\Dooly\05_RAG\run_server.bat |
| ngrok 도메인 | polymer-distinct-feminize.ngrok-free.dev |
| Task API 접속 (내부) | http://192.168.0.10:8001 |
| Task API 접속 (외부) | 50번에서 Cloudflare Tunnel 예정 |

---

# 5. 이번 세션 시행착오 기록

## 48A — 자습실 PC FastAPI Task API 추가

### 에러 1: tasks.json BOM 문제
- **증상**: /tasks 엔드포인트 500 에러
- **원인**: PowerShell 5.1의 `Set-Content -Encoding UTF8`이 BOM(EF BB BF)을 파일 앞에 붙임 → Python json.load 실패
- **해결**: BOM 없는 UTF-8로 재작성
  ```powershell
  $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText("경로\tasks.json", "[]", $utf8NoBom)
  ```
- **향후 주의**: tasks.json 생성 시 반드시 BOM 없는 UTF-8 사용

### 에러 2: 자습실 PC IP 주소 변경
- **증상**: 스마트폰에서 Task API 연결 안 됨
- **원인**: 작업지시서에 이전 IP(192.168.219.100) 기재, 실제 IP는 192.168.0.10으로 변경됨
- **해결**: 48B 작업지시서 IP 수정 후 재배포
- **향후 주의**: 자습실 PC IP가 고정 IP가 아님. 공유기 재시작 시 IP 변경 가능성 있음
  → 50번 Cloudflare Tunnel 적용하면 IP 문제 해결됨

### 에러 3: Python 서버 2개 중복 실행
- **증상**: 포트 8001 충돌 에러
  ```
  ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8001)
  ```
- **원인**: Claude Code가 백그라운드로 서버 실행 → 기존 서버와 중복
- **해결**: 기존 프로세스 종료 후 run_server.bat으로 정식 실행
  ```powershell
  Stop-Process -Id [PID] -Force
  Start-Process "C:\Obsidian\Dooly\05_RAG\run_server.bat"
  ```
- **향후 주의**: 서버 실행 전 반드시 포트 8001 사용 여부 확인

---

## 48B — PWA Task 화면 문제

### 에러 4: 🟢 온라인 상태 표시 안 됨
- **증상**: PWA 업무 탭에서 동기화 상태 바가 보이지 않음
- **원인 1**: IP 주소 불일치 (위 에러 2 참고)
- **원인 2**: 서비스워커 캐시가 이전 버전 HTML을 계속 제공
- **해결**: 서비스워커 Unregister 후 재접속
  ```
  chrome://serviceworker-internals
  → 2passion.github.io/Dooly 항목 → Unregister
  ```

### 에러 5: 서비스워커 Unregister 후 404
- **증상**: Unregister 후 접속 시 404 File not found
- **원인**: 캐시 완전 삭제 후 GitHub Pages에서 새로 받아오는 과정
- **해결**: 정확한 URL로 재접속 (`https://2passion.github.io/Dooly/`)
- **향후 주의**: 404가 떠도 당황하지 말고 URL 재입력

### 에러 6: data.js 404
- **증상**: 스마트폰에서 data.js 접속 시 404
- **원인**: GitHub Pages 캐시 미갱신 (파일은 GitHub에 존재함)
- **해결 중**: data.js에 주석 추가 후 강제 재배포 예정
- **현재 상태**: ⚠️ 미해결 → 49번 작업에서 해결 필요

---

## 기타 확인 사항

### 브라우저별 PWA 지원
| 브라우저 | PWA 지원 |
|------|------|
| Chrome | ✅ 정상 |
| 삼성 브라우저 | ✅ 정상 |
| 네이버 앱 | ❌ 지원 안 됨 |
| 카카오톡 인앱 | ❌ 지원 안 됨 |

### 자습실 PC run_server.bat 주의사항
- 창을 닫으면 서버도 함께 종료됨
- Ollama + FastAPI 함께 실행됨
- Task API는 Ollama 없어도 동작 (/chat만 Ollama 필요)

---

# 6. 다음 작업 목록

| 번호 | 작업 | 우선순위 | 비고 |
|------|------|---------|------|
| **49** | data.js 캐시 강제 갱신 + 스마트폰 테스트 완료 | 높음 | 에러 6 해결 |
| **50** | Cloudflare Tunnel 연동 | 보통 | IP 고정 문제 해결 |
| **51** | SETUP_GUIDE.md 작성 | 보통 | |
| **52** | Claude API 전환 (v2.0 준비) | 낮음 | |

---

# 7. 49번 작업 내용 (다음 세션 즉시 진행)

## 목표
data.js GitHub Pages 캐시 강제 갱신

## 방법
노트북(화이트) Claude Code에서:

```
C:\Obsidian\Dooly\docs\data.js 파일 맨 첫 줄에
// cache-bust: 2026-06-28
한 줄 추가

C:\Obsidian\Dooly\04_Runtime\data.js 에도 동일하게 추가

git add .
git commit -m "fix: GitHub Pages 캐시 강제 갱신 (#49)"
git push
```

## 완료 확인
- 스마트폰에서 https://2passion.github.io/Dooly/data.js 접속 → 내용 표시
- 스마트폰 PWA 업무 탭 → 🟢 온라인 표시 확인
- Task 추가 → tasks.json 저장 확인
- 조교A 추가 → 조교B에서 보임 확인

---

# 8. 자습실 PC 현재 상태

| 항목 | 상태 |
|------|------|
| FastAPI 서버 | ✅ 실행 중 (포트 8001) |
| Ollama | ✅ 실행 중 (포트 11434) |
| tasks.json | ✅ 생성 완료 |
| Task API /ping | ✅ 응답 정상 |
| 스마트폰 /ping 접속 | ✅ 확인됨 (192.168.0.36에서 접속) |

---

# 9. 새 세션 시작 방법

```
1. 02_SESSION_HANDOVER.md 첨부
2. 04_PROJECT_GUIDE_v1.0.md 첨부
3. 05_WORKFLOW_GUIDE_v1.0.md 첨부
4. 아래 메시지 입력:
   "첨부한 파일을 읽고 프로젝트 현황을 파악해줘.
    다음 작업은 49번부터 이어서 진행할거야."
```
