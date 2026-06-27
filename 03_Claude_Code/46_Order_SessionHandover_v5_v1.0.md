# 46_Order_SessionHandover_v5_v1.0.md
# King Assistant OS v1.0
# Claude Code 작업지시서

Version: v1.0
Date: 2026-06-28

---

# 작업 목표

SESSION_HANDOVER v5.0 저장 및 업데이트

---

# STEP 1 — 현재 인수인계 파일을 히스토리로 복사

```
Copy-Item "C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md" "C:\Obsidian\Dooly\00_System\HANDOVER_HISTORY\09_SESSION_HANDOVER_v5.0.md"
```

기존 02_SESSION_HANDOVER.md 는 수정하지 않는다.

---

# STEP 2 — 02_SESSION_HANDOVER.md 최신 내용으로 덮어쓰기

아래 내용으로 C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md 를 덮어써줘.

---

# SESSION_HANDOVER.md v5.0

작성일: 2026-06-28
세션: 2026-06-27 ~ 2026-06-28
프로젝트 버전: King Assistant OS v1.0
현재 마일스톤: Phase 7 완료 (PWA + GitHub Pages 배포)

---

# 0. AI 인수인계 규칙

새 세션의 AI는 반드시 다음 순서로 시작한다.

1. 이 파일 (02_SESSION_HANDOVER.md) 읽기
2. 04_PROJECT_GUIDE_v1.0.md 읽기
3. 05_WORKFLOW_GUIDE_v1.0.md 읽기
4. 현재 마일스톤 파악
5. 작업지시서 번호 순서대로 작업 진행

이미 완료된 작업은 다시 구현하지 않는다.
작업지시서 번호는 반드시 순서를 유지한다. (현재 45번까지 완료)
다음 작업은 46번부터 시작한다.

---

# 1. 프로젝트 철학

King Assistant OS는 킹수학 학원 조교 운영을 위한 AI 비서 시스템이다.
학원 전체 운영 시스템이 아닌, 조교 업무 표준화와 효율화가 목표다.

## 핵심 원칙

- HTML 우선: 별도 프레임워크 없이 HTML + Vanilla JS로 구현
- 로컬 우선(Local First): 서버 없이도 기본 기능 동작 (localStorage)
- AI 중심 설계: Dooly(둘리)를 중심으로 업무 지원
- Mock 우선: data.js 기반 오프라인 답변이 기본
- Git 기반 버전 관리: 모든 변경사항 커밋 후 push

## AI 비서 Dooly 정의

| 항목 | 내용 |
|------|------|
| 이름 | 둘리 (Dooly) |
| 역할 | 학원 업무 AI 비서 |
| 기능 | SOP 검색, FAQ 검색, Mock 답변, 아코디언 목록 |
| 기본 모드 | Mock — 오프라인 모드 |
| 선택 모드 | 모델 A/B/C (Ollama, 서버 필요) |
| 향후 | Claude API 전환 예정 |

---

# 2. 버전 로드맵

```
v1.0 (현재 완료)
HTML + data.js + Mock 모드
GitHub Pages 배포 + PWA 설치
↓
v1.5 (다음)
아이폰 PWA 테스트 완료
Task 동기화 (FastAPI Task API)
↓
v2.0
Claude API 전환 (자연스러운 AI 답변)
Supabase (클라우드 DB, 실시간 동기화)
↓
v3.0
AI OS 통합 (멀티 AI, 자동화, 확장)
```

---

# 3. 현재 시스템 구조

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
        │   → 인터넷 불필요 (PWA 캐시)
        │
        └── 모델 A/B/C (선택)
            → 자습실 PC 서버 필요
            → Ollama RAG 답변
