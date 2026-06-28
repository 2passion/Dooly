# 02_SESSION_HANDOVER.md v7.0

작성일: 2026-06-28
세션: 2026-06-28 (야간)
프로젝트 버전: King Assistant OS v1.0 → v2.0 전환 준비
현재 마일스톤: Phase 8 완료 준비 + v2.0 설계 확정

---

# 0. AI 인수인계 규칙

새 세션의 AI는 반드시 다음 순서로 시작한다.

1. 이 파일 (02_SESSION_HANDOVER.md) 읽기
2. 04_PROJECT_GUIDE_v1.0.md 읽기
3. 05_WORKFLOW_GUIDE_v1.0.md 읽기
4. 현재 마일스톤 파악
5. 작업지시서 번호 순서대로 작업 진행

이미 완료된 작업은 다시 구현하지 않는다.
다음 작업은 50번부터 시작한다.

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
    ├── Claude API → Dooly AI 답변
    └── Supabase → Task 동기화 (기기간 공유)
```

| 도구 | 역할 | 상태 |
|------|------|------|
| GitHub | 코드 저장 + 버전 관리 | ✅ 사용 중 |
| Cloudflare Pages | PWA 배포 | ✅ 설정 완료 |
| Claude API | Dooly AI 답변 | 🔜 50번 |
| Supabase | Task DB (24시간) | 🔜 51번 |

---

# 3. 완료된 작업 (이번 세션 전체)

| 번호 | 작업 | 커밋 | 상태 |
|------|------|------|------|
| 47 | 아이폰 PWA 설치 가이드 | cfcb795 | ✅ |
| 48A | 자습실 PC FastAPI Task API | - | ✅ |
| 48B | PWA Task 화면 FastAPI 연동 | d9769a8 | ✅ |
| 48B-fix | IP 주소 수정 | d9769a8 | ✅ |
| 49 | 서비스워커 캐시 버전 갱신 | d8db5dc | ✅ |
| - | data.js 캐시 강제 갱신 | 9fd23bb | ✅ |
| - | SESSION_HANDOVER v6.0 | feb9787 | ✅ |
| - | 방화벽 포트 8001 허용 | - | ✅ |
| - | Cloudflare Pages 배포 | - | ✅ |

---

# 4. 배포 URL

| 환경 | URL | 상태 |
|------|------|------|
| GitHub Pages | https://2passion.github.io/Dooly/ | ✅ 유지 |
| Cloudflare Pages | https://dooly-f4m.pages.dev | ✅ 신규 |

---

# 5. 전체 시행착오 기록

## 에러 1: tasks.json BOM 문제
- 증상: /tasks 엔드포인트 500 에러
- 원인: PowerShell 5.1의 Set-Content -Encoding UTF8이 BOM(EF BB BF) 추가 → Python json.load 실패
- 해결: BOM 없는 UTF-8로 재작성
- 향후 주의: tasks.json 생성 시 반드시 BOM 없는 UTF-8 사용
  $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText("경로\tasks.json", "[]", $utf8NoBom)

## 에러 2: 자습실 PC IP 주소 변경
- 증상: 스마트폰에서 Task API 연결 안 됨
- 원인: 작업지시서에 이전 IP(192.168.219.100) 기재, 실제 IP 192.168.0.10으로 변경
- 해결: 48B 작업지시서 IP 수정 후 재배포
- 향후 주의: 자습실 PC IP가 고정 IP 아님. 공유기 재시작 시 변경 가능
  → v2.0 Supabase 전환하면 IP 문제 완전 해결

## 에러 3: Python 서버 2개 중복 실행
- 증상: ERROR [Errno 10048] 포트 8001 충돌
- 원인: Claude Code 백그라운드 서버 실행 → 기존 서버와 중복
- 해결: 기존 프로세스 종료 후 run_server.bat으로 정식 실행
- 향후 주의: 서버 실행 전 포트 8001 사용 여부 확인

## 에러 4: 온라인 상태 표시 안 됨
- 증상: PWA 업무 탭에서 동기화 상태 바 미표시
- 원인: IP 주소 불일치 + 서비스워커 캐시 이전 버전 유지
- 해결: chrome://serviceworker-internals → 2passion.github.io/Dooly → Unregister

## 에러 5: 서비스워커 Unregister 후 404
- 증상: Unregister 후 접속 시 404
- 원인: 캐시 완전 삭제 후 GitHub Pages에서 새로 받아오는 과정
- 해결: 정확한 URL 재입력 (https://2passion.github.io/Dooly/)

## 에러 6: data.js 404
- 증상: 스마트폰에서 data.js 접속 시 404
- 원인: GitHub Pages 캐시 미갱신
- 해결: data.js + service-worker.js 캐시 버전 갱신 후 재배포
  service-worker.js: king-assistant-v1 → king-assistant-v2

## 에러 7: Mixed Content 차단 (미해결)
- 증상: 스마트폰에서 ERR_CONNECTION_ABORTED
- 원인: HTTPS PWA에서 HTTP FastAPI 호출 → 브라우저 차단
- 현재 상태: 미해결
- 근본 해결: v2.0 Supabase 전환으로 해결 예정

## 에러 8: Cloudflare Workers & Pages 혼동
- 증상: Worker 생성 화면으로 잘못 진입
- 원인: Workers & Pages 메뉴에서 Worker 탭 선택
- 해결: 하단 "Looking to deploy Pages? Get started" 링크 클릭
- 향후 주의: Pages 생성 시 반드시 Pages 탭 선택

## 브라우저별 PWA 지원
- Chrome: 정상
- 삼성 브라우저: 정상
- 네이버 앱: 지원 안 됨
- 카카오톡 인앱: 지원 안 됨

---

# 6. v2.0 개발 계획

목표: 업무내용 동기화 + AI 챗봇 답변 성능 개선 (속도, 온오프, 모델 선택)

| 번호 | 작업 | 우선순위 |
|------|------|---------|
| 50 | Claude API 연동 (Dooly 챗봇) | 높음 |
| 51 | Supabase Task 동기화 | 높음 |
| 52 | Cloudflare Pages PWA 테스트 | 보통 |
| 53 | SETUP_GUIDE.md 작성 | 보통 |

---

# 7. 환경 정보

| 항목 | 내용 |
|------|------|
| GitHub 저장소 | https://github.com/2passion/Dooly.git |
| GitHub Pages URL | https://2passion.github.io/Dooly/ |
| Cloudflare Pages URL | https://dooly-f4m.pages.dev |
| Cloudflare 계정 | 2davidpassion@gmail.com |
| 자습실 PC IP | 192.168.0.10 (DHCP, 변경 가능) |
| FastAPI 포트 | 8001 |
| tasks.json 경로 | C:\★공유폴더★\Sync\Dooly\tasks.json |
| 서비스워커 버전 | king-assistant-v2 |

---

# 8. 새 세션 시작 방법

1. 02_SESSION_HANDOVER.md 첨부
2. 04_PROJECT_GUIDE_v1.0.md 첨부
3. 05_WORKFLOW_GUIDE_v1.0.md 첨부
4. 아래 메시지 입력:
   "첨부한 파일을 읽고 프로젝트 현황을 파악해줘.
    다음 작업은 50번부터 이어서 진행할거야.
    v2.0 목표: Claude API + Supabase 연동"
