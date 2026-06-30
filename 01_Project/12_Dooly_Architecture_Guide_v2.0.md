# Dooly 앱 구조 설명서 v2.0

작성일: 2026-06-29
프로젝트: King Assistant OS v2.0
이전 버전: 11_Dooly_Architecture_Guide_v1.0.md
문서 목적: Dooly 앱의 전체 구조, AI 답변 흐름, Task 동기화 흐름 설명 (Vercel 이전 반영)

---

## ⚡ v1.0 → v2.0 주요 변경사항 요약

| 항목 | v1.0 (이전) | v2.0 (현재) | 변경 이유 |
|------|------------|------------|----------|
| PWA 서빙 | Cloudflare Pages | Vercel | 관리 통합 |
| API 프록시 | Cloudflare Worker | Vercel Function | 한국 서버 위치 차단 문제 |
| AI 모델 | gemini-1.5-flash | gemini-2.5-flash | 모델 업데이트 |
| 배포 URL | dooly-f4m.pages.dev | dooly-eight.vercel.app | 플랫폼 변경 |
| 관리 포인트 | GitHub + Cloudflare | GitHub + Vercel | 단일화 |

---

## 1. 전체 구조 개요

Dooly 앱은 5개 레이어로 구성된다.

```
┌─────────────────────────────────────────────────────┐
│  레이어 1 — 개발 환경 (킹스 작업 공간)               │
│  claude.ai (설계)  │  Claude Code (실행)  │  Obsidian │
└─────────────────────┬───────────────────────────────┘
                      │ git push
┌─────────────────────▼───────────────────────────────┐
│  레이어 2 — 배포 인프라 (v2.0: Vercel로 통합)        │
│  GitHub  →  Vercel Pages (PWA) + Vercel Function    │
└─────────────────────┬───────────────────────────────┘
                      │ PWA 앱
┌─────────────────────▼───────────────────────────────┐
│  레이어 3 — 사용자 기기 (조교 스마트폰)              │
│  둘리 챗봇  │  Task 관리  │  Mock 모드  │  SOP 검색  │
└──────┬──────────────────────────────────────────────┘
       │ AI 모드                          │ Task API
┌──────▼──────────┐              ┌────────▼──────────┐
│  레이어 4       │              │  레이어 5          │
│  AI 엔진        │              │  데이터베이스       │
│  Gemini API     │              │  Supabase (예정)   │
│  gemini-2.5-    │              │  현재: 로컬 FastAPI │
│  flash          │              │                    │
└─────────────────┘              └───────────────────┘
```

---

## 2. 레이어별 상세 설명

### 레이어 1 — 개발 환경 (변경 없음)

| 도구 | 역할 | 비고 |
|------|------|------|
| claude.ai | 설계 + 작업지시서 md 작성 | 직접 파일 실행 안 함 |
| Claude Code (VS Code) | 코드 실행 + git push | md 파일 읽고 자동 실행 |
| Obsidian | 오프라인 백업 | `C:\Obsidian\Dooly\` |

**워크플로우 원칙:**
- claude.ai → 작업지시서 md 파일 생성 (다운로드)
- Claude Code → md 파일 읽고 실행 + git push
- claude.ai에서 직접 git 명령 수행 안 함

---

### 레이어 2 — 배포 인프라 ⚡ 변경됨

#### v1.0 구조 (이전)
```
GitHub → Cloudflare Pages (PWA 서빙)
              ↓
       Cloudflare Worker (API 프록시) → Gemini API ❌ 차단
```

#### v2.0 구조 (현재)
```
GitHub → Vercel (PWA 서빙 + API 프록시)
              ↓
         Gemini API ✅ 정상 (미국 서버)
