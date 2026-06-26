# KING Assistant OS — 프로젝트 전체 가이드
> 킹수학 조교 운영 시스템 구축 전체 과정
> 작성일: 2026-06-26
> 최신 커밋: 4ab9bd9 — feat: FastAPI static HTML serving for mobile access

---

## 1. 프로젝트 개요

### 1-1. 목적

킹수학 학원 조교의 반복 업무를 표준화하고, AI 비서 둘리(Dooly)를 통해 업무 운영 효율을 향상시킨다.
학원 전체 운영 시스템이 아닌, **조교 운영 시스템** 구축이 목표다.

MVP 5개 기능:
- 업무 관리 (Task)
- SOP 검색
- FAQ 검색
- 공지사항 조회 (홈 통합)
- 둘리 질의응답 (RAG 기반 AI)

### 1-2. 기술 스택

| 영역 | 기술 |
|------|------|
| 프론트엔드 | Single-page HTML + localStorage (백엔드 없음) |
| AI 서버 | FastAPI + ChromaDB + Ollama |
| 임베딩 모델 | paraphrase-multilingual-MiniLM-L12-v2 |
| LLM 모델 | qwen2.5:7b (기본), qwen2.5:3b, gemma3:4b 선택 가능 |
| 버전 관리 | Git (main 단일 브랜치) |
| 원격 저장소 | https://github.com/2passion/Dooly.git |

### 1-3. 폴더 구조

```
C:\Obsidian\Dooly\
├── 00_System\          ← 시스템 문서 (마스터, 인수인계, 규칙, 가이드)
├── 01_Project\         ← 설계 문서
├── 02_Claude_Project\  ← Claude Project 지침
├── 03_Claude_Code\     ← Claude Code 작업지시서 (11번~)
├── 04_Runtime\         ← HTML 실행 파일 (7개)
├── 05_RAG\             ← RAG 서버 (FastAPI + ChromaDB + Ollama)
└── 99_Archive\         ← 아카이브 (git 제외)
```

---

## 2. 환경 준비 (Phase 0)

### 2-1. 필수 소프트웨어 설치

**Python 3.13.9**
- https://www.python.org/downloads/ 에서 설치
- 설치 시 "Add Python to PATH" 반드시 체크

**Ollama 0.30.10**
- https://ollama.com/download 에서 설치
- 설치 후 자동으로 백그라운드 서비스 실행됨

**Ollama 모델 다운로드** (cmd에서 실행)
```
ollama pull qwen2.5:7b
ollama pull qwen2.5:3b
ollama pull gemma3:4b
```
- qwen2.5:7b: 고품질 (기본값)
- qwen2.5:3b: 빠름
- gemma3:4b: 균형

**Python 패키지 설치** (cmd에서 실행)
```
pip install fastapi uvicorn chromadb sentence-transformers ollama PyPDF2
```

### 2-2. GitHub 저장소 생성 및 연결

```
cd C:\Obsidian\Dooly
git init
git remote add origin https://github.com/2passion/Dooly.git
git branch -M main
git push -u origin main
```

### 2-3. Obsidian 폴더 구조 생성

```
mkdir C:\Obsidian\Dooly\00_System
mkdir C:\Obsidian\Dooly\03_Claude_Code
mkdir C:\Obsidian\Dooly\04_Runtime
mkdir C:\Obsidian\Dooly\05_RAG
mkdir C:\Obsidian\Dooly\05_RAG\docs
mkdir C:\Obsidian\Dooly\99_Archive
```

### 2-4. .gitignore 설정

`C:\Obsidian\Dooly\.gitignore` 생성:
```
99_Archive/
05_RAG/db/
05_RAG/__pycache__/
```

### 2-5. 시스템 문서 작성 (00_System)

- `01_PROJECT_MASTER.md` — 프로젝트 전체 상태 요약
- `02_SESSION_HANDOVER.md` — 세션 간 인수인계 기록
- `03_DEVELOPMENT_RULE_v1.0.md` — 개발 운영 규칙
- `04_PROJECT_GUIDE_v1.0.md` — 이 문서

---

## 3. HTML 프로토타입 구축 (Phase 1)

### 3-1. HTML 파일 7개 생성 (작업지시서 11번)

