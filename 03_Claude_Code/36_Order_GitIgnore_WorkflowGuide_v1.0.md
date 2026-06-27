# 36_Order_GitIgnore_v1.0.md
# King Assistant OS v1.0
# Claude Code 작업지시서

Version: v1.0
Date: 2026-06-27

---

# 작업 시작 전 필수 확인

아래 파일을 순서대로 읽어라.

```
C:\Obsidian\Dooly\00_System\01_PROJECT_MASTER.md
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md
C:\Obsidian\Dooly\00_System\05_WORKFLOW_GUIDE_v1.0.md
```

---

# 작업 목표

.gitignore 항목 추가 (보안 + 불필요 파일 제외)

※ 05_WORKFLOW_GUIDE_v1.0.md 는 34번 작업 중 이미 git push 완료됨 → 별도 작업 불필요

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

기존 내용 아래에 아래 항목을 추가한다.
(기존 3줄은 절대 삭제하지 않는다)

```
# Windows 시스템 파일
Thumbs.db
desktop.ini

# Python 캐시
*.pyc
*.pyo

# ngrok 설정 (authtoken 보안)
ngrok.yml
ngrok.yaml
```

## 최종 .gitignore 전체 내용

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

# ngrok 설정 (authtoken 보안)
ngrok.yml
ngrok.yaml
```

## 완료 확인

```
✅ 기존 3개 항목 유지됨
✅ 신규 6개 항목 추가됨 (Thumbs.db, desktop.ini, *.pyc, *.pyo, ngrok.yml, ngrok.yaml)
```

---

# STEP 2 — 커밋 및 push

## 실행 명령어

```
cd C:\Obsidian\Dooly

git add .gitignore
git commit -m "chore: update .gitignore - add pyc, ngrok, Windows system files"
git push
```

## 완료 확인

```
✅ git push 완료
✅ GitHub 에서 .gitignore 커밋 확인
```

---

# 전체 작업 완료 조건

```
✅ STEP 1 완료 (.gitignore 업데이트 - 기존 유지 + 신규 추가)
✅ STEP 2 완료 (git push 완료)
```

---

# 작업지시서 번호 현황

| 번호 | 내용 | 상태 |
|---|---|---|
| 34 | 파일명 수정 + 인수인계 정리 + PWA manifest | ✅ 완료 |
| 35 | 초안 (폐기) | ❌ 사용 안 함 |
| 36 | .gitignore 업데이트 | 이 파일 |
| 37 | PWA service-worker.js + 아이콘 파일 추가 | 다음 작업 |

---

# 다음 작업

37_Order_PWA_ServiceWorker_v1.0.md
→ service-worker.js 생성 + 아이콘 파일 추가 (192px, 512px)

---

# END OF ORDER
