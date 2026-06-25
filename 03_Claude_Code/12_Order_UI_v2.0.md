# 12_Order_UI_v2.0.md
# King Assistant OS — UI 수정 작업지시서

---

# 수정 대상
C:\Obsidian\Dooly\04_Runtime\index.html
C:\Obsidian\Dooly\04_Runtime\02_Task_v1.html

---

# [수정 1] index.html — 홈 화면

## 업무 현황 카드
순서: 대기중(왼쪽) → 진행중(가운데) → 완료(오른쪽)
localStorage tasks 배열에서 각각 카운트:
- 대기중 = status === 'pending'
- 진행중 = status === 'in_progress'
- 완료   = status === 'completed'

## 빠른 실행 버튼 6개 전부 삭제

## 업무 현황 카드 아래에 "업무" 섹션 추가
- 섹션 제목: "업무"
- localStorage tasks 배열을 읽어서 카드로 표시
- 카드 구성: 제목 / 담당자 / 우선순위 신호등(urgent=🔴 today=🟡 normal=🟢)
- 카드 클릭 시 02_Task_v1.html 이동
- tasks가 없으면 "등록된 업무가 없습니다." 표시

## 업무 섹션 아래에 "공지" 섹션 추가
- 섹션 제목: "공지"
- 아래 공지 데이터를 하드코딩으로 표시
- 카드 구성: 제목 / 날짜
- 카드 클릭 시 05_Notice_v1.html 이동

공지 데이터:
```
{ title: '시스템 오픈 안내', date: '2026-06-25' }
{ title: '조교 업무 매뉴얼 배포', date: '2026-06-25' }
```

---

# [수정 2] 02_Task_v1.html — 업무 관리

## 상태 3단계로 축소
- pending(대기) → in_progress(진행중) → completed(완료)
- "review(검토)" 완전 삭제
- 상태 순환: pending → in_progress → completed → pending
- hold 기능 삭제 (홀드 버튼 제거)

## 상태 뱃지 색상
- pending    → 회색   "대기"
- in_progress → 파란색 "진행중"
- completed  → 초록색 "완료"

## 우선순위 3가지로 변경
- urgent / today / normal
- 기존 low, high, normal 삭제

## 우선순위 신호등 표시
카드 제목 오른쪽 끝에 배치:
- urgent → 빨간 원(●) + "urgent" (빨간색 텍스트)
- today  → 노란 원(●) + "today"  (노란색 텍스트)
- normal → 초록 원(●) + "normal" (초록색 텍스트)

신호등 스타일:
```
display: flex
align-items: center
gap: 4px
font-size: 12px
font-weight: 700
```
urgent 색상: #ff4444
today  색상: #ffcc00
normal 색상: #3cc864

## 업무 추가 폼 우선순위 선택
urgent / today / normal 3개만 표시
기본값: normal

## localStorage 데이터 구조 유지
```json
{
  "id": "T001",
  "title": "업무명",
  "assignee": "조교명",
  "status": "pending",
  "priority": "normal",
  "created_at": "2026-06-25"
}
```

---

# 작업 완료 후

git add . && git commit -m "feat: simplified home UI, task 3-step status, priority signal" && git push
