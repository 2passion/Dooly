# 02_SESSION_HANDOVER.md v14.0

작성일: 2026-06-30
세션: 2026-06-30 (주간)
프로젝트 버전: King Assistant OS v2.0
현재 마일스톤: Task #53 완료 — Supabase Task 동기화

---

# 0. AI 인수인계 규칙

새 세션의 AI는 반드시 다음 순서로 시작한다.

1. 이 파일 (02_SESSION_HANDOVER.md) 읽기
2. 04_PROJECT_GUIDE_v1.0.md 읽기
3. 05_WORKFLOW_GUIDE_v1.0.md 읽기
4. 현재 마일스톤 파악
5. 작업지시서 번호 순서대로 작업 진행

이미 완료된 작업은 다시 구현하지 않는다.
다음 작업은 54번부터 진행한다.

---

# 1. 워크플로우 원칙 (반드시 준수)

- claude.ai: 검토 + 작업지시서 md 파일 생성 (다운로드 제공)
- Claude Code (VS Code): md 파일 읽고 실행 + git push
- 인수인계 md 파일 작성도 동일하게 claude.ai에서 생성 → Claude Code에서 저장/push
- claude.ai에서 직접 파일을 실행하거나 git 명령을 수행하지 않음

## 파일 정리 자동화 (Claude Code 프롬프트 템플릿)

```
아래 작업을 순서대로 실행해줘.

## 1. SESSION_HANDOVER 백업
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md 파일을
C:\Obsidian\Dooly\00_System\HANDOVER_HISTORY\{다음번호}_SESSION_HANDOVER_v{버전}.md 로 복사

## 2. SESSION_HANDOVER 업데이트
C:\Users\USER\Downloads\02_SESSION_HANDOVER_v{버전}.md 파일을
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md 로 덮어쓰기

## 3. 사용자 가이드 이동
C:\Users\USER\Downloads\13_Dooly_User_Guide_v2.0.md 파일을
C:\Obsidian\Dooly\01_Project\13_Dooly_User_Guide_v2.0.md 로 이동

## 4. 작업지시서 이동 (있는 경우)
C:\Users\USER\Downloads\{작업지시서파일명}.md 파일을
C:\Obsidian\Dooly\03_Claude_Code\{작업지시서파일명}.md 로 이동

## 5. git push
cd C:\Obsidian\Dooly
git add .
git commit -m "docs: SESSION_HANDOVER v14.0 업데이트 + 사용자 가이드 v2.0"
git push
```

---

# 2. v2.0 확정 구조 (완료)

```
GitHub (코드 저장 + 버전 관리)
    ↓ git push → 자동 배포
Vercel (PWA 서빙 + API 프록시) ✅ 완료
    ├── Gemini API 프록시 (docs/api/gemini.js)
    └── Supabase Task 프록시 (docs/api/tasks.js)
        ↓
Supabase (Task DB — 기기간 동기화) ✅ Task #53 완료
```

| 도구 | 역할 | 상태 |
|------|------|------|
| GitHub | 코드 저장 + 버전 관리 | ✅ 운영 중 |
| Vercel | PWA 서빙 + API 프록시 | ✅ 완료 |
| Gemini API | Dooly AI 답변 | ✅ 완료 |
| Supabase | Task DB (기기간 동기화) | ✅ Task #53 완료 |

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
| 52 | PWA 아이콘 + Gemini 출처 + 말풍선 | 33f3cd3 | ✅ |
| 52-E | SW v3 + Gemini 태그 UI + 줄바꿈 | d98cfb9 | ✅ |
| 52-F | manifest 링크 태그 추가 | 9a24c94 | ✅ |
| 추가 | PWA 이름 Dooly 통일 | e31eebb | ✅ |
| 52-G~I | 출처 번호 수정 시도 → 롤백 | - | ⚠️ 롤백 |
| 52-Y | 52-E 복원 (출처 태그 정상화) | 35f7576 | ✅ |
| 53 | Supabase Task 동기화 | 82d593a | ✅ |

---

# 4. 배포 URL

| 환경 | URL | 상태 |
|------|------|------|
| GitHub | https://github.com/2passion/Dooly.git | ✅ |
| Vercel (메인) | https://dooly-eight.vercel.app | ✅ |
| Dooly 챗봇 | https://dooly-eight.vercel.app/06_Dooly_v1.html | ✅ |
| Task 관리 | https://dooly-eight.vercel.app/02_Task_v1.html | ✅ |
| Task API | https://dooly-eight.vercel.app/api/tasks | ✅ |

---

# 5. 시행착오 기록 (전체 누적)

