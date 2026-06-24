# 08_King_Assistant_OS_v1.0_Implementation_Plan.md

---

# King Assistant OS v1.0 Implementation Plan

Version : v1.0
Status : Design Phase
AI Assistant : 둘리(Dooly)

---

# 1. 프로젝트 개요

## 1.1 프로젝트명

King Assistant OS v1.0

AI 비서

```text
둘리(Dooly)
```

---

## 1.2 프로젝트 목적

본 프로젝트는 학원 전체 운영 시스템이 아닌,

```text
조교 운영 시스템
```

구축을 목표로 한다.

원장이 반복적으로 수행하는 다음 업무를 표준화하고 자동화한다.

```text
조교 교육
업무 지시
업무 확인
업무 보고 확인
SOP 안내
FAQ 응답
공지 전달
```

이를 AI 비서 둘리(Dooly)가 지원하여 조교 운영 효율성을 향상시킨다.

---

# 2. MVP 범위

## 포함 기능

```text
업무 관리

SOP 검색

FAQ 검색

공지사항 조회

둘리 질의응답
```

---

## 제외 기능

```text
학생 관리

학부모 관리

성적 관리

출결 관리

수납 관리

통계 분석

권한 관리 고도화
```

위 기능은 v1.0 MVP 범위에서 제외한다.

---

# 3. 시스템 구조

```text
King Assistant OS v1.0

├─ 조교 운영
├─ 업무 관리
├─ SOP 관리
└─ 시스템 관리
```

---

## 3.1 조교 운영

```text
신규 조교 교육

인수인계

교육자료

업무 체크리스트
```

---

## 3.2 업무 관리

```text
업무 등록

업무 진행

업무 검토

업무 완료

운영 로그
```

---

## 3.3 SOP 관리

```text
업무 매뉴얼

FAQ

복습테스트 운영

오답노트 관리

비품 관리

예외상황 매뉴얼

공지사항
```

---

## 3.4 시스템 관리

```text
둘리(Dooly)

Claude Project

Claude Code

Obsidian

GitHub
```

---

# 4. 사용자 역할

## 원장

권한

```text
업무 등록

업무 수정

업무 승인

SOP 관리

FAQ 관리

공지 관리

로그 조회
```

---

## 조교

권한

```text
업무 조회

업무 수행

업무 보고

SOP 조회

FAQ 조회

공지 조회
```

---

## 둘리(Dooly)

역할

```text
업무 안내

SOP 검색

FAQ 검색

공지 검색

질의응답

운영 지원
```

---

# 5. 사용자 흐름(User Flow)

## 업무 등록

```text
원장

↓

업무 등록

↓

Task DB 저장

↓

조교 업무 목록 표시
```

---

## 업무 진행

```text
조교

↓

업무 확인

↓

진행중

↓

작업 수행

↓

검토중
```

---

## 업무 완료

```text
원장

↓

검토

↓

승인

↓

완료

↓

Log DB 기록
```

---

## SOP 검색

```text
검색어 입력

↓

Knowledge DB 검색

↓

결과 출력
```

---

## 둘리 질의응답

```text
질문 입력

↓

Knowledge DB 검색

↓

답변 생성

↓

출력
```

---

# 6. 화면 구조(UI Structure)

## 6.1 조교 화면

```text
안녕하세요.
둘리(Dooly)입니다.

[내 업무]

진행중 3건
대기 2건

① 업무 보기

② 업무 보고

③ SOP 검색

④ FAQ 검색

⑤ 공지사항
```

---

## 6.2 원장 화면

```text
① 업무 등록

② 업무 현황

③ SOP 관리

④ FAQ 관리

⑤ 공지 관리

⑥ 로그 조회
```

---

## 6.3 둘리 화면

```text
질문 입력

↓

Knowledge DB 검색

↓

답변 생성

↓

답변 출력
```

---

# 7. 데이터베이스 설계

초기 MVP는 아래 3개 DB만 사용한다.

```text
Task DB

Knowledge DB

Log DB
```

---

## 7.1 Task DB

```json
{
  "id": "",
  "title": "",
  "description": "",
  "assignee": "",
  "status": "",
  "priority": "",
  "created_by": "",
  "created_at": "",
  "updated_at": "",
  "completed_at": ""
}
```

### status

```text
pending
in_progress
review
completed
hold
```

### priority

```text
low
normal
high
urgent
```

