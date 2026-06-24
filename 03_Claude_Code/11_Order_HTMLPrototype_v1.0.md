# 11_Order_HTMLPrototype_v1.0.md
# King Assistant OS v1.0
# Claude Code 작업지시서

Version: v1.0
Date: 2026-06-25

---

# 작업 시작 전 필수 확인

아래 파일을 순서대로 읽어라.

```
C:\Obsidian\Dooly\00_System\01_PROJECT_MASTER.md
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md
C:\Obsidian\Dooly\00_System\03_DEVELOPMENT_RULE_v1.0.md
C:\Obsidian\Dooly\01_Project\09_UI_Wireframe_v1.0.md
C:\Obsidian\Dooly\01_Project\10_HTML_Prototype_v1.0.md
```

---

# 작업 목표

King Assistant OS v1.0 HTML Prototype 전체 생성.

10_HTML_Prototype_v1.0.md 기준으로 아래 파일 6개를 생성한다.

---

# 생성 파일 목록

```
C:\Obsidian\Dooly\04_Runtime\index.html
C:\Obsidian\Dooly\04_Runtime\02_Task_v1.html
C:\Obsidian\Dooly\04_Runtime\03_SOP_v1.html
C:\Obsidian\Dooly\04_Runtime\04_FAQ_v1.html
C:\Obsidian\Dooly\04_Runtime\05_Notice_v1.html
C:\Obsidian\Dooly\04_Runtime\06_Dooly_v1.html
```

---

# 공통 기술 조건

- HTML5 + CSS3 + Vanilla JavaScript 만 사용
- 외부 라이브러리 금지 (CDN, npm 전부 금지)
- React 금지
- DB 금지
- API 금지
- localStorage로 데이터 유지
- 단일 파일 구조 (HTML 1개에 CSS + JS 전부 포함)
- 모바일 기준: width 360px ~ 430px

---

# 공통 UI 구조 (모든 파일 동일 적용)

```
┌────────────────────┐
│ Header             │  ← 페이지 제목 고정
├────────────────────┤
│ Content Area       │  ← 스크롤 가능
│                    │
├────────────────────┤
│ Bottom Navigation  │  ← 항상 하단 고정
└────────────────────┘
```

---

# Bottom Navigation (모든 파일 동일)

```
[홈] [업무] [SOP] [FAQ] [공지] [둘리]
```

- 모든 페이지에 동일하게 고정
- 클릭 시 location.href로 이동
- 현재 페이지 아이콘/텍스트 강조 표시

이동 경로:
```
홈   → index.html
업무 → 02_Task_v1.html
SOP  → 03_SOP_v1.html
FAQ  → 04_FAQ_v1.html
공지 → 05_Notice_v1.html
둘리 → 06_Dooly_v1.html
```

---

# 디자인 기준

- 배경색: #0b0f1a (다크 계열)
- 텍스트: #ffffff
- 강조색: #4da3ff (파란 계열)
- 버튼: 충분한 크기 (최소 height 48px)
- 여백: 넉넉하게
- 폰트: 시스템 기본 (Arial, sans-serif)
- 카드 배경: #1c2333
- 보조 텍스트: opacity 0.6

---

# 파일별 상세 지시

---

## [1] index.html — 홈 화면

### 구조

```
Header: "King Assistant OS"

[인사말]
안녕하세요, 둘리(Dooly)입니다.

[업무 현황 카드]
진행중: N건
대기중: N건
(localStorage에서 읽어서 표시)

[빠른 실행 버튼 6개, 2열 그리드]
업무 보기   | 업무 보고
SOP 검색   | FAQ 검색
공지사항   | 둘리 질문

Bottom Nav
```

### 기능
- 각 버튼 클릭 시 해당 페이지로 이동
- 업무 현황은 localStorage의 tasks 배열에서 상태별 count 계산

---

## [2] 02_Task_v1.html — 업무 관리

### 구조

```
Header: "업무 관리"

[업무 추가 버튼] → 클릭 시 입력 폼 표시

[업무 리스트]
┌─────────────────────┐
│ 업무 제목           │
│ 담당자 | 상태 뱃지  │
└─────────────────────┘
(카드 형태, 클릭 시 상태 변경 가능)

Bottom Nav
```

### 업무 추가 폼 (버튼 클릭 시 표시)
```
업무 제목: [입력]
담당자:   [입력]
우선순위: [선택] low / normal / high / urgent
[저장] [취소]
```

### 상태 뱃지 색상
```
pending     → 회색
in_progress → 파란색
review      → 노란색
completed   → 초록색
hold        → 빨간색
```

