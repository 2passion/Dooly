# SESSION_HANDOVER.md v3.0

작성일: 2026-06-26
세션: 2026-06-26
프로젝트 버전: King Assistant OS v1.0
아키텍처 버전: AI OS v1.0
현재 마일스톤: Phase 6 완료 (자습실 PC 서버 구성 완료)

---

# 0. AI 인수인계 규칙

새 세션의 AI는 반드시 다음 순서로 시작한다.

1. SESSION_HANDOVER.md 읽기
2. 04_PROJECT_GUIDE_v1_0.md 읽기
3. 현재 마일스톤 파악
4. 작업지시서 번호 순서대로 작업 진행

이미 완료된 작업은 다시 구현하지 않는다.
작업지시서 번호는 반드시 순서를 유지한다.

---

# 1. 프로젝트 철학

King Assistant OS는 킹수학 학원 조교 운영을 위한 AI 비서 시스템이다.
학원 전체 운영 시스템이 아닌, 조교 업무 표준화와 효율화가 목표다.

## 핵심 원칙

- HTML 우선: 별도 프레임워크 없이 HTML + Vanilla JS로 구현
- 로컬 우선(Local First): 서버 없이도 기본 기능 동작 (localStorage)
- AI 중심 설계: Dooly(둘리)를 중심으로 업무 지원
- 모듈 독립성: 각 HTML 파일은 독립적으로 동작
- Git 기반 버전 관리: 모든 변경사항 커밋 후 push
- 사람이 이해하기 쉬운 구조 유지: 조교도 직접 파일을 수정할 수 있는 수준

## AI 비서 Dooly 정의

| 항목 | 내용 |
|------|------|
| 이름 | 둘리 (Dooly) |
| 역할 | 학원 업무 AI 비서 |
| 기능 | SOP 검색, FAQ 검색, RAG 답변, 업무 안내 |
| 모델 | qwen2.5:7b (기본), qwen2.5:3b, gemma3:4b |
| 향후 | AI OS의 메인 Assistant로 확장 예정 |

---

# 2. 버전 로드맵

```
v1.0 (현재)
HTML 기반 + RAG 서버 + ngrok
↓
v1.5
PWA 전환 (홈 화면 설치, 오프라인 지원)
↓
v2.0
Supabase 연동 (클라우드 DB, 실시간 동기화)
↓
v3.0
AI OS 통합 (멀티 AI, 자동화, 확장)
```

---

# 3. 데이터 흐름

```
[사용자 기기]
스마트폰 / 노트북 / PC
브라우저에서 URL 접속
        │
        ▼
[ngrok 터널]
polymer-distinct-feminize.ngrok-free.dev
HTTPS → localhost:8001
        │
        ▼
[FastAPI server.py]
POST /chat (질문 수신)
GET /app (HTML 서빙)
        │
        ├─────────────────┐
        ▼                 ▼
[ChromaDB]          [Ollama]
벡터 검색           qwen2.5:7b
top-3 문서 반환     LLM 답변 생성
        │                 │
        └────────┬────────┘
                 ▼
        [JSON 응답 반환]
        {answer, sources}
                 │
                 ▼
        [브라우저 화면 표시]
        답변 + 출처 태그
```

---

# 4. 의존성 관계

```
04_Runtime (HTML)
    │ fetch() API 호출
    ▼
05_RAG/server.py (FastAPI)
    ├── embed.py (임베딩 전처리)
    ├── docs/ (SOP/FAQ 텍스트)
    ├── db/ (ChromaDB 벡터)
    └── Ollama (LLM 실행)
           └── qwen2.5:7b / 3b, gemma3:4b
```

---

# 5. 개발 규칙

## 반드시 지킬 규칙

- HTML 파일명 변경 금지 (탭 링크와 연동됨)
- API 경로 변경 시 리다이렉트 반드시 유지
- ChromaDB db/ 폴더는 git 제외 (.gitignore)
- 모든 작업 완료 후 반드시 git commit + push
- 작업지시서 번호는 순서대로 증가 (현재 33번까지 완료)
- 포트는 반드시 8001 유지 (8000은 SMART 앱 충돌)

## 절대 변경 금지 항목