`04_Runtime\` 폴더에 아래 파일 생성:

| 파일 | 기능 |
|------|------|
| index.html | 홈 + 주간/월간 달력 + 공지사항 |
| 02_Task_v1.html | 업무 추가/조회/상태변경/담당자/삭제 |
| 03_SOP_v1.html | SOP 카테고리 필터 + 실시간 검색 + 상세 보기 |
| 04_FAQ_v1.html | FAQ 카테고리 필터 + 실시간 검색 + 아코디언 |
| 05_Notice_v1.html | index.html로 자동 리다이렉트 |
| 06_Dooly_v1.html | AI 채팅 UI (RAG 연동) |
| 07_Settings_v1.html | 담당자 관리 + 데이터 초기화 |

모든 파일 공통 특징:
- localStorage 기반 데이터 저장 (백엔드 없음)
- 최대 430px 모바일 레이아웃
- 다크 테마 (#0b0f1a 배경, #4da3ff 포인트 색)
- 하단 6탭 네비게이션: 홈 / 업무 / SOP / FAQ / Dooly / 설정

### 3-2. UI 개선 (작업지시서 12~16번)

- KING 텍스트 표시, 한국어 우선, 항목 번호 표시
- 날짜별 파일명 형식 안내
- 드래그 재정렬 (SOP, FAQ, 공지, 업무 카드)
- JSON 다운로드/업로드 (데이터 백업)
- 업무 카드: 3단계 상태 (진행 전 / 진행 중 / 완료), 우선순위
- FAQ 아코디언, 담당자 메모 필드

### 3-3. 달력 + 설정 탭 추가 (작업지시서 17번)

- 홈 화면에 주간/월간 달력 토글 추가
- `weekOffset` 변수로 주간 화살표 이동 지원
- 설정 탭(07_Settings_v1.html) 신설: 담당자 추가/수정/삭제

---

## 4. 데이터 확장 (Phase 2)

### 4-1. SOP 22개 / 9카테고리 (작업지시서 18번)

`03_SOP_v1.html` 내부 JavaScript 배열에 직접 삽입.

9개 카테고리:
- 복테 관리 / 복사기 · 스캐너 / 제본 · 인쇄 / 비품 관리
- 채점 · 교재검사 / 루틴 / 학생관리 / 예외상황 / 기타

### 4-2. FAQ 22개 / 10카테고리 + Dooly 키워드 23개 (작업지시서 19번)

`04_FAQ_v1.html`에 FAQ 22개 삽입.
`06_Dooly_v1.html`의 `mockResponse()` 함수에 키워드 매핑 23개 추가.

---

## 5. UI 버그 수정 및 기능 개선 (Phase 3)

### 5-1. 체크박스 제거 + 상태 필터 (작업지시서 20번)

`02_Task_v1.html`:
- 업무 카드 체크박스 제거
- 상태 필터 바 추가 (전체 / 진행 전 / 진행 중 / 완료 / 홀드)
- 담당자 데이터 구조 변경: `string[]` → `[{name, memo}]` (마이그레이션 자동 처리)
- `loadAssigneeNames()` 함수로 이름만 추출하여 표시

`07_Settings_v1.html`:
- 담당자 콜랩서블 편집 UI (이름 + 메모 입력, 저장/삭제)
- localStorage 마이그레이션: `typeof a === 'string'` 체크 후 객체로 변환

### 5-2. 주간 달력 화살표 버그 수정 (작업지시서 21번)

`index.html`:
- 기존 버그: `prevMonth()`/`nextMonth()`에 주간 모드에서 `return` 처리하여 이동 불가
- 수정: `var weekOffset = 0` 추가, 화살표 클릭 시 `weekOffset` 증감, 날짜 계산에 반영
- `setCalView()` 호출 시 `weekOffset = 0` 초기화

### 5-3. SOP/FAQ URL 링크 + 경로 복사 버튼 (작업지시서 22~23번)

`03_SOP_v1.html`, `04_FAQ_v1.html`:
- `linkify()` 함수: http URL → `<a>` 링크, `C:\` 경로 → 복사 버튼
- `copyPath()`, `showToast()` 함수 추가
- SOP 본문, FAQ 답변에 `linkify(escHtml(...))` 적용

### 5-4. 공지 탭 홈으로 통합 (작업지시서 24번)

- 공지사항 기능을 `index.html`로 이전
- JSON 다운로드/업로드 버튼 추가
- 드래그 핸들로 공지 순서 변경
- `05_Notice_v1.html` → index.html로 리다이렉트 처리
- 네비게이션 탭 7개 → 6개 (공지 탭 제거)

---

## 6. RAG 서버 구축 (Phase 4)

### 6-1. 사전 설치 확인

```
python --version        # 3.13.9
ollama --version        # 0.30.10
ollama list             # qwen2.5:7b 확인
pip list | findstr fastapi
```

### 6-2. 05_RAG 폴더 구조

```
05_RAG\
├── docs\
│   ├── sop_data.txt     ← SOP 22개 텍스트
│   └── faq_data.txt     ← FAQ 22개 텍스트
├── db\                  ← Chroma 벡터DB (자동 생성, git 제외)
├── embed.py             ← 임베딩 스크립트
├── server.py            ← FastAPI RAG 서버
├── run_embed.bat        ← 임베딩 실행 (더블클릭)
├── run_server.bat       ← 서버 실행 (더블클릭)
├── start.bat            ← 초보자용 안내
└── README_RAG.txt       ← 사용 방법
```

### 6-3. docs 텍스트 형식

`sop_data.txt`, `faq_data.txt` 모두 동일 형식:
```
[SOP-1] 제목 | 카테고리: XXX
내용 텍스트...

