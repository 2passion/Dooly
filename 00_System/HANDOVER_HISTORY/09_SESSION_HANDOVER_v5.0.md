# SESSION_HANDOVER.md v4.0

작성일: 2026-06-27
세션: 2026-06-26 ~ 2026-06-27
프로젝트 버전: King Assistant OS v1.0
아키텍처 버전: AI OS v1.0
현재 마일스톤: Phase 6 완료 → Phase 7 (PWA) 진행 예정

---

# 0. AI 인수인계 규칙

새 세션의 AI는 반드시 다음 순서로 시작한다.

1. 이 파일 (02_SESSION_HANDOVER.md) 읽기
2. 04_PROJECT_GUIDE_v1_0.md 읽기
3. 현재 마일스톤 파악
4. 작업지시서 번호 순서대로 작업 진행

이미 완료된 작업은 다시 구현하지 않는다.
작업지시서 번호는 반드시 순서를 유지한다. (현재 33번까지 완료)
다음 작업은 34번부터 시작한다.

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
- 사람이 이해하기 쉬운 구조 유지

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
Claude API + Supabase (클라우드 LLM + DB)
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
- 작업지시서 번호는 순서대로 증가
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

# 6. 완료 단계 현황

| Phase | 내용 | 상태 |
|-------|------|------|
| Phase 0 | 환경 준비 | ✅ |
| Phase 1 | HTML 프로토타입 (7개 파일) | ✅ |
| Phase 2 | 데이터 확장 (SOP/FAQ 22개) | ✅ |
| Phase 3 | UI 버그 수정 | ✅ |
| Phase 4 | RAG 서버 구축 | ✅ |
| Phase 5 | Dooly AI 고도화 | ✅ |
| Phase 6 | 자습실 PC 서버 구성 | ✅ |
| Phase 7 | PWA 전환 | 🔜 다음 작업 |

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
| Version Control | Git / GitHub (main 브랜치) |
| Remote | https://github.com/2passion/Dooly.git |

---

# 8. 폴더 구조

```
C:\Obsidian\Dooly\
├── 00_System\
│   ├── 01_PROJECT_MASTER.md
│   ├── 02_SESSION_HANDOVER.md  ← 이 파일 (항상 최신)
│   ├── 03_DEVELOPMENT_RULE_v1.0.md
│   ├── 04_PROJECT_GUIDE_v1.0.md
│   └── HANDOVER_HISTORY\       ← 이전 버전 보관
│       ├── 05_SESSION_HANDOVER_v1.md
│       ├── 06_SESSION_HANDOVER_v2.md
│       ├── 07_SESSION_HANDOVER_v3.md
│       └── 08_SESSION_HANDOVER_v4.md  ← 이번 세션 보관본
├── 01_Project\         ← 설계 문서
├── 02_Claude_Project\  ← Claude Project 지침
├── 03_Claude_Code\     ← 작업지시서 (33번까지 완료)
├── 04_Runtime\         ← HTML 파일
│   ├── index.html
│   ├── 02_Task_v1.html
│   ├── 03_SOP_v1.html
│   ├── 04_FAQ_v1.html
│   ├── 05_Notice_v1.html
│   ├── 06_Dooly_v1.html
│   └── 07_Settings_v1.html
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
| ngrok authtoken | 대시보드에서 확인 (문서에 직접 기재 금지) |

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

③ ngrok 실행 (작업 스케줄러로 자동 실행됨)
   수동: ngrok http --url=polymer-distinct-feminize.ngrok-free.dev 8001

④ localhost 테스트
   http://localhost:8001/app

⑤ 스마트폰 테스트
   https://polymer-distinct-feminize.ngrok-free.dev/app
```

※ 자습실 PC: 작업 스케줄러로 ②③ 자동 실행 등록 완료

---

# 12. 완료된 작업지시서 목록 (1~33번)

| 번호 | 내용 | 커밋 |
|------|------|------|
| 1~30 | HTML 프로토타입, SOP/FAQ, RAG 서버, AI 고도화 등 | 여러 커밋 |
| 31 | FastAPI static HTML serving (스마트폰 접속) | 4ab9bd9 |
| 32 | 탭 404 오류 수정 (리다이렉트 추가) | 355bc8e |
| 33 | Dooly 한국어 전용 답변 | a8257ab |

---

# 13. 다음 작업지시서 목록 (34번부터)

| 번호 | 작업 | 우선순위 |
|------|------|---------|
| 34 | PWA manifest.json 생성 + FastAPI 연동 + index.html 메타태그 | 높음 |
| 35 | PWA service-worker.js + 아이콘 파일 생성 | 높음 |
| 36 | 갤럭시 PWA 설치 테스트 및 수정 | 높음 |
| 37 | 아이폰 PWA 설치 테스트 및 수정 | 높음 |
| 38 | 인수인계 md 파일 업데이트 + GitHub push | 높음 |
| 39 | 보조 PC (데스크) 환경 구성 | 보통 |
| 40 | setup.bat 자동화 스크립트 | 보통 |
| 41 | SETUP_GUIDE.md 가이드북 작성 | 보통 |
| 42 | Cloudflare Tunnel 전환 (ngrok 대체) | 낮음 |
| 43 | Mock 모드 추가 | 낮음 |
| 44 | RAG 답변 품질 개선 | 낮음 |