| 항목 | 이유 |
|------|------|
| 폴더 구조 (00~05) | 전체 시스템 참조 기준 |
| 작업지시서 번호 순서 | 이력 추적 기준 |
| /app 경로 | HTML 서빙 기준 경로 |
| 포트 8001 | 8000 충돌로 변경된 값 |
| Dooly 이름 | 시스템 전체 브랜딩 |
| ngrok 고정 도메인 | PWA URL 기준 |

---

# 6. 현재 시스템 구성

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

# 7. 기술 스택

| 영역 | 기술 |
|------|------|
| Frontend | HTML5, Vanilla JS, localStorage |
| Backend | FastAPI (Python) |
| Database | ChromaDB (벡터DB) |
| Embedding | paraphrase-multilingual-MiniLM-L12-v2 |
| LLM | Ollama (qwen2.5:7b, qwen2.5:3b, gemma3:4b) |
| Tunnel | ngrok (고정 도메인) |
| Version Control | Git (main 브랜치) |
| Remote | https://github.com/2passion/Dooly.git |

---

# 8. 폴더 구조

```
C:\Obsidian\Dooly\
├── 00_System\          ← 시스템 문서
├── 01_Project\         ← 설계 문서
├── 02_Claude_Project\  ← Claude Project 지침
├── 03_Claude_Code\     ← 작업지시서 (33번까지 완료)
├── 04_Runtime\         ← HTML 파일 7개
│   ├── index.html          (홈 + 달력 + 공지)
│   ├── 02_Task_v1.html     (업무 관리)
│   ├── 03_SOP_v1.html      (SOP 검색)
│   ├── 04_FAQ_v1.html      (FAQ 검색)
│   ├── 05_Notice_v1.html   (리다이렉트)
│   ├── 06_Dooly_v1.html    (AI 채팅)
│   └── 07_Settings_v1.html (설정)
├── 05_RAG\             ← RAG 서버
│   ├── server.py
│   ├── embed.py
│   ├── run_server.bat
│   ├── run_embed.bat
│   ├── docs/sop_data.txt
│   ├── docs/faq_data.txt
│   └── db/             (git 제외)
└── 99_Archive\         (git 제외)
```

---

# 9. 환경 설정

| 항목 | 값 |
|------|-----|
| 서버 포트 | 8001 |
| 기본 LLM 모델 | qwen2.5:7b |
| 임베딩 모델 | paraphrase-multilingual-MiniLM-L12-v2 |
| ChromaDB 경로 | C:\Obsidian\Dooly\05_RAG\db |
| ngrok 고정 도메인 | polymer-distinct-feminize.ngrok-free.dev |
| ngrok authtoken | 대시보드에서 확인 (절대 문서에 직접 기재 금지) |

---

# 10. 접속 URL

| 환경 | URL |
|------|-----|
| PC 로컬 | http://localhost:8001/app |
| 내부 와이파이 | http://192.168.219.100:8001/app |
| 외부 (ngrok) | https://polymer-distinct-feminize.ngrok-free.dev/app |

---

# 11. 서버 실행 순서

```
① git pull
   cd C:\Obsidian\Dooly && git pull

② run_server.bat 실행
   C:\Obsidian\Dooly\05_RAG\run_server.bat 더블클릭

③ ngrok 실행
   ngrok http --url=polymer-distinct-feminize.ngrok-free.dev 8001

④ localhost 테스트
   http://localhost:8001/app

⑤ 스마트폰 테스트
   https://polymer-distinct-feminize.ngrok-free.dev/app
```

※ 작업 스케줄러 등록 완료 → 자습실 PC 시작 시 ②③ 자동 실행

---

# 12. 오늘 완료 작업

| 번호 | 내용 | 커밋 |
|------|------|------|
| 32 | 탭 404 오류 수정 (리다이렉트 추가) | 355bc8e |
| 33 | Dooly 한국어 전용 답변 | a8257ab |
| - | ngrok 고정 도메인 설정 | - |
| - | 자습실 PC 환경 구성 완료 | - |
| - | 작업 스케줄러 자동 시작 등록 | - |

---

# 13. 다음 작업 (34번부터)

