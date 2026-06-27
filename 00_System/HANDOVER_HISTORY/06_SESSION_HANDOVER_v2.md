# SESSION_HANDOVER.md v2.0

작성일: 2026-06-26
세션: 2026-06-26 (오늘 세션)
프로젝트 버전: King Assistant OS v1.0
아키텍처 버전: AI OS v1.0
현재 마일스톤: Phase 6 완료 (자습실 PC 서버 구성 완료)

---

# 1. 현재 상태

## 완료 단계

| Phase | 내용 | 상태 |
|-------|------|------|
| Phase 0 | 환경 준비 | ✅ |
| Phase 1 | HTML 프로토타입 | ✅ |
| Phase 2 | 데이터 확장 (SOP/FAQ 22개) | ✅ |
| Phase 3 | UI 버그 수정 | ✅ |
| Phase 4 | RAG 서버 구축 | ✅ |
| Phase 5 | Dooly AI 고도화 | ✅ |
| Phase 6 | 자습실 PC 서버 구성 | ✅ |

---

# 2. 기술 스택

| 영역 | 기술 |
|------|------|
| Frontend | HTML5, Vanilla JS, localStorage |
| Backend | FastAPI (Python) |
| Database | ChromaDB (벡터DB) |
| Embedding | sentence-transformers (paraphrase-multilingual-MiniLM-L12-v2) |
| LLM | Ollama (qwen2.5:7b, qwen2.5:3b, gemma3:4b) |
| Tunnel | ngrok (고정 도메인) |
| Version Control | Git (main 브랜치) |
| Remote | https://github.com/2passion/Dooly.git |

---

# 3. 폴더 구조

```
C:\Obsidian\Dooly\
├── 00_System\          ← 시스템 문서 (마스터, 인수인계, 가이드)
├── 01_Project\         ← 설계 문서
├── 02_Claude_Project\  ← Claude Project 지침
├── 03_Claude_Code\     ← 작업지시서 (33번까지 완료)
├── 04_Runtime\         ← HTML 실행 파일 7개
│   ├── index.html
│   ├── 02_Task_v1.html
│   ├── 03_SOP_v1.html
│   ├── 04_FAQ_v1.html
│   ├── 05_Notice_v1.html (리다이렉트)
│   ├── 06_Dooly_v1.html
│   └── 07_Settings_v1.html
├── 05_RAG\             ← RAG 서버
│   ├── server.py
│   ├── embed.py
│   ├── run_server.bat
│   ├── run_embed.bat
│   ├── docs\
│   │   ├── sop_data.txt
│   │   └── faq_data.txt
│   └── db\             ← ChromaDB (git 제외)
└── 99_Archive\         ← 아카이브 (git 제외)
```

---

# 4. 환경 변수 및 주요 설정