---

## 7.2 Knowledge DB

```json
{
  "id": "",
  "type": "",
  "title": "",
  "content": "",
  "tags": [],
  "version": "",
  "updated_at": ""
}
```

### type

```text
sop

faq

notice

incident
```

---

## 7.3 Log DB

```json
{
  "id": "",
  "user": "",
  "action": "",
  "result": "",
  "created_at": ""
}
```

---

# 8. 문서 구조

```text
Dooly/

├─ 00_System
│  ├─ PROJECT_MASTER.md
│  ├─ SESSION_HANDOVER.md
│  └─ HANDOVER_HISTORY/
│
├─ 01_Project
│  ├─ 01_King_Assistant_OS_v1.0.md
│  ├─ 02_SOP_v1.0.md
│  ├─ 03_Exception_Manual_v1.0.md
│  ├─ 04_FAQ_v1.0.md
│  ├─ 06_Task_Management_v1.0.md
│  └─ 08_King_Assistant_OS_v1.0_Implementation_Plan.md
│
├─ 02_Claude_Project
│  └─ 05_Dooly_System_Prompt_v1.0.md
│
├─ 03_Claude_Code
│  └─ 07_Claude_Code_Operation_v1.0.md
│
└─ 99_Archive
```

---

# 9. GitHub 운영 규칙

## 브랜치 전략

초기 MVP는 단순 운영을 원칙으로 한다.

```text
main
```

단일 브랜치 사용.

---

## 커밋 규칙

```text
feat:
기능 추가

fix:
버그 수정

docs:
문서 수정

refactor:
구조 개선

chore:
기타 작업
```

예시

```text
feat: task management system

docs: update implementation plan

fix: task status update bug
```

---

## 백업 원칙

```text
작업 완료 후 Push

중요 변경 전 Commit

세션 종료 전 Push
```

---

# 10. 세션 인수인계 규칙

## PROJECT_MASTER.md

역할

```text
프로젝트의 단일 진실 공급원

현재 버전

현재 목표

현재 단계

핵심 문서

다음 작업
```

---

## SESSION_HANDOVER.md

역할

```text
현재 상태

완료 작업

진행 작업

다음 작업

주의사항
```

---

## HANDOVER_HISTORY

역할

```text
과거 인수인계 기록 보관
```

예시

```text
2026-06-25_v1.md

2026-06-28_v2.md

2026-07-01_v3.md
```

---

# 11. 개발 단계

## Phase 1

Task System

```text
업무 등록

업무 조회

업무 상태 변경
```

---

## Phase 2

Knowledge System

```text
SOP 검색

FAQ 검색

공지 검색
```

---

## Phase 3

Dooly Assistant

```text
검색 기반 질의응답

Knowledge DB 활용

답변 생성
```

---

## Phase 4

Log System

```text
로그 기록

로그 조회

변경 이력 관리
```

---

## Phase 5

GitHub Integration

```text
자동 백업

문서 자동화

배포 체계 정리
```

---

# 12. 기술 스택 (임시안)

현재 시점 기준 권장안

```text
Frontend
React + Vite

Database
Firebase

Storage
Firebase Storage

Version Control
GitHub

Documentation
Obsidian

AI
Claude Project
Claude Code
```

본 항목은 UI 설계 및 DB 상세 설계 완료 후 최종 확정한다.

---

# 13. 현재 프로젝트 상태

| 항목                |   진행률 |
| ----------------- | ----: |
| 프로젝트 비전           |  100% |
| MVP 범위            |  100% |
| 역할 정의             |  100% |
| 문서 체계             |   98% |
| Claude Project 구조 |   95% |
| Claude Code 운영    |   95% |
| 구현계획서             |  100% |
| UI 상세 설계          | 진행 예정 |
| DB 상세 설계          | 진행 예정 |
| 실제 개발             |    0% |

---

# 14. 다음 작업 우선순위

```text
1. UI Wireframe 설계

2. DB 상세 스키마 설계

3. 기술 스택 최종 확정

4. Claude Code 작업지시서 작성

5. MVP 개발 시작
```

---

# 최종 선언

King Assistant OS v1.0은 기획 단계를 종료하고 설계 확정 단계에 진입한다.

향후 논의는 신규 기능 추가보다

UI 설계

DB 상세 설계

개발 작업 분할

MVP 구현

에 집중한다.
