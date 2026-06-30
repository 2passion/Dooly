# README.md
# docs\ — King Assistant OS v2.0 운영 파일

작성일: 2026-06-30
프로젝트: King Assistant OS v2.0
배포: https://dooly-eight.vercel.app

---

## 이 폴더는 무엇인가?

Vercel이 서빙하는 현재 운영 중인 파일들이다.
GitHub에 push하면 Vercel이 자동으로 이 폴더를 배포한다.
Vercel Root Directory 설정: docs (공백 없이)

---

## 운영 구조

```
GitHub (코드 저장)
    ↓ git push → 자동 배포
Vercel (PWA 서빙 + API 프록시)
    ├── docs/api/gemini.js  → Gemini API 프록시
    └── docs/api/tasks.js   → Supabase Task API 프록시
        ↓
Supabase (Task DB — 기기간 동기화)
```

---

## 파일 목록 및 설명

### HTML 화면 파일

| 파일 | URL | 설명 |
|------|-----|------|
| index.html | /index.html | 홈 화면 (메인 진입점) |
| 02_Task_v1.html | /02_Task_v1.html | 업무 Task 관리 화면 (Supabase 연동) |
| 03_SOP_v1.html | /03_SOP_v1.html | SOP 조회 화면 |
| 04_FAQ_v1.html | /04_FAQ_v1.html | FAQ 조회 화면 |
| 05_Notice_v1.html | /05_Notice_v1.html | 공지사항 화면 |
| 06_Dooly_v1.html | /06_Dooly_v1.html | AI 챗봇 Dooly 메인 화면 (Gemini 연동) |
| 07_Settings_v1.html | /07_Settings_v1.html | 설정 화면 |

### JavaScript 파일

| 파일 | 설명 |
|------|------|
| data.js | FAQ/SOP 전체 데이터 (FAQS, SOPS 배열) |
| service-worker.js | PWA 캐시 관리 (버전: king-assistant-v3) |

### PWA 설정 파일

| 파일 | 설명 |
|------|------|
| manifest.json | PWA 설정 (이름, 아이콘, 시작URL 등) |
| icons\ | PWA 아이콘 폴더 (아기공룡, 192/512px) |

### API 프록시 (Vercel Functions)

| 파일 | 엔드포인트 | 설명 |
|------|-----------|------|
| api/gemini.js | /api/gemini | Gemini API 프록시 (GEMINI_API_KEY 사용) |
| api/tasks.js | /api/tasks | Supabase Task CRUD API (SUPABASE_URL, SUPABASE_ANON_KEY 사용) |

---

## 핵심 주의사항

- buildDataContext() 함수 수정 금지 (속도 저하 + 답변 잘림 발생)
- Vercel 환경변수: GEMINI_API_KEY, SUPABASE_URL, SUPABASE_ANON_KEY
- 문제 발생 시 롤백 커밋: 35f7576
- 현재 안정 커밋: a2316c2

---

## 구버전 파일 위치

v1.0 로컬 FastAPI 시절 파일:
C:\Obsidian\Dooly\99_Archive\04_Runtime_v1_backup\