| 항목 | 값 |
|------|-----|
| 서버 포트 | 8001 (8000 충돌로 변경) |
| LLM 기본 모델 | qwen2.5:7b |
| 임베딩 모델 | paraphrase-multilingual-MiniLM-L12-v2 |
| ChromaDB 경로 | C:\Obsidian\Dooly\05_RAG\db |
| ngrok 고정 도메인 | polymer-distinct-feminize.ngrok-free.dev |
| ngrok authtoken | 대시보드에서 확인 (https://dashboard.ngrok.com) |

---

# 5. 접속 URL

| 환경 | URL |
|------|-----|
| PC 로컬 | http://localhost:8001/app |
| 내부 와이파이 | http://192.168.219.100:8001/app |
| 외부 (ngrok) | https://polymer-distinct-feminize.ngrok-free.dev/app |

---

# 6. 서버 실행 순서

```
① git pull (코드 최신화)
   cd C:\Obsidian\Dooly
   git pull

② run_server.bat 실행
   C:\Obsidian\Dooly\05_RAG\run_server.bat 더블클릭

③ ngrok 실행
   ngrok http --url=polymer-distinct-feminize.ngrok-free.dev 8001

④ localhost 테스트
   브라우저: http://localhost:8001/app

⑤ 스마트폰 테스트
   https://polymer-distinct-feminize.ngrok-free.dev/app
```

※ 작업 스케줄러 등록 완료로 자습실 PC 시작 시 ②③ 자동 실행

---

# 7. 오늘 완료 작업

### 32번 — 탭 404 오류 수정 (커밋: 355bc8e)
- server.py에 리다이렉트 라우트 추가
- /{filename}.html → /app/{filename}.html

### 33번 — 한국어 전용 답변 (커밋: a8257ab)
- server.py 시스템 프롬프트에 한국어 강제 지시 추가
- qwen 모델 중국어 출력 문제 해결

### 자습실 PC 환경 구성
- Python 3.14.6, Git 2.54.0, Ollama 0.30.10 설치
- qwen2.5:7b, qwen2.5:3b, gemma3:4b 모델 설치
- pip 패키지 설치, git clone, run_embed.bat 실행
- ngrok 설치 및 설정

### 작업 스케줄러 등록
- Dooly RAG Server: 시스템 시작 시 자동 실행
- Dooly ngrok: 시스템 시작 시 자동 실행

---

# 8. 다음 작업 (작업지시서 34번부터)

| 번호 | 작업 | 우선순위 |
|------|------|---------|
| 34 | PWA manifest.json 생성 | 높음 |
| 35 | service-worker.js 생성 (오프라인 캐시) | 높음 |
| 36 | 홈 화면 아이콘 설정 | 높음 |
| 37 | 갤럭시 PWA 설치 테스트 | 높음 |
| 38 | 아이폰 PWA 설치 테스트 | 높음 |
| 39 | 보조 PC (데스크) 환경 구성 | 보통 |
| 40 | setup.bat 자동화 스크립트 | 보통 |
| 41 | SETUP_GUIDE.md 가이드북 작성 | 보통 |
| 42 | Cloudflare Tunnel 전환 (ngrok 대체) | 낮음 |
| 43 | Mock 모드 추가 (서버 없이 키워드 답변) | 낮음 |
| 44 | RAG 답변 품질 개선 (multi-turn) | 낮음 |

---

# 9. 사용자 기기 현황

| 기기 | 종류 | 상태 |
|------|------|------|
| 자습실 PC | 데스크탑 (Celeron G4900) | 메인 서버 ✅ |
| 데스크 PC | 데스크탑 | 보조 서버 (미구성) |
| 노트북(화이트) | 삼성 350XCJ (i5-10210U) | 개발용 ✅ |
| 노트북(블랙) | 노트북 | 사용자 기기 |
| S25 | 갤럭시 스마트폰 | 테스트 완료 ✅ |
| 조교A, B | 아이폰 | PWA 테스트 예정 |
| 조교C | 갤럭시폰 | 사용자 기기 |

---

# 10. 트러블슈팅 기록

| 문제 | 원인 | 해결 |
|------|------|------|
| 탭 클릭 404 오류 | HTML 링크가 /파일명 형태 | server.py 리다이렉트 추가 (32번) |
| Dooly 중국어 답변 | qwen 모델 습관 | 시스템 프롬프트 한국어 강제 (33번) |
| 포트 8000 충돌 | SMART 앱 점유 | 8001로 변경 |
| bat 파일 한글 깨짐 | CP949 인코딩 충돌 | 영문으로 교체 |
| ngrok 작업스케줄러 미작동 | 트리거가 로그온할 때 | 시스템 시작 시로 변경 |
| ngrok authtoken 오류 | 잘못된 토큰 사용 | 대시보드에서 직접 복사 |
| 카카오톡 대화기록 사라짐 | 인앱 브라우저 localStorage 초기화 | Chrome으로 열기 권장, PWA로 해결 예정 |

---

# 11. 서버 PC 업그레이드 계획

현재 자습실 PC (Celeron G4900, GPU 없음) → AI 답변 매우 느림

**추천 구성 (150만원)**

| 부품 | 모델 | 가격 |
|------|------|------|
| CPU | i5-13400F | 약 18만원 |
| 메인보드 | B760M | 약 12만원 |
| RAM | DDR4 32GB | 약 8만원 |
| SSD | NVMe 1TB | 약 10만원 |
| GPU | RTX 4070 Ti 12GB | 약 85만원 |
| 파워 | 750W 80+ Gold | 약 9만원 |
| 케이스 | 미들타워 | 약 5만원 |
| 합계 | | 약 147만원 |

---

# 12. CHANGELOG

## 2026-06-26
- fix: 탭 클릭 404 오류 수정 (리다이렉트 추가)
- fix: Dooly 중국어 답변 제거 (한국어 전용)
- feat: ngrok 고정 도메인 설정
- feat: 자습실 PC 서버 환경 구성 완료
- feat: 작업 스케줄러 자동 시작 등록

## 이전 세션 주요 이력
- feat: FastAPI static HTML serving (4ab9bd9)
- feat: Dooly 대화 기록 localStorage 유지 (54e2d19)
- feat: Dooly 모델 선택 + 출처 태그 (4dcf9dc)
- fix: 포트 8000 → 8001 변경 (a1bf341)
- feat: 공지 탭 홈으로 통합 (95d6782)
- feat: RAG 서버 구축 (69e55dd)

---

# 13. 새 세션 시작 방법

1. 이 파일 첨부
2. 04_PROJECT_GUIDE_v1_0.md 첨부
3. 아래 메시지로 시작:

```
첨부한 두 파일을 읽고 프로젝트 현황을 파악해줘.
다음 작업은 PWA 전환 (34번)부터 진행할거야.
```

---

# 14. 장기 문서 계획 (추후 분리 예정)

| 파일 | 내용 |
|------|------|
| PROJECT_STATUS.md | 현재 진행 상황 및 로드맵 |
| ARCHITECTURE.md | 시스템 구조와 데이터 흐름 |
| SETUP_GUIDE.md | 새 PC 설치 절차 + 체크리스트 |
| CHANGELOG.md | 버전별 변경 사항 |
| KNOWN_ISSUES.md | 알려진 문제와 해결 방법 |

