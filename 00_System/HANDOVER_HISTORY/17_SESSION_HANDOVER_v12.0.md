# 02_SESSION_HANDOVER.md v11.0

작성일: 2026-06-29
세션: 2026-06-29 (주간)
프로젝트 버전: King Assistant OS v2.0
현재 마일스톤: Task #51 완료 — Vercel + Gemini API 연동 성공

---

# 0. AI 인수인계 규칙

새 세션의 AI는 반드시 다음 순서로 시작한다.

1. 이 파일 (02_SESSION_HANDOVER.md) 읽기
2. 04_PROJECT_GUIDE_v1.0.md 읽기
3. 05_WORKFLOW_GUIDE_v1.0.md 읽기
4. 현재 마일스톤 파악
5. 작업지시서 번호 순서대로 작업 진행

이미 완료된 작업은 다시 구현하지 않는다.
다음 작업은 52번부터 진행한다.

---

# 1. 워크플로우 원칙 (반드시 준수)

- claude.ai: 검토 + 작업지시서 md 파일 생성 (다운로드 제공)
- Claude Code (VS Code): md 파일 읽고 실행 + git push
- 인수인계 md 파일 작성도 동일하게 claude.ai에서 생성 → Claude Code에서 저장/push
- claude.ai에서 직접 파일을 실행하거나 git 명령을 수행하지 않음

## 작업지시서 파일 정리 자동화 (Claude Code 프롬프트)

```
아래 작업을 순서대로 실행해줘.

## 1. SESSION_HANDOVER 백업
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md 파일을
C:\Obsidian\Dooly\00_System\HANDOVER_HISTORY\{다음번호}_SESSION_HANDOVER_v{버전}.md 로 복사

## 2. SESSION_HANDOVER 업데이트
C:\Users\USER\Downloads\02_SESSION_HANDOVER_v{버전}.md 파일을
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md 로 덮어쓰기

## 3. 작업지시서 이동
C:\Users\USER\Downloads\{작업지시서파일명}.md 파일을
C:\Obsidian\Dooly\03_Claude_Code\{작업지시서파일명}.md 로 이동

## 4. git push
cd C:\Obsidian\Dooly
git add .
git commit -m "docs: SESSION_HANDOVER 업데이트 + 작업지시서 추가"
git push
```

---

# 2. v2.0 확정 구조 (완료)

```
GitHub (코드 저장 + 버전 관리)
    ↓ git push → 자동 배포
Vercel (PWA 서빙 + Gemini 프록시) ✅ 완료
    ↓
Gemini API (미국 서버 → 정상 작동) ✅ 완료
Supabase → Task 동기화 (Task #52 예정)
```

| 도구 | 역할 | 상태 |
|------|------|------|
| GitHub | 코드 저장 + 버전 관리 | ✅ 운영 중 |
| Vercel | PWA 서빙 + Gemini 프록시 | ✅ 완료 |
| Gemini API | Dooly AI 답변 | ✅ 완료 |
| Cloudflare Pages | PWA 배포 (구) | ⏸ 방치 |
| Cloudflare Worker | API 프록시 (구) | ⏸ 방치 |
| Supabase | Task DB (기기간 동기화) | 🔜 52번 |

---

# 3. 완료된 작업 전체

| 번호 | 작업 | 커밋 | 상태 |
|------|------|------|------|
| 47 | 아이폰 PWA 설치 가이드 | cfcb795 | ✅ |
| 48A | 자습실 PC FastAPI Task API | - | ✅ |
| 48B | PWA Task 화면 FastAPI 연동 | d9769a8 | ✅ |
| 49 | 서비스워커 캐시 버전 갱신 | d8db5dc | ✅ |
| 50 | Gemini API 연동 PWA JS 수정 | eb4bd2b | ✅ |
| 51 | Vercel 이전 + Gemini 프록시 | ae6ae84 | ✅ |

---

# 4. 배포 URL

| 환경 | URL | 상태 |
|------|------|------|
| GitHub 저장소 | https://github.com/2passion/Dooly.git | ✅ |
| Vercel (메인) | https://dooly-eight.vercel.app | ✅ 운영 중 |
| Dooly 챗봇 | https://dooly-eight.vercel.app/06_Dooly_v1.html | ✅ |
| Cloudflare Pages | https://dooly-f4m.pages.dev | ⏸ 방치 |
| Cloudflare Worker | https://dooly-claude-proxy.2davidpassion.workers.dev | ⏸ 방치 |

---

# 5. 시행착오 기록 (전체 누적)

## 에러 1: tasks.json BOM 문제
- 증상: /tasks 엔드포인트 500 에러
- 원인: PowerShell 5.1의 Set-Content -Encoding UTF8이 BOM 추가 → Python json.load 실패
- 해결: BOM 없는 UTF-8로 재작성
- 향후 주의: `[System.IO.File]::WriteAllText("경로", "[]", $utf8NoBom)` 사용

## 에러 2: 자습실 PC IP 주소 변경
- 증상: 스마트폰에서 Task API 연결 안 됨
- 원인: DHCP로 IP 변경됨
- 해결: IP 수정 후 재배포
- 근본 해결: Task #52 Supabase로 완전 해결 예정

