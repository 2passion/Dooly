# 05_WORKFLOW_GUIDE_v1.0.md
# King Assistant OS v1.0
# 프로젝트 운영 워크플로우 가이드

Version: v1.0
Date: 2026-06-27

---

# 1. 역할 분담 (분업 원칙)

```
검토 · 설계 · 인수인계 작성
→ claude.ai (이 채팅창)

실행 · 파일 생성 · git push
→ VS Code 안의 Claude Code 입력창
```

| 작업 종류 | 도구 |
|---|---|
| 폴더 구조 검토 | claude.ai |
| 파일명 규칙 검토 | claude.ai |
| 작업지시서 md 작성 | claude.ai |
| 인수인계 md 작성 | claude.ai |
| 파일 생성 / 수정 | Claude Code |
| git add / commit / push | Claude Code |
| 서버 실행 / 테스트 | Claude Code or 직접 실행 |

---

# 2. 백업 체계 (이중 백업)

```
오프라인 백업         온라인 백업
Obsidian             GitHub
C:\Obsidian\Dooly\   https://github.com/2passion/Dooly.git
       │                        │
       └──────────┬─────────────┘
                  │
           작업 완료마다
           git add .
           git commit
           git push
```

## 백업 타이밍

| 시점 | 백업 방법 |
|---|---|
| 작업지시서 1개 완료 후 | git commit + push |
| 세션 종료 전 | git commit + push + SESSION_HANDOVER 업데이트 |
| 인수인계 파일 생성 후 | git commit + push |

## 절대 push 없이 종료 금지

```
세션 종료 전 반드시:
① git add .
② git commit -m "작업 내용 요약"
③ git push
```

---

# 3. 파일 구조 및 이름 규칙

## 폴더 구조

```
C:\Obsidian\Dooly\
├── 00_System\              ← 시스템 문서 (검토 대상)
│   ├── 01_PROJECT_MASTER.md
│   ├── 02_SESSION_HANDOVER.md    ← 항상 최신 버전
│   ├── 03_DEVELOPMENT_RULE_v1.0.md
│   ├── 04_PROJECT_GUIDE_v1.0.md
│   ├── 05_WORKFLOW_GUIDE_v1.0.md ← 이 파일
│   └── HANDOVER_HISTORY\         ← 이전 인수인계 보관
│       ├── 05_SESSION_HANDOVER_v1.md
│       ├── 06_SESSION_HANDOVER_v2.md
│       ├── 07_SESSION_HANDOVER_v3.md
│       └── 08_SESSION_HANDOVER_v4.0.md
├── 01_Project\             ← 설계 문서
├── 02_Claude_Project\      ← Claude Project 지침
├── 03_Claude_Code\         ← 작업지시서 (번호 순서)
├── 04_Runtime\             ← HTML 실행 파일
├── 05_RAG\                 ← RAG 서버
└── 99_Archive\             ← 아카이브 (git 제외)
```

## 파일명 규칙

| 폴더 | 규칙 | 예시 |
|---|---|---|
| 00_System | `{번호}_{이름}_v{버전}.md` | `03_DEVELOPMENT_RULE_v1.0.md` |
| 03_Claude_Code | `{번호}_Order_{기능}_v{버전}.md` | `34_Order_PWA_Manifest_v1.0.md` |
| 04_Runtime | `{번호}_{화면명}_v{버전}.html` | `02_Task_v1.html` |
| HANDOVER_HISTORY | `{번호}_SESSION_HANDOVER_v{버전}.md` | `08_SESSION_HANDOVER_v4.0.md` |

## 버전 표기 규칙

```
✅ 올바른 표기: v1.0 (점 사용)
❌ 잘못된 표기: v1_0 (언더스코어 사용)
```

---

# 4. 인수인계 파일 관리 방법

## 구조 원칙

```
02_SESSION_HANDOVER.md
→ 항상 최신 버전 1개만 유지

HANDOVER_HISTORY\
→ 이전 버전들을 시간순으로 보관
→ 번호는 00_System 파일 번호에 이어서 증가
   (현재 04번까지 있으므로 05번부터 시작)
```

## 인수인계 파일 업데이트 순서

```
① 현재 02_SESSION_HANDOVER.md 내용을
   HANDOVER_HISTORY\ 에 복사 (번호 증가)

② 02_SESSION_HANDOVER.md 를
   새로운 인수인계 내용으로 덮어쓰기

③ git add . → commit → push
```

