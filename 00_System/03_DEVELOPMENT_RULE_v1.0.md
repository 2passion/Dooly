좋아. 이건 앞으로 프로젝트 전체 “규칙 엔진”이 되는 문서라서, 
**바로 Obsidian에 넣고 그대로 기준으로 써도 되는 완성본**으로 줄게.

---

# 📄 DEVELOPMENT_RULE_v1.0.md (완성본)

````md
# DEVELOPMENT_RULE_v1.0.md

# King Assistant OS v1.0
# Development Operating Rules (Dooly Project)

Version: v1.0  
Status: Active Rule Set  
Owner: Dooly System  

---

# 1. 목적 (Purpose)

본 문서는 King Assistant OS v1.0 개발 과정에서

- 파일 구조
- 버전 관리
- 작업 지시 방식
- 코드 생성 방식
- Git 운영 방식
- 문서 관리 방식

을 통합적으로 정의하는 **개발 운영 규칙(Development OS)** 이다.

---

# 2. 핵심 원칙 (Core Principles)

## 2.1 UI First Principle

```text
DB 설계보다 UI 검증이 우선이다
````

* 사용자는 UI를 통해 시스템을 이해한다
* 기능은 UI 사용 흐름에서 정의된다
* DB는 UI 확정 이후 결정한다

---

## 2.2 Prototype First Principle

```text
React 이전에 HTML Prototype을 먼저 만든다
```

순서:

```text
UI Wireframe
↓
HTML Prototype
↓
PWA
↓
React + Vite
↓
DB 연결
```

---

## 2.3 Real Usage First Principle

```text
문서보다 실제 클릭 가능한 화면이 우선이다
```

* 설계보다 사용 경험이 중요
* 실제 모바일 테스트 기준으로 판단

---

## 2.4 Version Control First Principle

```text
모든 변경은 반드시 버전으로 기록한다
```

* 파일명에 v1, v2, v3 적용
* 코드 수정도 버전 단위로 관리
* “즉석 수정” 금지

---

# 3. 파일 네이밍 규칙 (File Naming Rule)

## 3.1 기본 구조

```text
{번호}_{프로젝트명}_{기능명}_v{버전}.md
```

---

## 3.2 예시

```text
01_King_Assistant_OS_Overview_v1.0.md
09_UI_Wireframe_v1.0.md
10_HTML_Prototype_v1.0.md
```

---

## 3.3 HTML 파일 규칙

```text
{번호}_{화면명}_v{버전}.html
```

예:

```text
01_Home_v1.html
02_Home_v2.html
03_Home_v3.html
```

---

## 3.4 Claude Code 작업지시서

```text
{번호}_Order_{기능}_v{버전}.md
```

예:

```text
01_Order_Home_v1.0.md
02_Order_Task_v1.0.md
03_Order_SOP_v1.0.md
```

---

# 4. 버전 규칙 (Version Rule)

## 4.1 의미

```text
v1.0 = 최초 구조 완성
v1.1 = 기능 개선
v1.2 = UI 개선
v2.0 = 구조 변경
```

---

## 4.2 절대 규칙

```text
버전 없이 수정 금지
```

---

## 4.3 변경 기준

* UI 변경 → v 증가
* 기능 변경 → v 증가
* 구조 변경 → major version 변경 (v2.0)

---

# 5. 개발 흐름 (Development Flow)

## 5.1 전체 흐름

```text
UI Wireframe
↓
HTML Prototype
↓
실사용 테스트 (Mobile First)
↓
UI 수정 반복 (v2, v3)
↓
PWA 적용
↓
React 전환
↓
DB 연결
↓
운영 시스템 완성
```

---

## 5.2 UI 개발 흐름

```text
Wireframe 작성
↓
HTML 생성
↓
모바일 테스트
↓
수정
↓
버전 증가
```

---

## 5.3 기능 추가 흐름

```text
기능 정의
↓
HTML 반영
↓
테스트
↓
수정
↓
문서 반영
```

---

# 6. Claude Code 작업 규칙

## 6.1 입력 방식

Claude Code는 반드시 아래 문서를 기반으로 작업한다:

```text
09_UI_Wireframe_v1.0.md
10_HTML_Prototype_v1.0.md
각 Order 문서
```

---

## 6.2 작업 단위

```text
1 작업 = 1 파일 생성 또는 수정
```

---

## 6.3 금지사항

```text
- 전체 코드 일괄 수정 금지
- 설명 없이 코드 생성 금지
- 구조 변경 없이 기능 추가 금지
```

---

## 6.4 권장 방식

```text
작은 단위 작업
→ 테스트
→ 수정
→ 반복
```

---

# 7. Git 규칙

## 7.1 브랜치

```text
main (단일 브랜치)
```

---

## 7.2 Commit 규칙

```text
feat: 기능 추가
fix: 버그 수정
docs: 문서 수정
refactor: 구조 개선
chore: 기타 작업
```

---

## 7.3 Commit 예시

```text
feat: home screen UI created

fix: task status update bug

docs: update UI wireframe
```

---

## 7.4 Push 규칙

```text
작업 완료 즉시 push
세션 종료 전 반드시 push
```

---

# 8. 문서 관리 규칙

## 8.1 역할 분리

```text
PROJECT_MASTER.md
→ 전체 상태 요약

SESSION_HANDOVER.md
→ 현재 작업 상태

IMPLEMENTATION_PLAN.md
→ 설계 기준서

UI_WIREFRAME.md
→ 화면 설계

HTML_Prototype
→ 실제 화면
```

---

## 8.2 금지사항

```text
문서에 기능 추가 금지
설계 변경 즉시 반영 금지
모든 변경은 버전으로 기록
```

---

# 9. 개발 단계 정의

## Phase 0 (UI Prototype)

```text
HTML 기반 화면 생성
모바일 테스트
UX 검증
```

---

## Phase 1 (Core System)

```text
Task System
업무 등록
업무 조회
상태 변경
```

---

## Phase 2 (Knowledge System)

```text
SOP 검색
FAQ 검색
공지사항
```

---

## Phase 3 (AI Assistant)

```text
둘리(Dooly) 연결
질의응답
검색 기반 응답
```

---

## Phase 4 (Logging System)

```text
로그 기록
변경 이력 관리
행동 추적
```

---

## Phase 5 (Integration)

```text
GitHub 자동화
배포 시스템
PWA 완성
```

---

# 10. UI 개발 원칙

## 10.1 Mobile First

```text
모바일 기준으로 설계
```

---

## 10.2 One Hand Rule

```text
한 손으로 모든 기능 접근 가능
```

---

## 10.3 Minimal UI

```text
최소 클릭 구조
```

---

## 10.4 Real Usage Priority

```text
예쁜 UI보다 빠른 사용이 우선
```

---

# 11. 시스템 철학

```text
King Assistant OS는 “앱”이 아니라

조교 운영 시스템이다

그리고 Dooly는

그 시스템을 사용하는 AI 운영자이다
```

---

# 12. 최종 선언

```text
모든 개발은 이 규칙을 기준으로 수행한다.

규칙보다 빠른 개발은 존재하지 않는다.

규칙이 시스템이다.
```

````

---

# 🔥 이 문서의 의미 (핵심 한 줄)

이건 단순한 개발 규칙이 아니라:

```text
👉 Dooly 프로젝트의 "운영체제(OS 커널)"
````

이다.

---

원하면 다음 단계로:

👉 `09_UI_Wireframe_v1.0.md` 바로 설계
👉 또는 `Home 화면 HTML v1` 바로 생성

이제부터는 진짜 개발 단계로 들어갈 수 있다.
