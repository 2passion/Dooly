# 55_Order_Archive_Runtime_v1.0.md
# Task #55 — 04_Runtime 아카이브 + README 작성

작성일: 2026-06-30
작업자: Claude Code

---

# 작업 개요

| 항목 | 내용 |
|------|------|
| 작업 번호 | Task #55 |
| 작업명 | 04_Runtime 아카이브 + README 작성 |
| 작업 유형 | 폴더 이동 + 문서 작성 |
| 예상 소요 | 5분 이내 |

## 작업 배경
- v1.0 시절 로컬 FastAPI 서버용 파일들이 04_Runtime에 남아있음
- v2.0 Vercel 배포로 마이그레이션 완료 후 구버전 파일 미정리 상태
- 현재 운영 파일은 docs\ 폴더에만 있음
- 혼동 방지를 위해 04_Runtime을 99_Archive로 이동하고 README로 설명 남김

---

# 작업 1 — 04_Runtime 폴더 아카이브 이동

## 실행 명령어

```powershell
cd C:\Obsidian\Dooly

# 99_Archive 안에 백업 폴더 생성 후 이동
Move-Item -Path "04_Runtime" -Destination "99_Archive\04_Runtime_v1_backup"
```

## 결과 확인
```
C:\Obsidian\Dooly\99_Archive\04_Runtime_v1_backup\  ← 이동 완료
C:\Obsidian\Dooly\04_Runtime\                       ← 삭제됨 (없어야 함)
```

---

# 작업 2 — 아카이브 README 작성

## 파일 경로
```
C:\Obsidian\Dooly\99_Archive\04_Runtime_v1_backup\README_archive.md
```

## 파일 내용

```markdown
# README_archive.md
# 04_Runtime_v1_backup — 아카이브 설명

작성일: 2026-06-30
아카이브 이유: v2.0 Vercel 마이그레이션 완료로 구버전 보관

---

## 이 폴더는 무엇인가?

King Assistant OS v1.0 시절 로컬 FastAPI 서버에서 직접 실행하던 파일들이다.
v2.0에서 Vercel + Supabase 구조로 전환하면서 운영에서 제외되었다.
현재 운영 파일은 C:\Obsidian\Dooly\docs\ 폴더에 있다.

---

## 구버전(v1.0)과 현재(v2.0) 차이

| 항목 | v1.0 (이 폴더) | v2.0 (docs\) |
|------|---------------|--------------|
| 서버 | 자습실 PC FastAPI 로컬 서버 | Vercel 클라우드 |
| AI | Ollama 로컬 모델 | Gemini API |
| Task DB | 없음 (로컬만) | Supabase (기기간 동기화) |
| 접속 방법 | ngrok URL | dooly-eight.vercel.app |
| PWA | manifest 링크 태그 없음 | manifest 정상 연결 |

---

## 파일 목록 및 설명

| 파일 | 설명 |
|------|------|
| icons\ | PWA 아이콘 폴더 (T-Rex 구버전 아이콘) |
| index.html | 홈 화면 (v1.0) |
| 02_Task_v1.html | 업무 Task 관리 화면 (v1.0, Supabase 미연동) |
| 03_SOP_v1.html | SOP 조회 화면 (v1.0) |
| 04_FAQ_v1.html | FAQ 조회 화면 (v1.0) |
| 05_Notice_v1.html | 공지사항 화면 (v1.0) |
| 06_Dooly_v1.html | AI 챗봇 Dooly 화면 (v1.0, Ollama 연동) |
| 07_Settings_v1.html | 설정 화면 (v1.0) |
| data.js | FAQ/SOP 데이터 (v1.0) |
| manifest.json | PWA 설정 (v1.0, 링크 태그 누락 상태) |
| service-worker.js | PWA 캐시 관리 (v1.0) |

---

## 주의사항

- 이 폴더의 파일은 현재 운영에 사용되지 않는다
- 참고용으로만 열람할 것
- 수정하거나 Vercel에 배포하지 말 것
- 현재 운영 파일 위치: C:\Obsidian\Dooly\docs\
```

---

# 작업 3 — docs\ README 작성

## 파일 경로
```
C:\Obsidian\Dooly\docs\README.md
```

## 파일 내용

```markdown
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
```

---

# 작업 4 — git push

```powershell
cd C:\Obsidian\Dooly
git add .
git commit -m "docs: 04_Runtime 아카이브 이동 + README 작성 (#55)"
git push
```

---

# 완료 확인

```
□ 99_Archive\04_Runtime_v1_backup\ 폴더 존재 확인
□ 04_Runtime\ 폴더 없어졌는지 확인
□ 99_Archive\04_Runtime_v1_backup\README_archive.md 존재 확인
□ docs\README.md 존재 확인
□ GitHub 커밋 확인
```

---

# END