---

# 14. 34번 작업지시서 상세 내용 (미실행, 다음 세션에서 진행)

## 34_Order_PWA_Manifest_v1.0

### 작업 개요
PWA 전환 1단계: manifest.json 생성 및 FastAPI 연동

### 수정 대상 파일
- 신규: C:\Obsidian\Dooly\04_Runtime\manifest.json
- 신규: C:\Obsidian\Dooly\04_Runtime\icons\ 폴더
- 수정: C:\Obsidian\Dooly\05_RAG\server.py
- 수정: C:\Obsidian\Dooly\04_Runtime\index.html

### 작업 내용 요약
1. manifest.json 생성
   - name: "KING Assistant OS"
   - short_name: "KING"
   - start_url: "/app"
   - display: "standalone"
   - background_color: "#0b0f1a"
   - theme_color: "#4da3ff"
   - icons: 192px, 512px

2. server.py에 라우트 추가
   - GET /manifest.json
   - GET /service-worker.js
   - GET /icons/{filename}

3. index.html <head>에 추가
   - <link rel="manifest" href="/manifest.json">
   - apple-mobile-web-app 메타태그

4. icons 폴더 생성 (아이콘은 35번에서 추가)

### git 명령어
git add .
git commit -m "feat: PWA manifest.json + FastAPI route + index.html meta tags"
git push

---

# 15. 사용자 기기 현황

| 기기 | 종류 | 상태 |
|------|------|------|
| 자습실 PC | Celeron G4900 데스크탑 | 메인 서버 ✅ |
| 데스크 PC | 데스크탑 | 보조 서버 (미구성) |
| 노트북(화이트) | 삼성 350XCJ i5-10210U | 개발용 ✅ |
| 노트북(블랙) | 노트북 | 사용자 기기 |
| S25 | 갤럭시 스마트폰 | 외부 접속 테스트 완료 ✅ |
| 조교A, B | 아이폰 | PWA 테스트 예정 |
| 조교C | 갤럭시폰 | 사용자 기기 |

---

# 16. 트러블슈팅 기록

| 문제 | 원인 | 해결 |
|------|------|------|
| 탭 클릭 404 | HTML 링크 경로 불일치 | server.py 리다이렉트 (32번) |
| Dooly 중국어 답변 | qwen 모델 습관 | 시스템 프롬프트 강제 (33번) |
| 포트 8000 충돌 | SMART 앱 점유 | 8001로 변경 |
| bat 파일 한글 깨짐 | CP949 인코딩 | 영문으로 교체 |
| ngrok 스케줄러 미작동 | 트리거 설정 오류 | 시스템 시작 시로 변경 |
| 카카오톡 대화기록 소실 | 인앱 브라우저 초기화 | Chrome 권장, PWA로 해결 예정 |
| ngrok authtoken 오류 | 잘못된 토큰 사용 | 대시보드에서 직접 복사 |

---

# 17. 서버 PC 업그레이드 계획

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

※ v2.0에서 Claude API 전환 시 서버 PC 불필요해질 수 있음

---

# 18. v2.0 Claude API 전환 검토 내용

| 항목 | 현재 (로컬 Ollama) | Claude API |
|------|-------------------|------------|
| 답변 속도 | 느림 (CPU) | 1~3초 |
| 월 비용 | 전기세 ~5,000원 | ~12,000원 |
| 서버 PC | 필요 | 불필요 |
| 인터넷 | ngrok만 | 항상 필요 |
| 구현 난이도 | 완료 | 쉬움 |

→ PWA 완성 후 v2.0에서 Claude API + Supabase 전환 예정

---

# 19. CHANGELOG

## 2026-06-27
- docs: SESSION_HANDOVER v4 작성

## 2026-06-26
- fix: 탭 클릭 404 오류 수정 (355bc8e)
- fix: Dooly 중국어 답변 제거 (a8257ab)
- feat: ngrok 고정 도메인 설정
- feat: 자습실 PC 환경 구성 완료
- feat: 작업 스케줄러 자동 시작 등록

## 이전 세션
- feat: FastAPI static HTML serving (4ab9bd9)
- feat: Dooly 대화 기록 유지 (54e2d19)
- feat: Dooly 모델 선택 + 출처 태그 (4dcf9dc)
- fix: 포트 8001 변경 (a1bf341)
- feat: 공지 탭 홈 통합 (95d6782)
- feat: RAG 서버 구축 (69e55dd)

---

# 20. 장기 문서 체계 (추후 분리 예정)

```
00_System\
├── 01_PROJECT_MASTER.md
├── 02_SESSION_HANDOVER.md   ← 항상 최신 버전
├── 03_DEVELOPMENT_RULE.md
├── 04_PROJECT_GUIDE.md
└── HANDOVER_HISTORY\        ← 버전별 보관
    ├── 05_SESSION_HANDOVER_v1.md
    ├── 06_SESSION_HANDOVER_v2.md
    ├── 07_SESSION_HANDOVER_v3.md
    └── 08_SESSION_HANDOVER_v4.md
```

추후 추가 예정:
- PROJECT_STATUS.md
- ARCHITECTURE.md
- SETUP_GUIDE.md
- CHANGELOG.md
- KNOWN_ISSUES.md
- AI_RULES.md
