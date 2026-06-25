# SESSION_HANDOVER.md

작성일 : 2026-06-25

---

# 현재 상태

King Assistant OS v1.0

AI 비서 : 둘리(Dooly)

현재 단계 :

HTML Prototype Phase (Phase 0)

---

# 완료 작업

* 프로젝트 비전 정의
* MVP 범위 확정
* 역할 구조 정의
* SOP 구조 정리
* FAQ 구조 정리
* 문서 체계 정리
* Claude Project 구조 확정
* Claude Code 운영 방식 정리
* Implementation Plan 작성 완료
* UI Wireframe v1.0 완료
* HTML Prototype v1.0 생성 완료 (2026-06-25)
  - index.html (홈 + 달력)
  - 02_Task_v1.html (업무 관리)
  - 03_SOP_v1.html (SOP 검색)
  - 04_FAQ_v1.html (FAQ)
  - 05_Notice_v1.html (공지사항)
  - 06_Dooly_v1.html (둘리 AI 채팅)
  - 07_Settings_v1.html (설정: 담당자/초기화)

---

# 생성 파일 위치

```
C:\Obsidian\Dooly\04_Runtime\
├── index.html
├── 02_Task_v1.html
├── 03_SOP_v1.html
├── 04_FAQ_v1.html
├── 05_Notice_v1.html
├── 06_Dooly_v1.html
└── 07_Settings_v1.html
```

---

# 진행 중 작업

* HTML Prototype 모바일 테스트 및 UI 검증

---

# 다음 작업

1. 모바일 브라우저 테스트 (360px 기준)
2. UI 개선 필요 사항 반영 (v2)
3. Task DB 상세 설계
4. Knowledge DB 상세 설계
5. PWA 전환 준비

---

# HTML Prototype 기능 요약

| 파일 | 기능 |
|------|------|
| index.html | 홈, 업무 현황 카드, 빠른 실행 6개 |
| 02_Task_v1.html | 업무 추가/조회/상태변경/홀드/삭제, localStorage |
| 03_SOP_v1.html | 카테고리 필터, 실시간 검색, 상세 보기 |
| 04_FAQ_v1.html | 실시간 검색, 아코디언 토글 |
| 05_Notice_v1.html | 공지 목록, 상세 보기 |
| 06_Dooly_v1.html | 채팅 UI, Mock 응답 (복사기/복테/연습장) |

---

# 주의사항

현재 MVP 범위는 확정 상태이다.

다음 항목은 추가하지 않는다.

* 신규 기능
* 신규 SOP
* 신규 FAQ
* 신규 메뉴

---

# 참고 문서

08_King_Assistant_OS_v1.0_Implementation_Plan.md

---

## PWA 전환 시 추가 구현 항목

### DB 폴더 경로 선택 기능
- File System Access API 사용
- 구현 방법:
  ```javascript
  const dirHandle = await window.showDirectoryPicker();
  localStorage.setItem('dbDirHandle', JSON.stringify(dirHandle));
  ```
- 폴더 선택 → IndexedDB에 FileSystemDirectoryHandle 저장
- 이후 다운로드/업로드 시 해당 폴더 자동 사용
- 설정 탭에 "폴더 선택" 버튼 추가 (현재는 안내 텍스트만 표시)
- 관련 파일: 07_Settings_v1.html DB 폴더 경로 섹션

PROJECT_MASTER.md
