# 02_SESSION_HANDOVER.md v13.0

작성일: 2026-06-30
세션: 2026-06-30 (주간)
프로젝트 버전: King Assistant OS v2.0
현재 마일스톤: Task #52 전체 완료 + 출처 태그 안정화

---

# 0. AI 인수인계 규칙

새 세션의 AI는 반드시 다음 순서로 시작한다.

1. 이 파일 (02_SESSION_HANDOVER.md) 읽기
2. 04_PROJECT_GUIDE_v1.0.md 읽기
3. 05_WORKFLOW_GUIDE_v1.0.md 읽기
4. 현재 마일스톤 파악
5. 작업지시서 번호 순서대로 작업 진행

이미 완료된 작업은 다시 구현하지 않는다.
다음 작업은 53번부터 진행한다.

---

# 1. 워크플로우 원칙 (반드시 준수)

- claude.ai: 검토 + 작업지시서 md 파일 생성 (다운로드 제공)
- Claude Code (VS Code): md 파일 읽고 실행 + git push
- 인수인계 md 파일 작성도 동일하게 claude.ai에서 생성 → Claude Code에서 저장/push
- claude.ai에서 직접 파일을 실행하거나 git 명령을 수행하지 않음

## 작업지시서 파일 정리 자동화 (Claude Code 프롬프트 템플릿)

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
Supabase → Task 동기화 (Task #53 예정)
```

| 도구 | 역할 | 상태 |
|------|------|------|
| GitHub | 코드 저장 + 버전 관리 | ✅ 운영 중 |
| Vercel | PWA 서빙 + Gemini 프록시 | ✅ 완료 |
| Gemini API | Dooly AI 답변 | ✅ 완료 |
| Supabase | Task DB (기기간 동기화) | 🔜 53번 |

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
| 52-G | Gemini 출처 번호 수정 시도 | ed8f884 | ⚠️ 롤백됨 |
| 52-H | maxOutputTokens 수정 시도 | 8f6eccf | ⚠️ 롤백됨 |
| 52-I | Gemini 응답 파싱 변경 시도 | 341aa1a | ⚠️ 롤백됨 |
| 52-X | 52-F 롤백 | 5281c6e | ✅ |
| 52-Y | 52-E 롤백 → 출처 태그 복원 | 35f7576 | ✅ |

---

# 4. 배포 URL

| 환경 | URL | 상태 |
|------|------|------|
| GitHub 저장소 | https://github.com/2passion/Dooly.git | ✅ |
| Vercel (메인) | https://dooly-eight.vercel.app | ✅ 운영 중 |
| Dooly 챗봇 | https://dooly-eight.vercel.app/06_Dooly_v1.html | ✅ |

---

# 5. 시행착오 기록 (신규 추가분)

## 에러 20: 출처 번호 수정 시도 → 성능 저하 (52-G~52-I)
- 시도: Gemini 출처를 "FAQ Q: 제목" → "FAQ Q1" 번호만 표시로 변경
- 방법: buildDataContext() 수정 + parseGeminiSources() 교체
- 결과: 속도 10초, 답변 잘림 발생
- 원인 추정: buildDataContext() 수정으로 컨텍스트 구조 변경 → Gemini 혼란
- 해결: 52-E(d98cfb9) 상태로 롤백
- 교훈: buildDataContext()는 건드리지 말 것. 출처 번호 재시도 시 시스템 프롬프트만 수정

## 에러 21: 52-F로 롤백했더니 출처 태그 사라짐
- 원인: 출처 태그 기능은 52-E에서 추가된 것 (52-F는 manifest 태그만 추가)
- 해결: 52-E(d98cfb9)로 롤백하여 출처 태그 복원
- 결과: FAQ Q1/Q5, SOP 10/SOP 21 태그 정상 표시 ✅

---

# 6. 현재 Dooly UI 상태

| 기능 | 상태 | 비고 |
|------|------|------|
| Gemini AI 답변 | ✅ | gemini-2.5-flash |
| 출처 태그 표시 | ✅ | FAQ Q1, SOP 10 형식 |
| 말풍선 텍스트 | ✅ | 흰색 텍스트 |
| 답변 줄바꿈 | ✅ | \n → <br> |
| PWA 아이콘 | ✅ | 공룡 아이콘 |
| PWA 이름 | ✅ | Dooly |
| manifest 링크 태그 | ✅ | 06_Dooly_v1.html |

---

# 7. 다음 작업 계획

| 번호 | 작업 | 우선순위 | 상태 |
|------|------|---------|------|
| **53** | **Supabase Task 동기화** | **높음** | **🔜 다음** |
| 54 | GitHub Pages 최신버전 업데이트 | 낮음 | 🔜 대기 |

---

# 8. 환경 정보

| 항목 | 내용 |
|------|------|
| GitHub 저장소 | https://github.com/2passion/Dooly.git |
| Vercel URL | https://dooly-eight.vercel.app |
| AI API | Gemini API (gemini-2.5-flash) |
| Gemini 크레딧 | ₩25,000 충전 완료 |
| Gemini 프록시 경로 | docs/api/gemini.js |
| 서비스워커 버전 | king-assistant-v3 |
| 최신 커밋 | 35f7576 |

---

# 9. 핵심 주의사항 (다음 세션 필독)

## buildDataContext() 수정 금지
- Gemini에게 전달하는 컨텍스트 구조를 변경하면 속도 저하 + 답변 잘림 발생
- 출처 번호 표시 개선 시 **시스템 프롬프트 지시문만** 수정할 것

## 롤백 기준 커밋
- 현재 안정 상태: 35f7576 (52-E 복원)
- 문제 발생 시 위 커밋으로 롤백

---

# 10. 새 세션 시작 방법

1. 02_SESSION_HANDOVER.md 첨부
2. 04_PROJECT_GUIDE_v1.0.md 첨부
3. 05_WORKFLOW_GUIDE_v1.0.md 첨부
4. 아래 메시지 입력:

```
첨부한 파일을 읽고 프로젝트 현황을 파악해줘.
다음 작업은 Task #53 Supabase Task 동기화야.
```
