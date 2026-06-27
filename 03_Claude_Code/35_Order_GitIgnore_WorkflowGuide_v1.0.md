# 35_Order_GitIgnore_WorkflowGuide_v1.0.md
# King Assistant OS v1.0
# Claude Code 작업지시서

Version: v1.0
Date: 2026-06-27

---

# 작업 시작 전 필수 확인

아래 파일을 순서대로 읽어라.

```
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md
C:\Obsidian\Dooly\00_System\05_WORKFLOW_GUIDE_v1.0.md
```

---

# 작업 목표

1. .gitignore 항목 추가 (보안 + 불필요 파일 제외)
2. 05_WORKFLOW_GUIDE_v1.0.md git 등록
3. 전체 커밋 및 push

작업은 반드시 아래 순서대로 진행한다.

---

# STEP 1 — .gitignore 업데이트

## 수정 대상 파일

```
C:\Obsidian\Dooly\.gitignore
```

## 현재 내용 (변경 금지)

```
99_Archive/
05_RAG/db/
05_RAG/__pycache__/
```

## 추가할 내용

아래 내용을 기존 내용 아래에 추가한다.

```
# Windows 시스템 파일
Thumbs.db
desktop.ini

# Python 캐시
*.pyc
*.pyo

# ngrok 설정 (토큰 보안)
ngrok.yml
```

## 최종 .gitignore 내용

```
99_Archive/
05_RAG/db/
05_RAG/__pycache__/

# Windows 시스템 파일
Thumbs.db
desktop.ini

# Python 캐시
*.pyc
*.pyo

# ngrok 설정 (토큰 보안)
ngrok.yml
```

## 완료 확인

```
✅ .gitignore 파일 내용 7개 항목 포함
✅ 기존 3개 항목 유지됨
✅ 신규 4개 항목 추가됨
```

---

# STEP 2 — 05_WORKFLOW_GUIDE_v1.0.md git 등록 확인

## 확인 사항

아래 파일이 존재하는지 확인한다.

```
C:\Obsidian\Dooly\00_System\05_WORKFLOW_GUIDE_v1.0.md
```

존재하지 않으면 아래 내용으로 생성한다.

```
파일 내용:
C:\Obsidian\Dooly\00_System\05_WORKFLOW_GUIDE_v1.0.md 가 없는 경우,
claude.ai 채팅창에서 받은 05_WORKFLOW_GUIDE_v1.0.md 내용을 그대로 생성한다.
```

존재하면 그대로 진행한다.

## 완료 확인

```
✅ 00_System\05_WORKFLOW_GUIDE_v1.0.md 존재 확인
```

---

# STEP 3 — 전체 커밋 및 push

## 실행 명령어

```
cd C:\Obsidian\Dooly

git add .
git commit -m "chore: update .gitignore + add WORKFLOW_GUIDE v1.0"
git push
```

## 완료 확인

```
✅ git push 완료
✅ GitHub 에서 커밋 확인
```

---

# 전체 작업 완료 조건

```
✅ STEP 1 완료 (.gitignore 업데이트)
✅ STEP 2 완료 (WORKFLOW_GUIDE 존재 확인)
✅ STEP 3 완료 (git push 완료)
```

---

# 다음 작업

36_Order_PWA_ServiceWorker_v1.0.md
→ service-worker.js 생성 + 아이콘 파일 추가 (192px, 512px)

---

# END OF ORDER
