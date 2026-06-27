# SESSION_HANDOVER.md

작성일: 2026-06-26

---

# 현재 상태

King Assistant OS v1.0
AI 비서: 둘리(Dooly)
현재 단계: Phase 6 완료 (자습실 PC 서버 구성 완료)

---

# 완료 작업 전체 목록

## Phase 0~5 (이전 세션 완료)
- HTML 프로토타입 7개 파일 생성
- SOP 22개, FAQ 22개, Dooly 키워드 23개
- RAG 서버 구축 (FastAPI + ChromaDB + Ollama)
- Dooly 모델 선택, 출처 태그, 대화 기록 유지
- 스마트폰 접속 구현

## 오늘 세션 완료 작업

### 32번 작업지시서 — 탭 404 오류 수정
- server.py에 리다이렉트 라우트 추가
- /{filename}.html → /app/{filename}.html 자동 리다이렉트
- 커밋: 355bc8e

### 33번 작업지시서 — 한국어 전용 답변
- server.py 시스템 프롬프트에 한국어 전용 지시 추가
- qwen 모델 중국어 답변 문제 해결
- 커밋: a8257ab

### ngrok 고정 도메인 설정
- ngrok 설치 (Microsoft Store)
- 계정 가입 (2davidpassion@gmail.com)
- 고정 도메인 확보: polymer-distinct-feminize.ngrok-free.dev
- 외부 접속 URL: https://polymer-distinct-feminize.ngrok-free.dev/app
- 실행 명령어: ngrok http --url=polymer-distinct-feminize.ngrok-free.dev 8001

### 자습실 PC 환경 구성 완료
- Python 3.14.6 설치
- Git 2.54.0 설치
- Ollama 0.30.10 설치
- qwen2.5:7b, qwen2.5:3b, gemma3:4b 모델 설치
- pip 패키지 설치 (fastapi, uvicorn, chromadb, sentence-transformers, ollama, PyPDF2)
- git clone 완료 (C:\Obsidian\Dooly)
- run_embed.bat 실행 완료 (44개 청크 임베딩)
- ngrok 설치 및 authtoken 등록

### 작업 스케줄러 등록
- Dooly RAG Server: 시스템 시작 시 자동 실행
- Dooly ngrok: 시스템 시작 시 자동 실행
- 두 작업 모두 트리거: 시작할 때 (시스템 시작 시)

---

# 현재 시스템 구성

## 자습실 PC (메인 서버)
- CPU: Intel Celeron G4900 (저사양, GPU 없음)
- 메인보드: ASUS PRIME H310M-K R2.0
- OS: Windows 10 Pro
- 역할: RAG 서버 + ngrok 터널

## 노트북(화이트)
- 제조사: 삼성 (350XCJ/350XCR)
- CPU: i5-10210U
- 역할: 개발 및 작업 (Claude Code 사용)

## 접속 URL
- 내부 (같은 와이파이): http://192.168.219.100:8001/app
- 외부 (ngrok 고정): https://polymer-distinct-feminize.ngrok-free.dev/app
- PC 로컬: http://localhost:8001/app