```

| 도구 | 역할 | URL | 상태 |
|------|------|-----|------|
| GitHub | 코드 버전 관리 | github.com/2passion/Dooly | ✅ 운영 중 |
| Vercel | PWA 서빙 (HTTPS) | dooly-eight.vercel.app | ✅ 운영 중 |
| Vercel Function | Gemini API 프록시 | dooly-eight.vercel.app/api/gemini | ✅ 운영 중 |
| Cloudflare Pages | PWA 서빙 (구) | dooly-f4m.pages.dev | ⏸ 방치 |
| Cloudflare Worker | API 프록시 (구) | dooly-claude-proxy.2davidpassion.workers.dev | ⏸ 방치 |

**Vercel Function이 필요한 이유:**
- PWA는 HTTPS로 서빙됨
- Gemini API 키를 클라이언트에 노출하면 보안 위험
- Function이 중간에서 API 키를 숨기고 요청을 중계함
- **Vercel은 미국 서버 기반** → Gemini API 위치 차단 없음

---

### 레이어 3 — 사용자 기기 (변경 없음)

조교 스마트폰에 PWA 설치 (Chrome 또는 삼성 브라우저)

| 화면 | 기능 |
|------|------|
| 둘리 챗봇 | AI 질문 답변 (Mock / AI 모드 전환 가능) |
| Task 관리 | 업무 상태 추적 (Pending / In Progress / Review / Completed / Hold) |
| Mock 모드 | 오프라인 FAQ/SOP 검색 (data.js 참조) |
| SOP 검색 | 표준 운영 절차 검색 |

**지원 브라우저:**
- Chrome ✅ / 삼성 브라우저 ✅
- 네이버 앱 ❌ / 카카오톡 인앱 ❌

**접속 URL:**
```
https://dooly-eight.vercel.app/06_Dooly_v1.html
```

---

### 레이어 4 — AI 엔진 ⚡ 변경됨

| 항목 | v1.0 (이전) | v2.0 (현재) |
|------|------------|------------|
| API | Google Gemini API | Google Gemini API |
| 모델 | gemini-1.5-flash ❌ (404 오류) | gemini-2.5-flash ✅ |
| 프록시 | Cloudflare Worker | Vercel Function |
| 파일 경로 | (Worker 코드) | docs/api/gemini.js |
| 크레딧 | 무료 티어 | ₩25,000 충전 완료 |

**모델 변경 이유:**
- gemini-1.5-flash → 새 키에서 404 Not Found
- gemini-2.0-flash → "no longer available"
- gemini-2.5-flash → ✅ 정상 작동

---

### 레이어 5 — 데이터베이스 (변경 예정)

| 구분 | 현재 (v1.0) | 미래 (v2.0) |
|------|------------|------------|
| 방식 | 로컬 FastAPI | Supabase (클라우드) |
| 서버 | 자습실 PC (192.168.0.10:8001) | 클라우드 (항상 가동) |
| 문제 | IP 변경, PC 꺼지면 접속 불가 | 해결됨 |
| 구현 | Task #48 완료 | Task #52 예정 |

---

## 3. AI 답변 흐름 ⚡ 변경됨

조교가 둘리에게 질문하면 아래 순서로 처리된다.

### v1.0 흐름 (이전)
```
조교 질문 → PWA → Cloudflare Worker → Gemini API ❌ 위치 차단
```

### v2.0 흐름 (현재)
```
조교 질문
("복사기 종이 먹었어요")
        │
        ▼
┌───────────────┐
│  PWA 분기     │
│  Mock / AI?   │
└───┬───────────┘
    │               │
  Mock              AI
    │               │
    ▼               ▼
data.js       buildDataContext()
FAQ/SOP       (FAQ + SOP 데이터 조합)
로컬 검색            │
    │               ▼
    │     Vercel Function
    │     docs/api/gemini.js
    │     POST { message, context }
    │     (미국 서버 → 위치 차단 없음)
    │               │
    │               ▼
    │         Gemini API
    │     gemini-2.5-flash 추론
    │               │
    └──────┬────────┘
           │
           ▼
     조교 화면에 답변 출력
```

### 단계별 상세

**① 조교 질문**
- 스마트폰 PWA 챗봇 화면에 질문 입력

**② PWA 분기**
- 현재 모드 확인 (Mock 또는 AI)
- `handleUserMessage()` 함수에서 분기 처리

**③ Mock 모드 경로**
- `data.js`에서 FAQ / SOP 키워드 검색
- 오프라인에서도 작동
- 즉시 응답 (네트워크 불필요)

**④ AI 모드 경로 — 컨텍스트 빌드**
- `buildDataContext()` 함수 실행
- FAQ 데이터 + SOP 데이터를 텍스트로 조합
- 시스템 프롬프트와 함께 묶음

**⑤ Vercel Function 전송** ⚡ 변경됨
- `POST { message, context }` 전송
- Function에서 GEMINI_API_KEY(Sensitive) 주입
- API 키가 클라이언트에 노출되지 않음
- **미국 서버에서 실행** → Gemini API 위치 차단 없음

**⑥ Gemini API 추론**
- 시스템 프롬프트 + FAQ/SOP 컨텍스트 + 질문 전달
- gemini-2.5-flash 모델이 답변 생성

**⑦ 화면 출력**
- `{ answer: "..." }` 응답 수신
- 챗봇 화면에 답변 표시

### Dooly 시스템 프롬프트 (항상 포함)

```
당신은 킹수학 학원의 AI 비서 둘리(Dooly)입니다.
조교들의 업무를 돕고, FAQ와 SOP를 기반으로 정확하게 답변합니다.
모르는 내용은 추측하지 말고 "확인이 필요합니다."라고 답변하세요.

