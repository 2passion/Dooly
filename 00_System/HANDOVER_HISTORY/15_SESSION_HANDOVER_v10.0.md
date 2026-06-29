# 02_SESSION_HANDOVER.md v10.0

작성일: 2026-06-29
세션: 2026-06-29 (주간)
프로젝트 버전: King Assistant OS v2.0 전환 진행 중
현재 마일스톤: Task #51 — Vercel 이전 (Gemini API 위치 문제 해결)

---

# 0. AI 인수인계 규칙

새 세션의 AI는 반드시 다음 순서로 시작한다.

1. 이 파일 (02_SESSION_HANDOVER.md) 읽기
2. 04_PROJECT_GUIDE_v1.0.md 읽기
3. 05_WORKFLOW_GUIDE_v1.0.md 읽기
4. 현재 마일스톤 파악
5. 작업지시서 번호 순서대로 작업 진행

이미 완료된 작업은 다시 구현하지 않는다.
다음 작업은 51번 작업지시서부터 진행한다.

---

# 1. 워크플로우 원칙 (반드시 준수)

- claude.ai: 검토 + 작업지시서 md 파일 생성 (다운로드 제공)
- Claude Code (VS Code): md 파일 읽고 실행 + git push
- 인수인계 md 파일 작성도 동일하게 claude.ai에서 생성 → Claude Code에서 저장/push
- claude.ai에서 직접 파일을 실행하거나 git 명령을 수행하지 않음

---

# 2. v2.0 확정 구조 (변경됨: Cloudflare → Vercel)

```
GitHub (코드 저장 + 버전 관리)
    ↓ git push → 자동 배포
Vercel (PWA 서빙 + Gemini 프록시) ← Task #51 진행 중
    ↓
Gemini API (미국 서버 → 정상)
Supabase → Task 동기화 (Task #52 예정)
```

| 도구 | 역할 | 상태 |
|------|------|------|
| GitHub | 코드 저장 + 버전 관리 | ✅ 사용 중 |
| Vercel | PWA 서빙 + Gemini 프록시 | 🔄 51번 진행 중 |
| Gemini API | Dooly AI 답변 | 🔄 51번 진행 중 |
| Cloudflare Pages | PWA 배포 (구) | ⏸ 방치 예정 |
| Cloudflare Worker | API 프록시 (구) | ⏸ 방치 예정 |
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

---

# 4. Task #51 진행 현황

## 목표
Cloudflare → Vercel 완전 이전 (Gemini API 위치 문제 해결)

## 작업지시서
`C:\Obsidian\Dooly\03_Claude_Code\51_Order_Vercel_Migration_v1.0.md`

## 단계

| Step | 내용 | 상태 |
|------|------|------|
| Step 1 | Vercel 가입 + GitHub 연동 | ⏳ 수동 |
| Step 2 | api/gemini.js 생성 | ⏳ Claude Code |
| Step 3 | PWA WORKER_URL 변경 | ⏳ Claude Code |
| Step 4 | Vercel 환경변수 설정 | ⏳ 수동 |
| Step 5 | git push | ⏳ Claude Code |
| Step 6 | 최종 테스트 | ⏳ |
| Step 7 | Cloudflare 정리 | ⏳ 선택 |

---

# 5. 배포 URL

| 환경 | URL | 상태 |
|------|------|------|
| GitHub Pages | https://2passion.github.io/Dooly/ | ✅ 유지 |
| Cloudflare Pages | https://dooly-f4m.pages.dev | ⏸ 방치 예정 |
| Cloudflare Worker | https://dooly-claude-proxy.2davidpassion.workers.dev | ⏸ 방치 예정 |
| Vercel | 미정 (Step 1 완료 후 확인) | 🔄 진행 중 |

---

# 6. 시행착오 기록 (누적)

## 에러 1~9: 이전 세션 참고

## 에러 10: Claude API → Gemini API 전환 (2026-06-29)
- 전환 이유: Anthropic 크레딧 구매 불가
- Gemini API 키 보유 중

## 에러 11: Gemini API 위치 차단 문제 (2026-06-29)
- 증상: "User location is not supported for the API use"
- 원인: Cloudflare Worker가 한국/아시아 서버에서 실행됨
  → Gemini API가 해당 위치에서의 호출 차단
- 시도한 것:
  - cf: { country: 'US' } 추가 → 효과 없음
  - resolveOverride 추가 → 효과 없음
  - 모델명 변경 (gemini-1.5-flash, gemini-2.0-flash, gemini-2.5-flash) → 동일 에러
  - 새 API 키 발급 → 동일 에러
  - Gemini API 결제 (₩25,000) → 동일 에러
- 결론: Cloudflare Worker 자체가 Gemini API와 궁합이 안 맞음
  → Vercel(미국 서버)로 이전

## 에러 12: Gemini API 일일 한도 초과 (2026-06-29)
- 원인: 테스트 과정에서 무료 티어 일일 한도 소진
- 해결: Gemini API 결제 (₩25,000 크레딧 충전)

## 브라우저별 PWA 지원
- Chrome: 정상 / 삼성 브라우저: 정상
- 네이버 앱: 지원 안 됨 / 카카오톡 인앱: 지원 안 됨

---

# 7. v2.0 개발 계획

| 번호 | 작업 | 우선순위 | 상태 |
|------|------|---------|------|
| 51 | Vercel 이전 (PWA + Gemini 프록시) | 높음 | 🔄 진행 중 |
| 52 | Supabase Task 동기화 | 높음 | 🔜 대기 |
| 53 | SETUP_GUIDE.md 작성 | 보통 | 🔜 대기 |

---

# 8. 환경 정보

| 항목 | 내용 |
|------|------|
| GitHub 저장소 | https://github.com/2passion/Dooly.git |
| Vercel URL | 미정 (Task #51 완료 후 업데이트) |
| Cloudflare Pages | https://dooly-f4m.pages.dev (방치 예정) |
| Cloudflare Worker | https://dooly-claude-proxy.2davidpassion.workers.dev (방치 예정) |
| AI API | Gemini API (gemini-2.5-flash) |
| Gemini 크레딧 | ₩25,000 충전 완료 |
| 서비스워커 버전 | king-assistant-v2 |
| tasks.json 경로 | C:\★공유폴더★\Sync\Dooly\tasks.json |

---

# 9. 새 세션 시작 방법

1. 02_SESSION_HANDOVER.md 첨부
2. 04_PROJECT_GUIDE_v1.0.md 첨부
3. 05_WORKFLOW_GUIDE_v1.0.md 첨부
4. 아래 메시지 입력:

```
첨부한 파일을 읽고 프로젝트 현황을 파악해줘.
Task #51 Vercel 이전 작업지시서대로 Step 1부터 진행할거야.
작업지시서: C:\Obsidian\Dooly\03_Claude_Code\51_Order_Vercel_Migration_v1.0.md
```