[SOP-2] 제목 | 카테고리: XXX
내용 텍스트...
```
- 항목 구분: 빈 줄 (`\n\n`)
- embed.py가 빈 줄 기준으로 청크 분리

### 6-4. embed.py 동작

```python
# docs/ 폴더의 모든 .txt 파일 읽기
# \n\n 기준으로 청크 분리
# ChromaDB collection "dooly_docs"에 저장
# 임베딩 모델: paraphrase-multilingual-MiniLM-L12-v2
# DB 경로: C:\Obsidian\Dooly\05_RAG\db
```

### 6-5. server.py 구조

```python
# POST /chat
# - 요청: {message: str, model: str = "qwen2.5:7b"}
# - ChromaDB에서 top-3 문서 검색
# - Ollama로 컨텍스트 + 질문 전달
# - 반환: {answer: str, sources: [{type, label, file}]}

# GET /app           → index.html 반환
# GET /app/{filename} → 04_Runtime 폴더의 파일 반환
# GET /static/...    → 04_Runtime 정적 파일 서빙
```

### 6-6. 첫 실행 순서

1. `run_embed.bat` 더블클릭 → 임베딩 완료 대기 (최초 1회, 모델 다운로드 포함 5~10분)
2. `run_server.bat` 더블클릭 → 서버 실행
3. 브라우저에서 `http://localhost:8001/app` 접속

**이후 매일 사용:**
1. `run_server.bat` 더블클릭만 하면 됨

**데이터 변경 시:**
1. docs 폴더 txt 수정
2. `run_embed.bat` 실행 (재임베딩)
3. `run_server.bat` 실행

---

## 7. Dooly AI 고도화 (Phase 5)

### 7-1. 모델 선택 드롭다운 + 출처 태그 (작업지시서 29번)

`06_Dooly_v1.html`:
- 헤더 아래 모델 선택 드롭다운 추가 (A/B/C 3가지)
- fetch 요청에 `model` 필드 포함
- 답변 아래 출처 태그 표시: `FAQ Q1`, `SOP 3` 등
- 태그 색상: FAQ 초록 / SOP 주황 / DOC 보라

`server.py`:
- `ChatRequest`에 `model: str = "qwen2.5:7b"` 필드 추가
- 출처 메타데이터를 `{type, label, file}` 구조로 파싱하여 반환

### 7-2. 대화 기록 localStorage 유지 (작업지시서 30번)

`06_Dooly_v1.html`:
- `saveChatHistory()`: 답변 완료 시 `chatArea.innerHTML`을 localStorage 저장
- `loadChatHistory()`: 페이지 로드 시 복원 (없으면 초기 메시지)
- `clearChatHistory()`: localStorage 삭제 + 초기 메시지 표시
- 모델 선택 행 우측에 "대화 초기화" 버튼 추가
- localStorage 키: `dooly_chat_history`

### 7-3. 스마트폰 접속 (작업지시서 31번)

`server.py`:
- `StaticFiles`, `FileResponse` 추가
- `/static` 경로에 `04_Runtime` 폴더 마운트
- `/app`, `/app/{filename}` 라우트로 HTML 직접 서빙

`06_Dooly_v1.html`:
- `RAG_SERVER`를 `location.protocol` 기반으로 동적 설정
  - `file://` 로 열면 → `http://localhost:8001`
  - 서버 경유 시 → `http://{같은IP}:8001`

`run_server.bat`:
- 실행 시 PC/스마트폰 접속 URL 출력

---

## 8. 현재 시스템 완성 상태

