# 02_SESSION_HANDOVER.md v8.0

작성일: 2026-06-29
세션: 2026-06-29 (주간)
프로젝트 버전: King Assistant OS v1.0 → v2.0 전환 진행 중
현재 마일스톤: Task #50 진행 중 (Claude API + Cloudflare Worker 연동)

---

# 0. AI 인수인계 규칙

새 세션의 AI는 반드시 다음 순서로 시작한다.

1. 이 파일 (02_SESSION_HANDOVER.md) 읽기
2. 04_PROJECT_GUIDE_v1.0.md 읽기
3. 05_WORKFLOW_GUIDE_v1.0.md 읽기
4. 현재 마일스톤 파악
5. 작업지시서 번호 순서대로 작업 진행

이미 완료된 작업은 다시 구현하지 않는다.
다음 작업은 50번 이어서 진행한다 (Step 4부터).

---

# 1. 워크플로우 원칙 (반드시 준수)

- claude.ai: 검토 + 작업지시서 md 파일 생성 (다운로드 제공)
- Claude Code (VS Code): md 파일 읽고 실행 + git push
- 인수인계 md 파일 작성도 동일하게 claude.ai에서 생성 → Claude Code에서 저장/push
- claude.ai에서 직접 파일을 실행하거나 git 명령을 수행하지 않음

---

# 2. v2.0 확정 구조

```
GitHub (코드 저장 + 버전 관리)
    ↓ git push → 자동 배포
Cloudflare Pages (PWA 서빙) ← 배포 완료
    ├── Cloudflare Worker (프록시) ← Step 1~3 완료
    │       ↓
    │   Claude API → Dooly AI 답변
    └── Supabase → Task 동기화 (기기간 공유)
```

| 도구 | 역할 | 상태 |
|------|------|------|
| GitHub | 코드 저장 + 버전 관리 | ✅ 사용 중 |
| Cloudflare Pages | PWA 배포 | ✅ 완료 |
| Cloudflare Worker | Claude API 프록시 | 🔄 50번 진행 중 |
| Claude API | Dooly AI 답변 | 🔄 50번 진행 중 |
| Supabase | Task DB (기기간 동기화) | 🔜 51번 |

---

# 3. 완료된 작업 전체

| 번호 | 작업 | 커밋 | 상태 |
|------|------|------|------|
| 47 | 아이폰 PWA 설치 가이드 | cfcb795 | ✅ |
| 48A | 자습실 PC FastAPI Task API | - | ✅ |
| 48B | PWA Task 화면 FastAPI 연동 | d9769a8 | ✅ |
| 48B-fix | IP 주소 수정 | d9769a8 | ✅ |
| 49 | 서비스워커 캐시 버전 갱신 | d8db5dc | ✅ |
| - | data.js 캐시 강제 갱신 | 9fd23bb | ✅ |
| - | SESSION_HANDOVER v7.0 | feb9787 | ✅ |
| - | 방화벽 포트 8001 허용 | - | ✅ |
| - | Cloudflare Pages 배포 | - | ✅ |

---

# 4. Task #50 진행 현황

## 목표
Cloudflare Worker를 프록시로 사용하여 Claude API 연동

## 완료된 단계 (수동 작업)

### ✅ Step 1 — Cloudflare Worker 생성
- Worker 이름: `dooly-claude-proxy`
- URL: `https://dooly-claude-proxy.2davidpassion.workers.dev`
- 코드: Claude API 프록시 코드 배포 완료

### ✅ Step 2 — Worker 코드 교체
- Hello World 기본 코드 → Claude API 프록시 코드로 교체
- Deploy 완료

### 🔄 Step 3 — API 키 환경변수 설정 (미완료)
- Anthropic Console에서 크레딧 구매 시도 중
- USD 5 크레딧 구매 진행 중 (결제 버튼 활성화 문제 해결 필요)
- 완료 후: Worker Settings → Variables and Secrets → CLAUDE_API_KEY (Secret) 추가

### ⏳ Step 4 — PWA JS 수정 (대기 중)
- Worker URL 상수 추가
- getClaudeAnswer() 함수 추가
- handleUserMessage() Mock/AI 분기 처리
- buildDataContext() FAQ/SOP 컨텍스트 빌더 추가

### ⏳ Step 5 — 모드 전환 토글 UI 확인
### ⏳ Step 6 — git push 및 배포

## 작업지시서 위치
`C:\Obsidian\Dooly\03_Claude_Code\50_Order_Claude_API_Worker_v1.0.md`