```

---

# 4. 접속 정보

| 환경 | URL |
|------|-----|
| GitHub Pages (메인) | https://2passion.github.io/Dooly/ |
| 기존 ngrok (보조) | https://polymer-distinct-feminize.ngrok-free.dev/app |
| PC 로컬 | http://localhost:8001/app |

---

# 5. 완료 단계 현황

| Phase | 내용 | 상태 |
|-------|------|------|
| Phase 0 | 환경 준비 | ✅ |
| Phase 1 | HTML 프로토타입 (7개 파일) | ✅ |
| Phase 2 | 데이터 확장 (SOP/FAQ 22개) | ✅ |
| Phase 3 | UI 버그 수정 | ✅ |
| Phase 4 | RAG 서버 구축 | ✅ |
| Phase 5 | Dooly AI 고도화 | ✅ |
| Phase 6 | 자습실 PC 서버 구성 | ✅ |
| Phase 7 | PWA + GitHub Pages 배포 | ✅ |
| Phase 8 | 아이폰 PWA 테스트 | 🔜 다음 |

---

# 6. 기술 스택

| 영역 | 기술 |
|------|------|
| Frontend | HTML5, Vanilla JS, localStorage |
| 데이터 | data.js (SOP 23개 + FAQ 22개) |
| 배포 | GitHub Pages (무료, 24시간) |
| PWA | manifest.json + service-worker.js |
| 백업 서버 | FastAPI + ChromaDB + Ollama (자습실 PC) |
| Version Control | Git / GitHub (main 브랜치) |
| Remote | https://github.com/2passion/Dooly.git |

---

# 7. 폴더 구조

```
C:\Obsidian\Dooly\
├── 00_System\
│   ├── 01_PROJECT_MASTER.md
│   ├── 02_SESSION_HANDOVER.md  ← 이 파일 (항상 최신)
│   ├── 03_DEVELOPMENT_RULE_v1.0.md
│   ├── 04_PROJECT_GUIDE_v1.0.md
│   ├── 05_WORKFLOW_GUIDE_v1.0.md
│   └── HANDOVER_HISTORY\
│       ├── 02_SESSION_HANDOVER.md
│       ├── 05_SESSION_HANDOVER_v1.md
│       ├── 06_SESSION_HANDOVER_v2.md
│       ├── 07_SESSION_HANDOVER_v3.md
│       ├── 08_SESSION_HANDOVER_v4.0.md
│       └── 09_SESSION_HANDOVER_v5.0.md
├── 01_Project\
├── 02_Claude_Project\
├── 03_Claude_Code\     ← 작업지시서 (45번까지 완료)
├── 04_Runtime\         ← HTML 파일 (로컬 서버용)
│   ├── index.html
│   ├── 02_Task_v1.html
│   ├── 03_SOP_v1.html
│   ├── 04_FAQ_v1.html
│   ├── 05_Notice_v1.html
│   ├── 06_Dooly_v1.html
│   ├── 07_Settings_v1.html
│   ├── data.js
│   ├── manifest.json
│   ├── service-worker.js
│   └── icons\
│       ├── icon-192.png
│       └── icon-512.png
├── 05_RAG\             ← RAG 서버 (자습실 PC용)
├── docs\               ← GitHub Pages 배포 폴더
│   └── (04_Runtime과 동일 구조)
└── 99_Archive\
```

---

# 8. data.js 구조

```
C:\Obsidian\Dooly\04_Runtime\data.js
C:\Obsidian\Dooly\docs\data.js (동일 내용)

var SOPS = [ ... ]  // 23개, keywords 필드 포함
var FAQS = [ ... ]  // 22개, keywords 필드 포함

SOP 카테고리: 복테, 오답노트, 비품, 장비, 루틴, 채점, 학생관리, 예외상황
FAQ 카테고리: 복사기, 복테, 오답노트, 채점, 비품, 제본기, 파일관리, 학생관리, 루틴
```

---

# 9. Dooly Mock 모드 동작

```
질문 입력
    │
    ▼
Mock 모드 (기본값)
    │
    ├── FAQ 전체 키워드 매칭
    ├── SOP 전체 키워드 매칭
    │
    ▼
관련 항목 N개 목록 표시
    ├── FAQ Q1 제목 ▼ (초록, 클릭하면 내용 펼치기)
    ├── SOP 1 제목 ▼ (주황, 클릭하면 내용 펼치기)
    └── [Mock 뱃지]

