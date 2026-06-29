# Dooly 앱 구조 설명서 v1.0

작성일: 2026-06-29
프로젝트: King Assistant OS v2.0
문서 목적: Dooly 앱의 전체 구조, AI 답변 흐름, Task 동기화 흐름 설명

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
│  레이어 2 — 배포 인프라                              │
│  GitHub  →  Cloudflare Pages  +  Cloudflare Worker  │
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
│  (gemini-1.5-   │              │  현재: 로컬 FastAPI │
│   flash)        │              │                    │
└─────────────────┘              └───────────────────┘
```

---

## 2. 레이어별 상세 설명

### 레이어 1 — 개발 환경

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

### 레이어 2 — 배포 인프라

| 도구 | 역할 | URL | 상태 |
|------|------|-----|------|
| GitHub | 코드 버전 관리 | github.com/2passion/Dooly | ✅ 운영 중 |
| Cloudflare Pages | PWA 서빙 (HTTPS) | dooly-f4m.pages.dev | ✅ 운영 중 |
| Cloudflare Worker | API 프록시 | dooly-claude-proxy.2davidpassion.workers.dev | 🔄 구성 중 |

**Cloudflare Worker가 필요한 이유:**
- PWA는 HTTPS로 서빙됨
- Gemini API 키를 클라이언트에 노출하면 보안 위험
- Worker가 중간에서 API 키를 숨기고 요청을 중계함

---

### 레이어 3 — 사용자 기기 (PWA)

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

---

### 레이어 4 — AI 엔진

| 항목 | 내용 |
|------|------|
| API | Google Gemini API |
| 모델 | gemini-1.5-flash |
| 무료 티어 | 분당 15회, 일 1,500회 (학원 사용량 충분) |
| 변경 이유 | Anthropic 크레딧 구매 불가 → Gemini API로 전환 (2026-06-29) |

---

### 레이어 5 — 데이터베이스

| 구분 | 현재 (v1.0) | 미래 (v2.0) |
|------|------------|------------|
| 방식 | 로컬 FastAPI | Supabase (클라우드) |
| 서버 | 자습실 PC (192.168.0.10:8001) | 클라우드 (항상 가동) |
| 문제 | IP 변경, PC 꺼지면 접속 불가 | 해결됨 |
| 구현 | Task #48 완료 | Task #51 예정 |

---

## 3. AI 답변 흐름

조교가 둘리에게 질문하면 아래 순서로 처리된다.

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
    │     Cloudflare Worker
    │     POST { message, context }
    │               │
    │               ▼
    │         Gemini API
    │     gemini-1.5-flash 추론
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

**⑤ Cloudflare Worker 전송**
- `POST { message, context }` 전송
- Worker에서 GEMINI_API_KEY(Secret) 주입
- API 키가 클라이언트에 노출되지 않음

**⑥ Gemini API 추론**
- 시스템 프롬프트 + FAQ/SOP 컨텍스트 + 질문 전달
- gemini-1.5-flash 모델이 답변 생성

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

## 4. Task 동기화 흐름

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

---

### 미래 구조 (v2.0) — Supabase (Task #51 예정)

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

## 5. 시행착오 기록 (AI API 변경)

### Claude API → Gemini API 전환 (2026-06-29)

**배경:**
- 원래 Task #50은 Claude API(Anthropic) 연동으로 계획됨
- Anthropic Console에서 크레딧 구매 버튼 비활성화 문제 발생

**시도한 것:**
- 청구지 주소 입력 (성명, 국가, 도시, 주소, 우편번호) ✅
- 신용카드 번호/만료일/CVC 입력 (삼성카드 VISA) ✅
- 해외결제 허용 확인 ✅
- 페이지 새로고침 반복 ✅
- platform.claude.com에서 시도 ✅

**원인 추정:**
- Anthropic Console 계정이 "평가 액세스(Free)" 플랜
- 크레딧 구매 기능이 잠겨있는 버그로 추정
- GitHub Issue #62644 동일 증상 보고됨

**결론:**
- Claude API 포기 → Gemini API로 전환
- 기존 보유 중인 Gemini API 키 (`AIza...`) 사용
- Worker 코드 및 환경변수 Gemini용으로 교체 필요

---

## 6. 현재 진행 상태

| 항목 | 내용 |
|------|------|
| 진행 중 작업 | Task #50 — Gemini API + Cloudflare Worker 연동 |
| 작업지시서 | `50_Order_Gemini_API_Worker_v2.0.md` |
| 다음 작업 | Task #51 — Supabase Task 동기화 |
| 배포 URL | https://dooly-f4m.pages.dev |

---

## 7. 환경 정보

| 항목 | 내용 |
|------|------|
| GitHub 저장소 | https://github.com/2passion/Dooly.git |
| Cloudflare Pages | https://dooly-f4m.pages.dev |
| Cloudflare Worker | https://dooly-claude-proxy.2davidpassion.workers.dev |
| AI 모델 | gemini-1.5-flash |
| 서비스워커 버전 | king-assistant-v2 |
| FastAPI 포트 | 8001 (현재) |
| tasks.json 경로 | C:\★공유폴더★\Sync\Dooly\tasks.json |