## HANDOVER_HISTORY 번호 현황

| 파일 | 내용 |
|---|---|
| 05_SESSION_HANDOVER_v1.md | Phase 6 완료 직후 |
| 06_SESSION_HANDOVER_v2.md | 구조 개선 버전 |
| 07_SESSION_HANDOVER_v3.md | AI 인수인계 규칙 추가 |
| 08_SESSION_HANDOVER_v4.0.md | 최신 (다음 저장 시 생성) |
| 09_SESSION_HANDOVER_v5.0.md | ← 다음 세션 종료 시 생성 |

---

# 5. 채팅창이 길어질 때 인수인계 방법

## 기준

```
첨부 파일 80개 근접 OR 채팅창이 매우 길어졌을 때
→ 인수인계 작업 진행
```

## 인수인계 절차

### Step A — claude.ai 에서 (검토)

```
1. 현재 채팅창에서 아래 요청:
   "현재 작업 상태를 정리해서
    02_SESSION_HANDOVER 최신본을 작성해줘"

2. 작성된 내용을 확인하고 수정
```

### Step B — Claude Code 에서 (실행)

```
Claude Code 입력창에 아래 붙여넣기:

C:\Obsidian\Dooly\00_System\HANDOVER_HISTORY\{번호}_SESSION_HANDOVER_v{버전}.md 파일을
현재 02_SESSION_HANDOVER.md 내용으로 생성해줘.

그리고 02_SESSION_HANDOVER.md 파일을
아래 내용으로 덮어써줘.

[새로운 인수인계 내용 붙여넣기]

완료 후:
git add .
git commit -m "docs: SESSION_HANDOVER v{버전} 업데이트"
git push
```

### Step C — 새 채팅창에서 이어서 진행

```
1. 새 채팅창 열기
2. 아래 파일 첨부:
   - 02_SESSION_HANDOVER.md (최신)
   - 04_PROJECT_GUIDE_v1.0.md
   - 05_WORKFLOW_GUIDE_v1.0.md (이 파일)
3. 아래 메시지 입력:
   "첨부한 파일을 읽고 프로젝트 현황을 파악해줘.
    다음 작업은 {번호}번부터 이어서 진행할거야."
```

---

# 6. 작업지시서 작성 → 실행 흐름

```
① claude.ai 에서
   → 폴더·파일명 규칙 검토
   → 작업지시서 md 초안 작성

② 작업지시서 파일 저장
   → C:\Obsidian\Dooly\03_Claude_Code\{번호}_Order_{기능}_v1.0.md

③ Claude Code 입력창에 입력
   → "C:\Obsidian\Dooly\03_Claude_Code\{파일명} 읽고 작업 시작해"

④ Claude Code 가 파일 읽고 자동 실행
   → 파일 생성 / 수정 / git push 까지 자동 진행

⑤ 완료 확인
   → http://localhost:8001/app 브라우저 확인
   → GitHub 커밋 확인
```

---

# 7. 새 세션 시작 체크리스트

```
□ 02_SESSION_HANDOVER.md 첨부
□ 04_PROJECT_GUIDE_v1.0.md 첨부
□ 05_WORKFLOW_GUIDE_v1.0.md 첨부 (이 파일)
□ "첨부 파일 읽고 현황 파악해줘" 입력
□ 다음 작업지시서 번호 확인
□ 서버 상태 확인 (자습실 PC 켜져 있는지)
```

---

# 8. 세션 종료 체크리스트

```
□ 현재 작업 완료 확인
□ git add . 실행
□ git commit -m "작업 내용" 실행
□ git push 실행
□ 02_SESSION_HANDOVER.md 업데이트
□ HANDOVER_HISTORY 파일 생성 (다음 번호로)
□ GitHub 에서 커밋 확인
```

---

# 9. 현재 진행 상태 요약

| 항목 | 현재 값 |
|---|---|
| 마지막 작업지시서 | 33번 완료 |
| 다음 작업지시서 | 34번 (PWA manifest) |
| 마지막 커밋 | a8257ab |
| 서버 포트 | 8001 |
| ngrok 도메인 | polymer-distinct-feminize.ngrok-free.dev |
| 인수인계 최신 버전 | v4.0 |
| HANDOVER_HISTORY 마지막 번호 | 08번 |
| 다음 HANDOVER 번호 | 09번 |

---

# END OF GUIDE