매칭 없으면 → "확인이 필요합니다" 출력
```

---

# 10. 환경 설정

| 항목 | 값 |
|------|-----|
| GitHub Pages URL | https://2passion.github.io/Dooly/ |
| 서버 포트 (로컬) | 8001 |
| 기본 모델 | Mock (오프라인) |
| ngrok 도메인 | polymer-distinct-feminize.ngrok-free.dev |
| PWA 앱 이름 | Dooly |
| PWA 아이콘 | 공룡 캐릭터 (원형, 흰색 배경) |

---

# 11. 완료된 작업지시서 (주요 목록)

| 번호 | 내용 | 커밋 |
|------|------|------|
| 34 | 파일명 수정 + 인수인계 + PWA manifest | a4c1ba2 |
| 36 | .gitignore 업데이트 | 5fcacf9 |
| 37 | data.js 분리 + Mock 고도화 | 3c031ce |
| 38 | RAG 실패 시 Mock 자동 전환 | 8cc20d4 |
| 39 | Mock 모델 기본값 설정 | 8a4f613 |
| 40 | 출처 태그 + 날짜/시간 표시 | ff59ea0 |
| 41 | Mock 다중 결과 + 아코디언 | b1054e6 |
| 42 | GitHub Pages 배포 설정 | 1823d52 |
| 44 | PWA 공룡 아이콘 + Dooly 이름 | a6b7196 |
| 45 | 공룡 캐릭터 원형 아이콘 교체 | 45a99aa |

---

# 12. 다음 작업 목록 (46번부터)

| 번호 | 작업 | 우선순위 |
|------|------|---------|
| 46 | 인수인계 파일 업데이트 + git push | 높음 |
| 47 | 아이폰 PWA 설치 테스트 (조교 출근 시) | 높음 |
| 48 | Task API 추가 (기기 간 동기화) | 보통 |
| 49 | SETUP_GUIDE.md 작성 | 보통 |
| 50 | Cloudflare Pages 전환 (Private) | 낮음 |
| 51 | Claude API 전환 (v2.0 준비) | 낮음 |

---

# 13. 사용자 기기 현황

| 기기 | 종류 | 상태 |
|------|------|------|
| 자습실 PC | Celeron G4900 데스크탑 | 보조 서버 (필요 시) |
| 노트북(화이트) | 삼성 350XCJ i5-10210U | 개발용 ✅ |
| 갤럭시 S25 | 스마트폰 | PWA 설치 완료 ✅ |
| 조교A, B | 아이폰 | PWA 테스트 예정 |
| 조교C | 갤럭시폰 | 사용자 기기 |

---

# 14. 트러블슈팅 기록

| 문제 | 원인 | 해결 |
|------|------|------|
| 탭 클릭 404 | HTML 링크 경로 불일치 | server.py 리다이렉트 (32번) |
| Dooly 중국어 답변 | qwen 모델 습관 | 시스템 프롬프트 강제 (33번) |
| file:// data.js 로드 실패 | 브라우저 보안 정책 | 서버 통해서 열기 |
| Syntax error line 366 | 괄호 중복 | 수동 수정 |
| GitHub Pages Private 불가 | 무료 계정 제한 | Public으로 변경 |
| 아이콘 파일명 중복 | dooly_source.png.png | 정상 처리됨 |

---

# 15. docs 폴더 동기화 규칙

04_Runtime 파일을 수정하면 docs 폴더도 동기화해야 한다.

```
수정 후 동기화:
copy 04_Runtime\{파일명} docs\{파일명}

Claude Code 작업지시서에
"docs 폴더도 동일하게 수정할 것" 명시
```

GitHub Pages는 docs\ 폴더를 서빙하므로
docs\ 폴더가 항상 최신 상태여야 한다.

---

# 16. CHANGELOG

## 2026-06-28
- feat: data.js 분리 (SOP 23개 + FAQ 22개)
- feat: Mock 모드 고도화 (다중 결과 + 아코디언)
- feat: 출처 태그 + 날짜/시간 표시
- feat: Mock 모델 기본값 설정
- feat: GitHub Pages 배포
- feat: PWA service-worker.js + 공룡 아이콘
- feat: 갤럭시 S25 PWA 설치 완료

## 2026-06-27
- fix: 탭 클릭 404 오류 수정
- fix: Dooly 중국어 답변 제거
- feat: ngrok 고정 도메인 설정
- feat: 자습실 PC 환경 구성 완료

---

# 17. 새 세션 시작 방법

```
1. 02_SESSION_HANDOVER.md 첨부
2. 04_PROJECT_GUIDE_v1.0.md 첨부
3. 05_WORKFLOW_GUIDE_v1.0.md 첨부
4. 아래 메시지 입력:
   "첨부한 파일을 읽고 프로젝트 현황을 파악해줘.
    다음 작업은 46번부터 이어서 진행할거야."
```

---

# STEP 3 — git 커밋 및 push

```
cd C:\Obsidian\Dooly

git add .
git commit -m "docs: SESSION_HANDOVER v5.0 업데이트 (PWA + GitHub Pages 완료)"
git push
```

# END OF ORDER
