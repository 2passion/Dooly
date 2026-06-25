# 14_Order_Home_v3.0.md
# King Assistant OS — 홈 화면 개편 + JSON 템플릿 기능

---

# 수정 대상
C:\Obsidian\Dooly\04_Runtime\index.html
C:\Obsidian\Dooly\04_Runtime\05_Notice_v1.html

---

# [수정 1] index.html — 홈 화면 전면 개편

## 변경 사항 요약
- 업무 현황 카드 클릭 시 02_Task_v1.html 이동
- 업무 섹션 삭제
- 공지 섹션을 05_Notice_v1.html과 동일한 데이터로 표시
  (아코디언 방식 그대로, 홈에서 바로 열림)
- Bottom Nav의 "공지" 탭은 유지 (index.html과 동일 데이터)

## 상세 구조

```
Header: King Assistant OS

인사말: 안녕하세요, 둘리(Dooly)입니다.

[업무 현황 카드] ← 전체 카드 클릭 시 02_Task_v1.html 이동
  대기중 N  진행중 N  완료 N
  cursor: pointer
  클릭 안내 텍스트: "탭하여 업무 관리로 이동" (작은 글씨, opacity 0.4)

[공지사항 섹션]
섹션 제목: "공지사항"
아코디언 방식으로 공지 목록 표시
(05_Notice_v1.html과 완전히 동일한 NOTICES 데이터 및 toggle 방식 사용)

Bottom Nav (기존 유지)
```

## 공지 데이터 (index.html에 하드코딩)

```javascript
var NOTICES = [
  {
    id: 1,
    title: '시스템 오픈 안내',
    date: '2026-06-25',
    body: 'King Assistant OS v1.0이 오픈되었습니다.\n\n이 시스템은 조교 업무 운영을 지원하기 위한 시스템입니다.\n\n주요 기능:\n- 업무 등록 및 상태 관리\n- SOP 검색\n- FAQ 검색\n- Dooly AI 질의응답\n\n사용 중 문의사항은 담당자에게 문의해 주세요.'
  },
  {
    id: 2,
    title: '조교 업무 매뉴얼 배포',
    date: '2026-06-25',
    body: '조교 업무 매뉴얼이 배포되었습니다.\n\n매뉴얼 내용:\n- 복테 관리 방법\n- 오답노트 관리 방법\n- 비품 관리 방법\n- 복사기 사용 방법\n\n모든 조교는 매뉴얼을 숙지하고 업무에 임해 주세요.\n\n문의사항은 원장에게 직접 문의해 주세요.'
  }
];
```

## 아코디언 스타일 (05_Notice_v1.html과 동일)

```css
.notice-item { background: #1c2333; border-radius: 12px; overflow: hidden; cursor: pointer; margin-bottom: 8px; }
.notice-header { padding: 16px; display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.notice-left { display: flex; flex-direction: column; gap: 5px; flex: 1; }
.notice-title { font-size: 15px; font-weight: 600; }
.notice-date { font-size: 12px; opacity: 0.5; }
.notice-arrow { font-size: 14px; opacity: 0.5; transition: transform 0.2s; }
.notice-item.open .notice-arrow { transform: rotate(180deg); }
.notice-detail { display: none; padding: 12px 16px 16px; font-size: 14px; line-height: 1.7; opacity: 0.85; border-top: 1px solid rgba(255,255,255,0.06); }
.notice-item.open .notice-detail { display: block; }
```

---

# [수정 2] 05_Notice_v1.html — JSON 업로드/다운로드 기능 추가

Header 아래, 공지 리스트 위에 아래 버튼 2개 추가:

```
[📥 JSON 다운로드]  [📤 JSON 업로드]
```

## 다운로드 기능
- 버튼 클릭 시 현재 NOTICES 배열을 JSON 파일로 저장
- 파일명: notice_template.json
- 형식:
```json
[
  {
    "id": 1,
    "title": "공지 제목",
    "date": "2026-06-25",
    "body": "공지 내용"
  }
]
```

## 업로드 기능
- 버튼 클릭 시 파일 선택창 열림 (.json 파일만)
- JSON 파싱 후 NOTICES 배열 교체
- localStorage에 'notices' 키로 저장
- 저장 후 화면 즉시 재렌더링
- 오류 시 alert("JSON 형식이 올바르지 않습니다.")

## 페이지 로드 시
- localStorage에 'notices'가 있으면 그 데이터 사용
- 없으면 하드코딩 데이터 사용

## 버튼 스타일
```css
.data-btn-row { display: flex; gap: 10px; margin-bottom: 16px; }
.btn-download { flex: 1; background: #1c2333; border: 1px solid rgba(77,163,255,0.3); color: #4da3ff; border-radius: 8px; font-size: 14px; padding: 10px; cursor: pointer; min-height: 44px; }
.btn-upload { flex: 1; background: #1c2333; border: 1px solid rgba(77,163,255,0.3); color: #4da3ff; border-radius: 8px; font-size: 14px; padding: 10px; cursor: pointer; min-height: 44px; }
```

---

# [수정 3] 03_SOP_v1.html — JSON 업로드/다운로드 기능 추가

검색창 위에 버튼 2개 추가:

```
[📥 JSON 다운로드]  [📤 JSON 업로드]
```

## 다운로드
- 파일명: sop_template.json
- 형식:
```json
[
  {
    "id": 1,
    "title": "SOP 제목",
    "category": "카테고리",
    "body": "내용 (줄바꿈은 \\n 사용)"
  }
]
```

## 업로드
- localStorage에 'sops' 키로 저장
- 로드 시 localStorage 우선 사용
- 오류 시 alert

---

# [수정 4] 04_FAQ_v1.html — JSON 업로드/다운로드 기능 추가

검색창 위에 버튼 2개 추가:

## 다운로드
- 파일명: faq_template.json
- 형식:
```json
[
  {
    "id": 1,
    "question": "질문 내용",
    "answer": "답변 내용"
  }
]
```

## 업로드
- localStorage에 'faqs' 키로 저장
- 로드 시 localStorage 우선 사용

---

# [수정 5] 02_Task_v1.html — JSON 업로드/다운로드 기능 추가

Header의 "+ 업무 추가" 버튼 옆에 아이콘 버튼 2개 추가:
- 📥 (다운로드)
- 📤 (업로드)

## 다운로드
- 파일명: task_template.json
- 현재 localStorage tasks 배열 그대로 저장

## 업로드
- localStorage 'tasks' 키 교체
- 즉시 재렌더링

---

# 공통 JSON 다운로드 함수 (각 파일에 개별 구현)

```javascript
function downloadJSON(data, filename) {
  var blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
```

## 공통 JSON 업로드 함수

```javascript
function uploadJSON(callback) {
  var input = document.createElement('input');
  input.type = 'file';
  input.accept = '.json';
  input.onchange = function(e) {
    var file = e.target.files[0];
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function(ev) {
      try {
        var data = JSON.parse(ev.target.result);
        callback(data);
      } catch(err) {
        alert('JSON 형식이 올바르지 않습니다.');
      }
    };
    reader.readAsText(file);
  };
  input.click();
}
```

---

# 작업 순서

1. index.html 수정 (업무 현황 클릭 이동 + 업무 섹션 삭제 + 공지 아코디언)
2. 05_Notice_v1.html JSON 기능 추가
3. 03_SOP_v1.html JSON 기능 추가
4. 04_FAQ_v1.html JSON 기능 추가
5. 02_Task_v1.html JSON 기능 추가

---

# 작업 완료 후

git add . && git commit -m "feat: home UI v3, JSON upload/download for all data pages" && git push
