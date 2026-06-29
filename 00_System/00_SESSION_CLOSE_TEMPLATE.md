# 00_SESSION_CLOSE_TEMPLATE.md
# 세션 종료 Claude Code 프롬프트 템플릿
# ※ 매 세션 종료 시 이 템플릿을 복사해서 사용

---

## 📌 사용법
1. 아래 프롬프트에서 {버전}, {다음번호} 부분만 수정
2. Claude Code 입력창에 붙여넣기

---

## ✅ 세션 종료 Claude Code 프롬프트

```
아래 작업을 순서대로 실행해줘.

## 1. SESSION_HANDOVER 백업
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md 파일을
C:\Obsidian\Dooly\00_System\HANDOVER_HISTORY\{다음번호}_SESSION_HANDOVER_v{버전}.md 로 복사

## 2. SESSION_HANDOVER 업데이트
C:\Users\USER\Downloads\02_SESSION_HANDOVER_v{버전}.md 파일을
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md 로 덮어쓰기

## 3. git push
cd C:\Obsidian\Dooly
git add .
git commit -m "docs: SESSION_HANDOVER v{버전} 업데이트"
git push
```

---

## ✅ 작업지시서 포함 시 추가 프롬프트

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
C:\Obsidian\Dooly\03_Claude_Code\{작업지시서파일명}.md 로 복사

## 4. git push
cd C:\Obsidian\Dooly
git add .
git commit -m "docs: SESSION_HANDOVER v{버전} 업데이트 + {작업지시서} 추가"
git push
```

---

## ✅ 오늘 (2026-06-29) 실제 입력값

| 항목 | 값 |
|------|-----|
| {버전} | 12.0 |
| {다음번호} | 17 |
| SESSION_HANDOVER 파일명 | 02_SESSION_HANDOVER_v12.0.md |

### 오늘 사용할 프롬프트 (바로 복사 가능)

```
아래 작업을 순서대로 실행해줘.

## 1. SESSION_HANDOVER 백업
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md 파일을
C:\Obsidian\Dooly\00_System\HANDOVER_HISTORY\17_SESSION_HANDOVER_v12.0.md 로 복사

## 2. SESSION_HANDOVER 업데이트
C:\Users\USER\Downloads\02_SESSION_HANDOVER_v12.0.md 파일을
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md 로 덮어쓰기

## 3. git push
cd C:\Obsidian\Dooly
git add .
git commit -m "docs: SESSION_HANDOVER v12.0 업데이트"
git push
```

---

## ✅ 새 세션 시작 체크리스트

```
□ 02_SESSION_HANDOVER.md 첨부
□ 04_PROJECT_GUIDE_v1.0.md 첨부
□ 05_WORKFLOW_GUIDE_v1.0.md 첨부
□ 아래 메시지 입력:

"첨부한 파일을 읽고 프로젝트 현황을 파악해줘.
다음 작업은 Task #53 Supabase Task 동기화야."
```

---

## END OF TEMPLATE