| 번호 | 작업 | 우선순위 |
|------|------|---------|
| 34 | PWA manifest.json 생성 | 높음 |
| 35 | service-worker.js (오프라인 캐시) | 높음 |
| 36 | 홈 화면 아이콘 설정 | 높음 |
| 37 | 갤럭시 PWA 설치 테스트 | 높음 |
| 38 | 아이폰 PWA 설치 테스트 | 높음 |
| 39 | 보조 PC 환경 구성 | 보통 |
| 40 | setup.bat 자동화 스크립트 | 보통 |
| 41 | SETUP_GUIDE.md 가이드북 작성 | 보통 |
| 42 | Cloudflare Tunnel 전환 | 낮음 |
| 43 | Mock 모드 추가 | 낮음 |
| 44 | RAG 답변 품질 개선 | 낮음 |

---

# 14. 사용자 기기 현황

| 기기 | 종류 | 상태 |
|------|------|------|
| 자습실 PC | Celeron G4900 데스크탑 | 메인 서버 ✅ |
| 데스크 PC | 데스크탑 | 보조 서버 (미구성) |
| 노트북(화이트) | 삼성 350XCJ i5-10210U | 개발용 ✅ |
| 노트북(블랙) | 노트북 | 사용자 기기 |
| S25 | 갤럭시 | 외부 접속 테스트 완료 ✅ |
| 조교A, B | 아이폰 | PWA 테스트 예정 |
| 조교C | 갤럭시폰 | 사용자 기기 |

---

# 15. 트러블슈팅 기록

| 문제 | 원인 | 해결 |
|------|------|------|
| 탭 클릭 404 | HTML 링크 경로 불일치 | server.py 리다이렉트 (32번) |
| Dooly 중국어 답변 | qwen 모델 습관 | 시스템 프롬프트 강제 (33번) |
| 포트 8000 충돌 | SMART 앱 점유 | 8001로 변경 |
| bat 파일 한글 깨짐 | CP949 인코딩 | 영문으로 교체 |
| ngrok 스케줄러 미작동 | 트리거 설정 오류 | 시스템 시작 시로 변경 |
| 카카오톡 대화기록 소실 | 인앱 브라우저 초기화 | Chrome 열기 권장, PWA로 해결 예정 |

---

# 16. 서버 PC 업그레이드 계획

현재 자습실 PC (Celeron G4900, GPU 없음) → 답변 매우 느림

**추천 구성 150만원**

| 부품 | 모델 | 가격 |
|------|------|------|
| CPU | i5-13400F | 약 18만원 |
| 메인보드 | B760M | 약 12만원 |
| RAM | DDR4 32GB | 약 8만원 |
| SSD | NVMe 1TB | 약 10만원 |
| GPU | RTX 4070 Ti 12GB | 약 85만원 |
| 파워 | 750W 80+ Gold | 약 9만원 |
| 케이스 | 미들타워 | 약 5만원 |

---

# 17. CHANGELOG

## 2026-06-26
- fix: 탭 클릭 404 오류 수정
- fix: Dooly 중국어 답변 제거
- feat: ngrok 고정 도메인 설정
- feat: 자습실 PC 서버 환경 구성
- feat: 작업 스케줄러 자동 시작 등록

## 이전 세션
- feat: FastAPI static HTML serving (4ab9bd9)
- feat: Dooly 대화 기록 유지 (54e2d19)
- feat: Dooly 모델 선택 + 출처 태그 (4dcf9dc)
- fix: 포트 8001 변경 (a1bf341)
- feat: 공지 탭 홈 통합 (95d6782)
- feat: RAG 서버 구축 (69e55dd)

---

# 18. 장기 문서 체계 (추후 분리 예정)

```
00_System\
├── MASTER_GUIDE.md       ← 최상위 문서
├── SESSION_HANDOVER.md   ← 세션 인수인계 (현재 이 파일)
├── PROJECT_STATUS.md     ← 현재 진행률
├── ARCHITECTURE.md       ← 시스템 구조
├── CHANGELOG.md          ← 변경 이력
├── SETUP_GUIDE.md        ← 새 PC 설치 가이드
├── KNOWN_ISSUES.md       ← 알려진 문제
└── AI_RULES.md           ← AI 개발 규칙
```