---

# 5. 배포 URL

| 환경 | URL | 상태 |
|------|------|------|
| GitHub Pages | https://2passion.github.io/Dooly/ | ✅ 유지 |
| Cloudflare Pages | https://dooly-f4m.pages.dev | ✅ 운영 중 |
| Cloudflare Worker | https://dooly-claude-proxy.2davidpassion.workers.dev | ✅ 배포 완료 |

---

# 6. 시행착오 기록 (누적)

## 에러 1: tasks.json BOM 문제
- 증상: /tasks 엔드포인트 500 에러
- 원인: PowerShell 5.1의 Set-Content -Encoding UTF8이 BOM 추가 → Python json.load 실패
- 해결: BOM 없는 UTF-8로 재작성
- 향후 주의: `[System.IO.File]::WriteAllText("경로", "[]", $utf8NoBom)` 사용

## 에러 2: 자습실 PC IP 주소 변경
- 증상: 스마트폰에서 Task API 연결 안 됨
- 원인: 이전 IP(192.168.219.100) → 실제 IP 192.168.0.10으로 변경
- 해결: IP 수정 후 재배포
- 향후 주의: DHCP라 공유기 재시작 시 변경 가능 → v2.0 Supabase로 완전 해결 예정

## 에러 3: Python 서버 중복 실행
- 증상: ERROR [Errno 10048] 포트 8001 충돌
- 해결: 기존 프로세스 종료 후 run_server.bat으로 정식 실행

## 에러 4~6: 서비스워커 캐시 문제
- 해결: chrome://serviceworker-internals → Unregister 후 재접속
- service-worker.js 캐시 버전: king-assistant-v1 → king-assistant-v2

## 에러 7: Mixed Content 차단
- 증상: 스마트폰에서 ERR_CONNECTION_ABORTED
- 원인: HTTPS PWA에서 HTTP FastAPI 호출 → 브라우저 차단
- 근본 해결: v2.0 Cloudflare Worker + Supabase 전환으로 해결 예정

## 에러 8: Cloudflare Worker 생성 시 주의
- Workers & Pages → Create application → Workers 탭 선택
- "Start with Hello World!" 선택 후 이름 입력 → Deploy

## 에러 9: Anthropic 크레딧 구매 버튼 비활성화
- 증상: `크레딧 구매` 버튼이 회색으로 비활성화
- 원인: 청구지 주소 또는 신용카드 입력 미완료로 추정
- 현재 상태: 해결 중
- 다음 시도: 페이지 새로고침 후 카드 정보 재입력

## 브라우저별 PWA 지원
- Chrome: 정상 / 삼성 브라우저: 정상
- 네이버 앱: 지원 안 됨 / 카카오톡 인앱: 지원 안 됨

---

# 7. v2.0 개발 계획

| 번호 | 작업 | 우선순위 | 상태 |
|------|------|---------|------|
| 50 | Claude API 연동 (Dooly 챗봇) | 높음 | 🔄 진행 중 |
| 51 | Supabase Task 동기화 | 높음 | 🔜 대기 |
| 52 | Cloudflare Pages PWA 테스트 | 보통 | 🔜 대기 |
| 53 | SETUP_GUIDE.md 작성 | 보통 | 🔜 대기 |

---

# 8. 환경 정보

| 항목 | 내용 |
|------|------|
| GitHub 저장소 | https://github.com/2passion/Dooly.git |
| GitHub Pages URL | https://2passion.github.io/Dooly/ |
| Cloudflare Pages URL | https://dooly-f4m.pages.dev |
| Cloudflare Worker URL | https://dooly-claude-proxy.2davidpassion.workers.dev |
| Cloudflare 계정 | 2davidpassion@gmail.com |
| 자습실 PC IP | 192.168.0.10 (DHCP, 변경 가능) |
| FastAPI 포트 | 8001 |
| tasks.json 경로 | C:\★공유폴더★\Sync\Dooly\tasks.json |
| 서비스워커 버전 | king-assistant-v2 |

---

# 9. 새 세션 시작 방법

1. 02_SESSION_HANDOVER.md 첨부
2. 04_PROJECT_GUIDE_v1.0.md 첨부
3. 05_WORKFLOW_GUIDE_v1.0.md 첨부
4. 아래 메시지 입력:

```
첨부한 파일을 읽고 프로젝트 현황을 파악해줘.
Task #50 Step 3부터 이어서 진행할거야.
Anthropic API 키 발급 완료 후 Worker 환경변수 설정부터 시작.
```
