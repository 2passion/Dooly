# AI 개발 프로젝트 표준 구조 v1.0

## 목표

Claude Code 채팅창이 길어지더라도 언제든지 
새로운 세션에서 작업을 이어갈 수 있도록 한다.

모든 결정사항, 작업지시, 결과물은 Obsidian Vault에 저장하며 
GitHub로 버전관리한다.

---

# 폴더 구조

{프로젝트명}/

├── archive/
│   ├── session_backup/
│   ├── release_backup/
│   └── rollback_point/
│
├── command/
│   ├── current_order.md
│   ├── next_order.md
│   └── completed_order/
│
├── dev/
│   ├── PROJECT_MASTER.md
│   ├── SYSTEM_PROMPT.md
│   ├── ARCHITECTURE.md
│   ├── CHANGELOG.md
│   └── SESSION_HANDOVER.md
│
├── log/
│   ├── work_log_2026-06.md
│   ├── error_log.md
│   └── decision_log.md
│
├── user/
│   ├── USER_GUIDE.md
│   ├── INSTALL.md
│   ├── FAQ.md
│   └── RELEASE_NOTE.md
│
├── src/
│
├── assets/
│
└── README.md

---

# 핵심 문서 설명

## PROJECT_MASTER.md

프로젝트의 최상위 문서

포함 내용

* 프로젝트 목적
* 주요 기능
* 현재 상태
* 개발 우선순위
* 향후 계획

Claude Code가 가장 먼저 읽는 문서

---

## SYSTEM_PROMPT.md

Claude Code 행동 규칙

예시

* 작업 전 반드시 PROJECT_MASTER 확인
* 작업 후 CHANGELOG 작성
* 작업 후 Git Commit 수행
* 작업 완료 후 SESSION_HANDOVER 갱신

---

## SESSION_HANDOVER.md

가장 중요한 문서

채팅창이 길어지면 반드시 갱신

포함 내용

### 현재 상태

현재 구현 완료 기능

### 작업 중

현재 진행 중 기능

### 다음 작업

다음 세션에서 해야 할 일

### 주의사항

절대 수정하면 안 되는 부분

---

## CHANGELOG.md

버전 변경 기록

예시

v1.3

* 학생 검색 기능 추가
* 버그 수정
* UI 개선

---

## decision_log.md

왜 그렇게 만들었는지 기록

예시

Firebase 대신 Supabase 채택

이유

* 학생 수 증가 대비
* 백업 용이

---

# Claude Code 세션 종료 프로세스

작업 완료

↓

CHANGELOG 업데이트

↓

SESSION_HANDOVER 업데이트

↓

Git Commit

↓

Git Push

↓

세션 종료

---

# Claude Code 새 세션 시작 프로세스

새 채팅창 생성

↓

PROJECT_MASTER.md 읽기

↓

SESSION_HANDOVER.md 읽기

↓

현재 작업 파악

↓

작업 시작

---

# Git Commit 규칙

feat: 기능 추가

fix: 버그 수정

docs: 문서 수정

refactor: 구조 개선

style: UI 수정

chore: 기타 작업

예시

feat: 복테 자동 생성 기능 추가

docs: 조교 매뉴얼 업데이트

fix: 학생 검색 오류 수정

---

# Obsidian 활용 원칙

Obsidian = 프로젝트 기억장치

GitHub = 버전관리

Claude Code = 작업자

PROJECT_MASTER.md = 프로젝트 뇌

SESSION_HANDOVER.md = 인수인계 노트