## 에러 1~16: v12.0 참고

## 에러 17: manifest.json 링크 태그 누락
- 증상: PWA 홈 화면 아이콘이 V + Chrome 로고로 표시
- 원인: 06_Dooly_v1.html head에 link rel="manifest" 태그 없음
- 해결: manifest 링크 태그 3줄 추가
- 교훈: HTML 신규 생성 시 반드시 manifest 링크 태그 포함

## 에러 18: Gemini SOP 출처 번호 미표시
- 증상: SOP 태그에 번호 없이 카테고리명만 표시
- 현재: 52-E 상태(35f7576)에서 FAQ Q1/SOP 10 형식으로 정상 표시
- 교훈: buildDataContext() 수정하면 성능 저하 발생 → 건드리지 말 것

## 에러 19: 삼성 One UI PWA 아이콘 캐시
- 증상: 서버 아이콘 교체 후에도 홈 화면 아이콘 변경 안 됨
- 원인: manifest 링크 태그 누락이 진짜 원인
- 해결: manifest 링크 태그 추가 후 재설치

## 에러 20: 출처 번호 수정 시도 → 성능 저하 (52-G~52-I)
- 시도: buildDataContext() 수정으로 출처 번호 표시 변경
- 결과: 속도 10초, 답변 잘림 발생
- 해결: 52-E(d98cfb9) 상태로 롤백
- 교훈: buildDataContext()는 절대 수정하지 말 것
- 재시도 방법: 시스템 프롬프트 지시문만 수정할 것

## 에러 21: 52-F 롤백 시 출처 태그 사라짐
- 원인: 출처 태그 기능은 52-E에서 추가됨 (52-F는 manifest만)
- 해결: 52-E(d98cfb9)로 롤백하여 출처 태그 복원

---

# 6. 현재 Dooly UI 상태

| 기능 | 상태 | 비고 |
|------|------|------|
| Gemini AI 답변 | ✅ | gemini-2.5-flash |
| 출처 태그 | ✅ | FAQ Q1, SOP 10 형식 |
| 말풍선 텍스트 | ✅ | 흰색 |
| 답변 줄바꿈 | ✅ | \n → br |
| PWA 아이콘 | ✅ | 공룡 아이콘 |
| PWA 이름 | ✅ | Dooly |
| Task 동기화 | ✅ | Supabase 연동 |

---

# 7. 다음 작업 계획

| 번호 | 작업 | 우선순위 | 상태 |
|------|------|---------|------|
| 54 | GitHub Pages 최신버전 업데이트 | 낮음 | 🔜 대기 |
| 55 | Task 화면 — 담당자 필터 동기화 확인 | 보통 | 🔜 대기 |
| 56 | Supabase Auth 추가 (조교별 로그인) | 낮음 | 🔜 대기 |

---

# 8. 환경 정보

| 항목 | 내용 |
|------|------|
| GitHub | https://github.com/2passion/Dooly.git |
| Vercel URL | https://dooly-eight.vercel.app |
| AI API | Gemini API (gemini-2.5-flash) |
| Gemini 크레딧 | ₩25,000 충전 완료 |
| Gemini 프록시 | docs/api/gemini.js |
| Task 프록시 | docs/api/tasks.js |
| Supabase URL | https://yvtpenbltyeqmbbwhpmj.supabase.co |
| Supabase 프로젝트 | dooly (Northeast Asia — Tokyo) |
| 서비스워커 버전 | king-assistant-v3 |
| 최신 커밋 | 82d593a |
| HANDOVER_HISTORY | 17번까지 완료 → 다음은 18번 |

---

# 9. 핵심 주의사항 (다음 세션 필독)

## buildDataContext() 수정 금지
- 수정 시 속도 저하 + 답변 잘림 발생 확인됨
- 출처 표시 개선 시 시스템 프롬프트 지시문만 수정할 것

## 안정 커밋
- 현재 안정 상태: 82d593a (Task #53 완료)
- 문제 발생 시 35f7576으로 롤백 (출처 태그 포함 안정 상태)

## Vercel Root Directory
- 반드시 `docs` (공백 없이)

## Supabase RLS
- 현재 비활성화 상태
- Auth 추가 시 활성화 필요

---

# 10. 새 세션 시작 방법

1. 02_SESSION_HANDOVER.md 첨부
2. 04_PROJECT_GUIDE_v1.0.md 첨부
3. 05_WORKFLOW_GUIDE_v1.0.md 첨부
4. 아래 메시지 입력:

```
첨부한 파일을 읽고 프로젝트 현황을 파악해줘.
다음 작업은 Task #54부터야.
```