=== 참고 데이터 ===
[FAQ 전체 내용]
[SOP 전체 내용]

=== 조교 질문 ===
[질문 내용]
```

**예상 응답 시간:**
- Mock 모드: 즉시 (로컬 처리)
- AI 모드: 1~3초 (네트워크 + 추론 시간)

---

## 4. Task 동기화 흐름 (변경 없음)

### 현재 구조 (v1.0) — 로컬 FastAPI

```
스마트폰 A (조교A)  ──┐
                      ├──→  FastAPI 서버 (자습실 PC)
스마트폰 B (조교B)  ──┘     192.168.0.10:8001
                                    │
                               tasks.json
                          (C:\★공유폴더★\Sync\Dooly\)
```

**현재 문제점:**
- DHCP라 공유기 재시작 시 IP 변경됨
- 자습실 PC가 꺼지면 Task API 접속 불가
- HTTPS PWA → HTTP FastAPI 차단 (Mixed Content 에러)

### 미래 구조 (v2.0) — Supabase (Task #52 예정)

```
스마트폰 A (조교A)  ──┐
                      ├──→  Supabase (클라우드 DB)
스마트폰 B (조교B)  ──┘     실시간 동기화
```

**v2.0 장점:**
- IP 변경 문제 없음 (클라우드)
- 자습실 PC 꺼져도 항상 접속 가능
- 실시간 기기간 동기화
- HTTPS 통신으로 Mixed Content 문제 해결

---

## 5. 시행착오 기록 (전체 누적)

### v1.0 → v2.0 핵심 변경: Cloudflare → Vercel

#### 문제: Gemini API 위치 차단
- 증상: `"User location is not supported for the API use"`
- 원인: Cloudflare Worker가 한국/아시아 서버에서 실행됨
- 시도한 것:
  - `cf: { country: 'US' }` 추가 → 효과 없음
  - `resolveOverride` 추가 → 효과 없음
  - 모델명 변경 → 동일 에러
  - 새 API 키 발급 → 동일 에러
  - Gemini API 결제 (₩25,000) → 동일 에러
- 결론: **Cloudflare Worker + Gemini API 조합 불가**
- 해결: Vercel(미국 서버)로 이전

#### 문제: Gemini API 모델명 오류
| 모델명 | 결과 |
|--------|------|
| gemini-1.5-flash | 404 Not Found (새 키에서) |
| gemini-2.0-flash | 429 한도 초과 후 404 |
| gemini-2.0-flash-lite | "no longer available" |
| gemini-2.5-flash | ✅ 정상 작동 |

#### 문제: Vercel Root Directory 공백
- 증상: `Build Failed "docs " does not exist`
- 원인: Root Directory 입력 시 `"docs "` (공백 포함)
- 해결: 공백 제거 후 `docs` 정확히 입력 → Save → Redeploy

#### 문제: Vercel Function 경로 오류
- 증상: `api/gemini.js` 404 에러
- 원인: Root Directory = `docs`인데 `api/`는 루트에 생성됨
- 해결: `api/gemini.js` → `docs/api/gemini.js`로 이동

#### Claude API → Gemini API 전환
- 원인: Anthropic Console 크레딧 구매 버튼 비활성화
- 원인 추정: "평가 액세스(Free)" 플랜 버그
- 결론: Gemini API로 전환 (기존 보유 키 사용)

---

## 6. 현재 진행 상태

| 항목 | 내용 |
|------|------|
| 완료 작업 | Task #51 — Vercel 이전 + Gemini API 연동 |
| 다음 작업 | Task #52 — Supabase Task 동기화 |
| 배포 URL | https://dooly-eight.vercel.app/06_Dooly_v1.html |
| AI 답변 | ✅ 정상 작동 확인 |

---

## 7. 환경 정보

| 항목 | v1.0 | v2.0 (현재) |
|------|------|------------|
| GitHub 저장소 | github.com/2passion/Dooly | 동일 |
| PWA URL | dooly-f4m.pages.dev | dooly-eight.vercel.app |
| API 프록시 | Cloudflare Worker | Vercel Function (docs/api/gemini.js) |
| AI 모델 | gemini-1.5-flash | gemini-2.5-flash |
| 크레딧 | 무료 티어 | ₩25,000 충전 |
| 서비스워커 버전 | king-assistant-v2 | 동일 |
| tasks.json 경로 | C:\★공유폴더★\Sync\Dooly\tasks.json | 동일 (Task #52에서 Supabase로 이전 예정) |