## 에러 3: Python 서버 중복 실행
- 증상: ERROR [Errno 10048] 포트 8001 충돌
- 해결: 기존 프로세스 종료 후 run_server.bat으로 정식 실행

## 에러 4~6: 서비스워커 캐시 문제
- 해결: chrome://serviceworker-internals → Unregister 후 재접속
- service-worker.js 캐시 버전: king-assistant-v1 → king-assistant-v2

## 에러 7: Mixed Content 차단
- 증상: 스마트폰에서 ERR_CONNECTION_ABORTED
- 원인: HTTPS PWA에서 HTTP FastAPI 호출 → 브라우저 차단
- 해결: Vercel로 이전하여 완전 해결

## 에러 8: Cloudflare Worker 생성 시 주의
- Workers & Pages → Create application → Workers 탭 선택
- "Start with Hello World!" 선택 후 이름 입력 → Deploy

## 에러 9: Anthropic 크레딧 구매 버튼 비활성화
- 증상: 크레딧 구매 버튼 회색으로 영구 비활성화
- 원인: Anthropic Console 계정 "평가 액세스(Free)" 플랜 버그
- 결론: Claude API 포기 → Gemini API로 전환

## 에러 10: Claude API → Gemini API 전환
- 전환 일자: 2026-06-29
- 원인: Anthropic 크레딧 구매 불가
- 변경: Worker 코드, 환경변수, 모델명, PWA JS 함수명 모두 변경

## 에러 11: Gemini API 위치 차단 (핵심 문제)
- 증상: "User location is not supported for the API use"
- 원인: Cloudflare Worker가 한국/아시아 서버에서 실행됨
- 시도한 것:
  - cf: { country: 'US' } → 효과 없음
  - resolveOverride → 효과 없음
  - 모델명 변경 (gemini-1.5-flash, gemini-2.0-flash, gemini-2.5-flash) → 동일 에러
  - 새 API 키 발급 → 동일 에러
  - Gemini API 결제 (₩25,000) → 동일 에러
- 결론: Cloudflare Worker + Gemini API 조합 불가
  → Vercel(미국 서버)로 이전하여 완전 해결

## 에러 12: Gemini API 일일 한도 초과
- 원인: 테스트 과정에서 무료 티어 소진
- 해결: Gemini API 결제 (₩25,000 크레딧 충전)

## 에러 13: Gemini API 키 노출
- 증상: 채팅창에 API 키 직접 붙여넣기
- 조치: AI Studio에서 노출된 키 즉시 삭제 + 새 키 발급
- 향후 주의: API 키는 절대 채팅창에 입력하지 않음

## 에러 14: Gemini 모델명 오류
- gemini-1.5-flash → v1beta에서 404 (새 키에서)
- gemini-2.0-flash → 429 한도 초과 후 404
- gemini-2.0-flash-lite → "no longer available"
- gemini-2.5-flash → ✅ 정상 작동
- 결론: gemini-2.5-flash 사용

## 에러 15: Vercel Root Directory 설정
- 증상: api/gemini.js 404 에러
- 원인: Root Directory를 docs로 설정했으나 api/는 루트에 생성됨
- 해결: api/gemini.js → docs/api/gemini.js 로 이동
- 향후 주의: Vercel Root Directory = docs 이므로
  모든 파일은 docs/ 하위에 위치해야 함

## 에러 16: Vercel Root Directory 공백 문제
- 증상: Build Failed "docs " does not exist
- 원인: Root Directory 입력 시 "docs " (공백 포함)로 저장됨
- 해결: 공백 제거 후 "docs" 정확히 입력 → Save → Redeploy

## 브라우저별 PWA 지원
- Chrome: 정상 / 삼성 브라우저: 정상
- 네이버 앱: 지원 안 됨 / 카카오톡 인앱: 지원 안 됨

---

# 6. v2.0 개발 계획

| 번호 | 작업 | 우선순위 | 상태 |
|------|------|---------|------|
| 52 | Supabase Task 동기화 | 높음 | 🔜 대기 |
| 53 | SETUP_GUIDE.md 작성 | 보통 | 🔜 대기 |

---

# 7. 환경 정보

| 항목 | 내용 |
|------|------|
| GitHub 저장소 | https://github.com/2passion/Dooly.git |
| Vercel URL | https://dooly-eight.vercel.app |
| Vercel 계정 | GitHub 계정 (2passion) 연동 |
| Cloudflare Pages | https://dooly-f4m.pages.dev (방치) |
| Cloudflare Worker | https://dooly-claude-proxy.2davidpassion.workers.dev (방치) |
| AI API | Gemini API (gemini-2.5-flash) |
| Gemini 크레딧 | ₩25,000 충전 완료 |
| Gemini 프록시 경로 | docs/api/gemini.js |
| 서비스워커 버전 | king-assistant-v2 |
| tasks.json 경로 | C:\★공유폴더★\Sync\Dooly\tasks.json |

---

# 8. 새 세션 시작 방법

1. 02_SESSION_HANDOVER.md 첨부
2. 04_PROJECT_GUIDE_v1.0.md 첨부
3. 05_WORKFLOW_GUIDE_v1.0.md 첨부
4. 아래 메시지 입력:

```
첨부한 파일을 읽고 프로젝트 현황을 파악해줘.
다음 작업은 Task #52 Supabase Task 동기화야.
```