### 상태 변경
- 카드 클릭 시 상태 순환
- pending → in_progress → review → completed → pending
- hold는 별도 버튼으로 설정

### localStorage 구조
```json
{
  "tasks": [
    {
      "id": "T001",
      "title": "업무명",
      "assignee": "조교명",
      "status": "pending",
      "priority": "normal",
      "created_at": "2026-06-25"
    }
  ]
}
```

---

## [3] 03_SOP_v1.html — SOP 검색

### 구조

```
Header: "SOP"

[검색창]

[카테고리 필터]
전체 | 업무 | 예외 | 비품 | 복테 | 오답노트

[SOP 리스트]
┌─────────────────────┐
│ 제목                │
│ 카테고리 태그       │
└─────────────────────┘

[상세 보기 영역]
(클릭 시 하단에 내용 표시)

Bottom Nav
```

### 초기 데이터 (하드코딩)
```
복테 관리 SOP (카테고리: 복테)
오답노트 관리 SOP (카테고리: 오답노트)
비품 관리 SOP (카테고리: 비품)
연습장 관리 SOP (카테고리: 비품)
복사기 관리 SOP (카테고리: 업무)
```

### 기능
- 검색어 입력 시 실시간 필터
- 카테고리 클릭 시 필터
- 항목 클릭 시 상세 내용 표시

---

## [4] 04_FAQ_v1.html — FAQ

### 구조

```
Header: "FAQ"

[검색창]

[FAQ 리스트]
┌─────────────────────┐
│ Q. 질문 내용        │
└─────────────────────┘

[답변 영역]
A. 답변 내용
(클릭 시 펼쳐짐 / 아코디언 방식)

Bottom Nav
```

### 초기 데이터 (하드코딩)
```
Q: 복사기가 종이를 먹었어요
Q: 학생이 복테를 못 찾겠어요
Q: 오답기록표에 끝이라고 적혀있어요
Q: 연습장이 부족해요
```

(답변은 "확인이 필요합니다. 담당자에게 문의하세요." 로 임시 처리)

### 기능
- 검색 실시간 필터
- 클릭 시 답변 토글 (아코디언)

---

## [5] 05_Notice_v1.html — 공지사항

### 구조

```
Header: "공지사항"

[공지 리스트]
┌─────────────────────┐
│ 제목                │
│ 날짜                │
└─────────────────────┘

[상세 보기]
(클릭 시 내용 표시)

Bottom Nav
```

### 초기 데이터 (하드코딩)
```
공지1: 시스템 오픈 안내 (2026-06-25)
공지2: 조교 업무 매뉴얼 배포 (2026-06-25)
```

---

## [6] 06_Dooly_v1.html — 둘리 AI 채팅

### 구조

```
Header: "둘리 (Dooly)"

[대화 영역]
(스크롤 가능, 최신 메시지가 아래)

Dooly: 안녕하세요! 무엇이든 질문하세요.

User: 질문 내용
Dooly: 답변 내용

[입력창 고정 영역]
[질문을 입력하세요...] [전송]

Bottom Nav
```

### 기능
- 입력 후 전송 클릭 또는 Enter → 메시지 추가
- Dooly 답변은 Mock Response (아래 규칙 적용)
- 입력창은 항상 하단 고정

### Mock Response 규칙
```
입력에 "복사기" 포함 → "복사기 오류 SOP를 확인하세요."
입력에 "복테" 포함   → "복테 관리 SOP를 확인하세요."
입력에 "연습장" 포함 → "연습장 관리 SOP를 확인하세요."
그 외               → "확인이 필요합니다. SOP 또는 FAQ를 검색해보세요."
```

---

# 작업 순서

```
1. index.html 생성 및 확인
2. 02_Task_v1.html 생성 및 확인
3. 03_SOP_v1.html 생성 및 확인
4. 04_FAQ_v1.html 생성 및 확인
5. 05_Notice_v1.html 생성 및 확인
6. 06_Dooly_v1.html 생성 및 확인
7. 전체 연결 확인 (Bottom Nav 이동 테스트)
```

파일 1개 완성 후 다음으로 넘어간다.
한 번에 전체 생성 금지.

---

# 작업 완료 조건

```
✅ 파일 6개 전부 생성됨
✅ 모바일 360px 기준 깨짐 없음
✅ Bottom Nav 전체 이동 가능
✅ Task localStorage 저장/조회 동작
✅ SOP/FAQ 검색 필터 동작
✅ Dooly Mock 응답 동작
```

---

# 세션 종료 전 필수

```
1. SESSION_HANDOVER.md 업데이트
2. git add .
3. git commit -m "feat: HTML prototype v1 generated"
4. git push
```

---

# END OF ORDER