### 8-1. HTML 파일 목록 및 기능

| 파일 | 탭 | 주요 기능 |
|------|-----|-----------|
| index.html | 홈 | 주간/월간 달력, 공지사항 관리 (JSON 업/다운, 드래그 정렬) |
| 02_Task_v1.html | 업무 | 업무 CRUD, 상태 필터, 담당자 지정, 드래그 정렬 |
| 03_SOP_v1.html | SOP | 22개 SOP, 카테고리 9개, 검색, URL 링크, 경로 복사 |
| 04_FAQ_v1.html | FAQ | 22개 FAQ, 카테고리 10개, 검색, URL 링크 |
| 05_Notice_v1.html | (없음) | index.html로 자동 리다이렉트 |
| 06_Dooly_v1.html | Dooly | RAG AI 채팅, 모델 선택, 출처 태그, 대화 기록 유지 |
| 07_Settings_v1.html | 설정 | 담당자 편집 (이름+메모), 전체 데이터 초기화 |

### 8-2. RAG 서버 파일 목록

| 파일 | 역할 |
|------|------|
| embed.py | 문서 임베딩 (최초 1회 또는 데이터 변경 시) |
| server.py | FastAPI 서버 (채팅 API + HTML 서빙) |
| run_embed.bat | 임베딩 실행 배치 |
| run_server.bat | 서버 실행 배치 |
| start.bat | 초보자용 안내 |
| README_RAG.txt | 사용법 안내 |
| docs/sop_data.txt | SOP 22개 텍스트 |
| docs/faq_data.txt | FAQ 22개 텍스트 |
| db/ | ChromaDB 벡터 데이터 (자동 생성) |

### 8-3. 설치 완료 목록

- Python 3.13.9
- Ollama 0.30.10
- qwen2.5:7b 모델
- qwen2.5:3b 모델 (선택)
- gemma3:4b 모델 (선택)
- fastapi, uvicorn, chromadb, sentence-transformers, ollama, PyPDF2

### 8-4. Git 커밋 히스토리

| 커밋 | 내용 |
|------|------|
| 4ab9bd9 | feat: FastAPI static HTML serving for mobile access |
| 54e2d19 | feat: Dooly chat history persist in localStorage + clear button |
| 4dcf9dc | feat: Dooly model A/B/C selector + source tag display |
| a1bf341 | fix: change RAG server port 8000 -> 8001 |
| 8ea1cb9 | fix: bat file encoding - replace Korean with English |
| 4b3bbb2 | feat: RAG one-click bat files, README_RAG |
| 69e55dd | feat: RAG setup with FastAPI + Chroma + Ollama, Dooly API integration |
| 95d6782 | feat: merge notice tab into home, remove notice nav tab |
| 5a498d6 | fix: week calendar nav, SOP/FAQ URL link + local path copy button |
| 405712b | fix: task checkbox remove+status filter, FAQ category tag+filter |
| 933aeb5 | feat: FAQ 12→22개, Dooly 키워드 12→23개 |
| aaeb936 | feat: SOP 13→22개 |
| ddb36aa | feat: home calendar, settings tab |
| 94ddb59 | feat: FAQ category filter, task overhaul |
| af249d1 | feat: KING text, drag reorder |
| 261fe74 | feat: home UI v3, JSON upload/download |
| 110619c | feat: SOP 13개, FAQ 12개, Dooly 키워드 11개 |
| 553004b | chore: gitignore 설정 |
| 59f234a | feat: simplified home UI, task 3-step status |
| e9c65c7 | fix: Dooly label, accordion UX |

---

## 9. 매일 사용 방법

### 9-1. 서버 시작

```
C:\Obsidian\Dooly\05_RAG\run_server.bat 더블클릭
```

실행 후 출력 확인:
```
Access URLs:
  PC browser  : http://localhost:8001/app
  Smartphone  : http://192.168.219.100:8001/app
  API status  : http://localhost:8001
```

### 9-2. PC 접속

브라우저에서: `http://localhost:8001/app`

또는 파일 직접 열기: `C:\Obsidian\Dooly\04_Runtime\index.html`

### 9-3. 스마트폰 접속

1. PC와 **같은 와이파이** 연결 확인
2. 스마트폰 브라우저에서: `http://192.168.219.100:8001/app`
3. PC IP가 바뀐 경우: cmd에서 `ipconfig` → IPv4 주소 확인 후 교체

### 9-4. 데이터 변경 시 재임베딩

