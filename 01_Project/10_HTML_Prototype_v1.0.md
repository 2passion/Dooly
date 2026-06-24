# 📄 10_HTML_Prototype_v1.0.md (FULL FINAL)

````md id="htmlproto001"
# 10_HTML_Prototype_v1.0.md

# King Assistant OS v1.0
# HTML Prototype Specification

Version: v1.0  
Status: Prototype Phase  
Dependency: 09_UI_Wireframe_v1.0.md  
Target: Mobile First (PWA Ready)

---

# 1. 목적

본 문서는 King Assistant OS v1.0의 UI Wireframe을 기반으로
실제 동작 가능한 HTML 프로토타입을 생성하기 위한 설계 문서이다.

이 단계는 "디자인"이 아니라 "실사용 검증 단계"이다.

---

# 2. 핵심 목표

```text
1. 실제 클릭 가능한 UI 생성
2. 모바일에서 사용 가능
3. DB 없이 동작
4. 로컬 상태 기반 기능 구현
5. 사용자 흐름 검증
````

---

# 3. 기술 스택 (Prototype 단계)

```text
HTML5
CSS3
Vanilla JavaScript
LocalStorage (임시 데이터)
```

---

# 4. 구조 원칙

## 4.1 파일 구조

```text
01_Home_v1.html
02_Task_v1.html
03_SOP_v1.html
04_FAQ_v1.html
05_Notice_v1.html
06_Dooly_v1.html
```

---

## 4.2 설계 원칙

* 프레임워크 사용 금지
* React 금지
* DB 금지
* API 금지
* 완전 독립 실행

---

# 5. 전체 페이지 구조

```text
Home (index.html)
├─ 조교 홈
├─ 원장 홈
└─ 둘리 AI 홈
```

---

# 6. 공통 UI 구조

모든 페이지 동일 구조 사용

```text id="layout001"
┌────────────────────┐
│ Header             │
├────────────────────┤
│ Content Area       │
│                    │
├────────────────────┤
│ Bottom Navigation  │
└────────────────────┘
```

---

# 7. Bottom Navigation (공통)

```text id="nav001"
[Home] [업무] [SOP] [FAQ] [공지] [둘리]
```

* 모든 페이지 고정
* 클릭 시 페이지 이동 (location.href)

---

# 8. 페이지 정의

---

# 8.1 Home (index.html)

## 구조

```text id="home001"
안녕하세요 둘리입니다

[업무 요약]
- 진행중: 3
- 대기: 2

[빠른 실행]

[업무 보기]
[업무 보고]
[SOP 검색]
[FAQ 검색]
[공지사항]
[둘리 질문]
```

---

## 기능

* 버튼 클릭 시 페이지 이동
* 업무 데이터는 localStorage 사용

---

# 8.2 Task Page (02_Task_v1.html)

```text id="task001"
[업무 리스트]

- 제목
- 담당자
- 상태

[상태]
pending
in_progress
review
completed
hold
```

## 기능

* 업무 추가
* 상태 변경
* 삭제
* localStorage 저장

---

# 8.3 SOP Page (03_SOP_v1.html)

```text id="sop001"
[검색창]

[SOP 리스트]

- 업무 SOP
- 예외 SOP
- 비품 SOP
- 복테 SOP
- 오답노트 SOP
```

## 기능

* 검색 필터
* 리스트 클릭 상세보기

---

# 8.4 FAQ Page (04_FAQ_v1.html)

```text id="faq001"
[검색창]

[질문 리스트]

[답변 표시 영역]
```

## 기능

* 검색
* 클릭 시 답변 표시

---

# 8.5 Notice Page (05_Notice_v1.html)

```text id="notice001"
[공지 리스트]

- 제목
- 날짜

[상세 보기]
```

---

# 8.6 Dooly AI Page (06_Dooly_v1.html)

```text id="dooly001"
[채팅 UI]

--------------------------------
| 질문 입력창                 |
--------------------------------

[대화 영역]

User: 질문
Dooly: 답변
```

## 기능

* 입력 → 메시지 추가
* 답변은 mock response

---

# 9. JavaScript 규칙

---

## 9.1 데이터 구조 (LocalStorage)

```json id="data001"
{
  "tasks": [],
  "sop": [],
  "faq": [],
  "notice": []
}
```

---

## 9.2 Task 구조

```json id="task001"
{
  "id": "T001",
  "title": "업무명",
  "assignee": "조교",
  "status": "pending",
  "created_at": "timestamp"
}
```

---

## 9.3 상태 변경 로직

```text id="state001"
pending → in_progress → review → completed
```

hold는 예외 상태

---

# 10. UI 동작 규칙

---

## 10.1 페이지 이동

```text id="navflow001"
onclick → location.href
```

---

## 10.2 데이터 저장

```text id="save001"
localStorage.setItem()
localStorage.getItem()
```

---

## 10.3 렌더링

```text id="render001"
DOM 직접 조작
innerHTML 사용
```

---

# 11. 모바일 최적화 규칙

---

## 11.1 기준

```text id="mobile001"
width: 360px ~ 430px
```

---

## 11.2 UI 원칙

* 버튼 크게
* 여백 충분
* 텍스트 중심
* 스크롤 최소화

---

# 12. UX Flow (핵심)

---

## 12.1 업무 흐름

```text id="flow001"
원장 → 업무 생성 → 조교 확인 → 진행 → 완료
```

---

## 12.2 검색 흐름

```text id="flow002"
사용자 → 검색 → 결과 → 상세
```

---

## 12.3 AI 흐름

```text id="flow003"
사용자 질문 → Dooly → Mock 답변
```

---

# 13. Claude Code 실행 기준

이 문서는 Claude Code에게 다음을 지시한다:

---

## 13.1 생성 대상

```text id="gen001"
index.html
02_Task_v1.html
03_SOP_v1.html
04_FAQ_v1.html
05_Notice_v1.html
06_Dooly_v1.html
```

---

## 13.2 생성 조건

* 완전 실행 가능한 HTML
* 외부 라이브러리 금지
* localStorage 사용
* 모바일 대응
* 단일 파일 구조

---

# 14. Prototype 성공 기준

```text id="success001"
1. 스마트폰에서 실행 가능
2. 클릭으로 전체 흐름 이동 가능
3. 업무 생성 가능
4. 상태 변경 가능
5. 데이터 유지됨 (localStorage)
```

---

# 15. 다음 단계

```text id="next001"
1. HTML Prototype 생성
2. 모바일 테스트
3. UI 개선 (v2)
4. PWA 변환
5. React 전환
6. DB 연결
```

---

# END OF DOCUMENT

````

---

# 🔥 핵심 정리

이 문서의 의미는 단 하나야:

```text
👉 이제 설계 끝
👉 이제 "진짜 개발 시작"
````

---

# 🚀 다음 단계 (중요)

이제 선택은 1개야:

## 👉 Claude Code로 바로 생성할 것

명령 예시:

```text
King Assistant OS v1.0

10_HTML_Prototype_v1.0.md 기준으로

다음 파일 생성:

- index.html
- 02_Task_v1.html
- 03_SOP_v1.html
- 04_FAQ_v1.html
- 05_Notice_v1.html
- 06_Dooly_v1.html
```