## ngrok 계정 정보
- 이메일: 2davidpassion@gmail.com
- 고정 도메인: polymer-distinct-feminize.ngrok-free.dev
- authtoken: 대시보드에서 확인 (https://dashboard.ngrok.com/get-started/your-authtoken)

---

# 매일 사용 방법

## 서버 자동 시작 (작업 스케줄러 등록됨)
- 자습실 PC 켜면 자동으로 run_server.bat + ngrok 실행
- 별도 조작 불필요

## 수동 실행이 필요한 경우
1. run_server.bat 더블클릭 (C:\Obsidian\Dooly\05_RAG\)
2. cmd에서: ngrok http --url=polymer-distinct-feminize.ngrok-free.dev 8001

---

# 파일 구조

```
C:\Obsidian\Dooly\
├── 00_System\          ← 시스템 문서
├── 01_Project\         ← 설계 문서
├── 02_Claude_Project\  ← Claude Project 지침
├── 03_Claude_Code\     ← 작업지시서 (32번, 33번까지 완료)
├── 04_Runtime\         ← HTML 파일 7개
├── 05_RAG\             ← RAG 서버
└── 99_Archive\
```

## 04_Runtime HTML 파일
| 파일 | 탭 | 기능 |
|------|-----|------|
| index.html | 홈 | 달력, 공지사항 |
| 02_Task_v1.html | 업무 | 업무 CRUD, 상태 필터 |
| 03_SOP_v1.html | SOP | 22개 SOP, 검색 |
| 04_FAQ_v1.html | FAQ | 22개 FAQ, 검색 |
| 05_Notice_v1.html | (없음) | index.html 리다이렉트 |
| 06_Dooly_v1.html | Dooly | RAG AI 채팅 |
| 07_Settings_v1.html | 설정 | 담당자 관리 |

## 05_RAG 파일
| 파일 | 역할 |
|------|------|
| server.py | FastAPI 서버 (포트 8001) |
| embed.py | 문서 임베딩 |
| run_server.bat | 서버 실행 |
| run_embed.bat | 임베딩 실행 |
| docs/sop_data.txt | SOP 22개 |
| docs/faq_data.txt | FAQ 22개 |

---

# Git 커밋 히스토리 (최신순)

| 커밋 | 내용 |
|------|------|
| a8257ab | fix: enforce Korean-only response in Dooly system prompt |
| 355bc8e | fix: redirect /{filename}.html to /app/{filename}.html |
| 4ab9bd9 | feat: FastAPI static HTML serving for mobile access |
| 54e2d19 | feat: Dooly chat history persist in localStorage |
| 4dcf9dc | feat: Dooly model A/B/C selector + source tag display |

GitHub: https://github.com/2passion/Dooly.git

---

# 다음 작업 (미완료)

## 우선순위 높음
1. **PWA 전환** (manifest.json + Service Worker)
   - 홈 화면 아이콘 설치 지원
   - 갤럭시, 아이폰 테스트 필요
   - 아이폰 조교 출근 시 직접 테스트 예정

2. **보조 PC (데스크 PC) 환경 구성**
   - 자습실 PC와 동일하게 구성
   - setup.bat 자동화 스크립트 작성 예정

## 우선순위 보통
3. **가이드북 작성** (setup 가이드 md 파일)
   - 새 PC 설치 체크리스트 포함
   - Obsidian 저장 + GitHub push

4. **서버 PC 업그레이드 계획**
   - 예산: 150만원
   - 추천 구성: i5-13400F + RTX 4070 Ti + 32GB RAM + 1TB SSD
   - 현재 자습실 PC (Celeron G4900)는 저사양으로 답변 느림

5. **Cloudflare Tunnel 전환** (ngrok 대체)
   - 완전 무료 + 고정 URL
   - PWA 검증 후 진행 예정

## 낮은 우선순위
6. Mock 모드 추가 (서버 없이 키워드 답변)
7. RAG 답변 품질 개선 (multi-turn, 청크 최적화)
8. 고정 IP 설정 (방식 2)

---

# 사용자 기기 현황

| 기기 | 종류 | 역할 |
|------|------|------|
| 자습실 PC | 데스크탑 | 메인 서버 |
| 데스크 PC | 데스크탑 | 보조 서버 (미구성) |
| 노트북(화이트) | 삼성 노트북 | 개발용 |
| 노트북(블랙) | 노트북 | 사용자 기기 |
| S25 | 갤럭시 스마트폰 | 테스트 완료 |
| 조교A, B | 아이폰 | PWA 테스트 예정 |
| 조교C | 갤럭시폰 | 사용자 기기 |

---

# 트러블슈팅 기록 (오늘)

## 탭 클릭 시 404 오류
- 원인: HTML 탭 링크가 /02_Task_v1.html 형태
- 해결: server.py에 리다이렉트 라우트 추가 (32번)

## Dooly 중국어 답변
- 원인: qwen2.5 모델이 답변 끝에 중국어 추가
- 해결: 시스템 프롬프트에 한국어 전용 지시 추가 (33번)

## ngrok 작업 스케줄러 미작동
- 원인: 트리거가 로그온할 때로 설정됨
- 해결: 트리거를 시작할 때 (시스템 시작 시)로 변경

## ngrok authtoken 오류
- 원인: 대화에서 잘못된 토큰 사용
- 해결: dashboard.ngrok.com에서 직접 복사

---

# 새 세션 시작 방법

1. 이 파일 (02_SESSION_HANDOVER.md) 읽기
2. 04_PROJECT_GUIDE_v1_0.md 읽기
3. 다음 작업 확인 후 진행
4. Claude Code 작업지시서는 03_Claude_Code 폴더에 34번부터 시작