1. `05_RAG\docs\` 폴더의 txt 파일 수정
2. `run_embed.bat` 더블클릭 (기존 DB 삭제 후 재생성)
3. `run_server.bat` 더블클릭

---

## 10. 다음 단계 (미완료)

### 10-1. Windows 작업 스케줄러 등록

서버 자동 시작 등록:
```
작업 스케줄러 → 새 작업 → 로그인 시 트리거
→ 동작: C:\Obsidian\Dooly\05_RAG\run_server.bat
```

### 10-2. PWA 전환

- Service Worker 등록
- manifest.json 작성
- 홈 화면 추가 지원
- IndexedDB로 데이터 마이그레이션 (localStorage 대체)
- File System Access API로 폴더 경로 선택 기능

### 10-3. 외부 접속 (ngrok)

```
ngrok http 8001
→ 외부에서 접속 가능한 HTTPS URL 제공
→ 원격 근무 시 유용
```

### 10-4. 답변 품질 개선

- 청크 분리 단위 최적화 (현재: `\n\n`)
- top-k 조정 (현재: 3)
- 시스템 프롬프트 개선
- 답변 길이 조절 파라미터 추가
- 대화 맥락(multi-turn) 유지

---

## 11. 트러블슈팅

### bat 파일 한글 깨짐 (작업지시서 27번)

**증상:** `run_embed.bat`, `run_server.bat` 실행 시 한글 echo 문자열이 깨지거나 명령어 오류 발생
**원인:** Windows cmd의 기본 인코딩(CP949)과 파일 저장 인코딩 충돌
**해결:** bat 파일의 모든 한글 echo를 영문으로 교체, `chcp 65001` 라인 제거

### 포트 8000 충돌 (작업지시서 28번)

**증상:** `run_server.bat` 실행 시 포트 이미 사용 중 오류
**원인:** 다른 앱(SMART)이 8000 포트 점유 중
**해결:** 모든 포트 참조를 8001로 변경 (`run_server.bat`, `README_RAG.txt`, `06_Dooly_v1.html`)

### FAQ 필터 미작동

**증상:** FAQ 카테고리 필터 클릭해도 필터링 안 됨
**원인:** localStorage에 구버전 데이터 잔존 (카테고리 필드 없음)
**해결:** 브라우저 개발자도구 → Application → localStorage → faq_data 삭제 후 새로고침

### Dooly 답변 부정확 / 오래된 내용

**증상:** 업데이트한 SOP/FAQ 내용이 답변에 반영 안 됨
**원인:** ChromaDB에 이전 임베딩 데이터가 남아있음
**해결:** `run_embed.bat` 재실행 (DB 완전 재생성)

### 스마트폰 접속 불가

**증상:** 스마트폰에서 서버 URL 접속 시 연결 안 됨
**원인 1:** PC와 다른 와이파이 연결
**원인 2:** Windows 방화벽이 8001 포트 차단
**해결:**
- 같은 와이파이 확인
- Windows Defender 방화벽 → 인바운드 규칙 → 포트 8001 허용 추가
- `ipconfig`로 현재 IP 재확인

---

## 12. 개발 워크플로우

### 12-1. Claude Code 작업지시서 규칙

파일 위치: `C:\Obsidian\Dooly\03_Claude_Code\`

명명 규칙:
```
{번호}_Order_{기능}_v{버전}.md
예: 29_Order_Dooly_ModelSource_v1.0.md
```

Claude Code 실행 방법:
```
{파일 전체 경로} 읽고 작업 시작해
예: C:\Obsidian\Dooly\03_Claude_Code\29_Order_Dooly_ModelSource_v1.0.md 읽고 작업 시작해
```

작업지시서 필수 포함 항목:
1. 작업 개요
2. 수정 대상 파일 경로
3. 기존 코드 → 변경 코드 (diff 형식)
4. 작업 완료 후 git 명령어

### 12-2. 세션 인수인계 방법

각 세션 종료 전 `00_System\02_SESSION_HANDOVER.md` 업데이트:
- 완료 작업 추가
- 다음 작업 업데이트
- 신규 파일/폴더 구조 반영

Claude Code 재시작 시 SESSION_HANDOVER.md를 먼저 읽어 컨텍스트 복원.

### 12-3. Git 커밋 규칙

```
feat:     새 기능 추가
fix:      버그 수정
docs:     문서 수정
refactor: 구조 개선
chore:    기타 (gitignore 등)
```

세션 종료 전 반드시 push:
```
git add .
git commit -m "feat: 작업 내용 요약"
git push
```
