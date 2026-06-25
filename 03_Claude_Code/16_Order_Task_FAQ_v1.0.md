# 16_Order_Task_FAQ_v1.0.md
# KING Assistant OS — FAQ 태그 + 업무관리 개편

---

# 수정 대상
C:\Obsidian\Dooly\04_Runtime\04_FAQ_v1.html
C:\Obsidian\Dooly\04_Runtime\02_Task_v1.html

---

# [수정 1] 04_FAQ_v1.html — 카테고리 태그 추가

## 카테고리 목록
['전체', '복사기', '복테', '오답노트', '비품', '제본기']

## 각 FAQ 항목에 category 필드 추가
기존 FAQS 배열에 category 추가:
```javascript
{ id: 1, question: '복사기가 종이를 먹었어요',         category: '복사기', answer: '...' },
{ id: 2, question: '학생이 복테를 못 찾겠어요',         category: '복테',   answer: '...' },
{ id: 3, question: '오답기록표에 끝이라고 적혀있어요',  category: '오답노트', answer: '...' },
{ id: 4, question: '연습장이 부족해요',                 category: '비품',   answer: '...' },
{ id: 5, question: 'ADF 스캔과 수동 스캔 차이가 뭐예요?', category: '복사기', answer: '...' },
{ id: 6, question: '제본링 사이즈는 어떻게 선택해요?',  category: '제본기', answer: '...' },
{ id: 7, question: '제본기 찌꺼기는 언제 비워요?',      category: '제본기', answer: '...' },
{ id: 8, question: '복테 보관함 배치 순서가 어떻게 돼요?', category: '복테', answer: '...' },
{ id: 9, question: '비품이 부족할 때 언제 보고해요?',   category: '비품',   answer: '...' },
{ id: 10, question: '이면지는 어디에 보관해요?',         category: '비품',   answer: '...' },
{ id: 11, question: '복테 완료 기준이 뭐예요?',          category: '복테',   answer: '...' },
{ id: 12, question: '연습장은 몇 권 유지해야 해요?',     category: '비품',   answer: '...' }
```

## 카테고리 필터 UI 추가 (SOP와 동일한 방식)
검색창 아래에 가로 스크롤 필터 칩 추가:
```
[전체] [복사기] [복테] [오답노트] [비품] [제본기]
```

CSS: SOP의 .filter-row, .filter-chip, .filter-chip.active 와 동일

## 필터 동작
- 카테고리 클릭 시 해당 카테고리만 표시
- 검색어 + 카테고리 동시 필터 적용
- 번호는 필터 결과 기준으로 재계산 (Q1, Q2, ...)

## 각 FAQ 카드에 카테고리 태그 표시
SOP의 .sop-cat 과 동일한 스타일로 질문 아래에 표시:
```css
.faq-cat {
  display: inline-block;
  background: rgba(77,163,255,0.15);
  color: #4da3ff;
  border-radius: 6px;
  font-size: 11px;
  padding: 2px 8px;
  margin-top: 4px;
}
```

---

# [수정 2] 02_Task_v1.html — 업무관리 전면 개편

## 2-1. 담당자 관리 (localStorage 연동)

담당자 목록을 localStorage 'assignees' 키로 관리:
```javascript
function loadAssignees() {
  return JSON.parse(localStorage.getItem('assignees') || '[]');
}
function saveAssignees(list) {
  localStorage.setItem('assignees', JSON.stringify(list));
}
```

## 2-2. 업무 추가 폼 개편

기존 폼에 아래 항목 추가/수정:

### 담당자 입력 방식 변경
직접 입력 + 등록된 담당자 클릭 선택 병행:
```
[담당자 입력창]
등록된 담당자: [조교A] [조교B] [조교C]  ← 클릭 시 입력창에 자동 입력
```

구현:
```html
<div class="form-group">
  <label>담당자</label>
  <input type="text" id="inputAssignee" placeholder="직접 입력 또는 아래서 선택">
  <div class="assignee-chips" id="assigneeChips"></div>
</div>
```

```javascript
function renderAssigneeChips() {
  var assignees = loadAssignees();
  var el = document.getElementById('assigneeChips');
  if (assignees.length === 0) { el.innerHTML = ''; return; }
  el.innerHTML = assignees.map(function(a) {
    return '<button class="assignee-chip" onclick="selectAssignee(\'' + escHtml(a) + '\')">' + escHtml(a) + '</button>';
  }).join('');
}

function selectAssignee(name) {
  document.getElementById('inputAssignee').value = name;
}
```

CSS:
```css
.assignee-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 8px;
}
.assignee-chip {
  background: rgba(77,163,255,0.15);
  border: 1px solid rgba(77,163,255,0.3);
  color: #4da3ff;
  border-radius: 16px;
  font-size: 12px;
  padding: 4px 12px;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}
```

### 업무 내용 텍스트 입력창 추가
우선순위 아래에 추가:
```html
<div class="form-group">
  <label>업무 내용 (선택)</label>
  <textarea id="inputContent" placeholder="업무 내용을 입력하세요..." rows="5"
    style="width:100%; background:#0b0f1a; border:1px solid rgba(77,163,255,0.3);
    border-radius:8px; color:#fff; font-size:14px; padding:10px 12px;
    outline:none; resize:none; font-family:Arial,sans-serif; line-height:1.5;
    min-height:100px;"></textarea>
</div>
```

localStorage task 구조에 content 필드 추가:
```json
{
  "id": "T001",
  "title": "업무명",
  "assignee": "조교명",
  "content": "업무 내용",
  "status": "pending",
  "priority": "normal",
  "created_at": "2026-06-25"
}
```

## 2-3. 담당자/우선순위 태그 필터 추가

JSON 다운로드/업로드 버튼 아래에 필터 태그 영역 추가:

### 우선순위 필터
```
[전체] [즉시] [오늘] [보통]
```

### 담당자 필터
localStorage 'assignees' 에서 읽어서 동적 생성:
```
[전체] [조교A] [조교B] [조교C]
```

두 필터를 동시에 적용하여 목록 렌더링

CSS (SOP filter-chip과 동일):
```css
.filter-section { margin-bottom: 12px; }
.filter-label { font-size: 11px; opacity: 0.5; margin-bottom: 6px; }
.filter-row { display: flex; gap: 6px; overflow-x: auto; padding-bottom: 4px;
  scrollbar-width: none; -webkit-overflow-scrolling: touch; }
.filter-row::-webkit-scrollbar { display: none; }
.filter-chip { background: #1c2333; border: 1px solid rgba(77,163,255,0.2);
  border-radius: 20px; color: rgba(255,255,255,0.6); font-size: 12px;
  padding: 5px 12px; cursor: pointer; white-space: nowrap; flex-shrink: 0;
  -webkit-tap-highlight-color: transparent; }
.filter-chip.active { background: #4da3ff; border-color: #4da3ff;
  color: #0b0f1a; font-weight: 700; }
```

## 2-4. 카드에 체크박스 추가

카드 제목 왼쪽에 체크박스 추가:
```html
<input type="checkbox" class="task-check" data-id="{id}"
  onclick="event.stopPropagation(); toggleCheck('{id}')">
```

task 구조에 checked 필드 추가 (boolean):
```javascript
function toggleCheck(id) {
  var tasks = loadTasks().map(function(t) {
    if (t.id === id) t.checked = !t.checked;
    return t;
  });
  saveTasks(tasks);
  renderTasks();
}
```

체크된 카드는 제목에 취소선 표시:
```css
.task-check:checked + .task-title { text-decoration: line-through; opacity: 0.5; }
```

## 2-5. 카드 클릭 시 인라인 수정 모드

카드를 길게 누르면(또는 수정 버튼 클릭) 수정 모드 전환:
카드 하단에 수정 버튼 추가:
```
[상태뱃지] [수정] [삭제]
```

수정 버튼 클릭 시 해당 카드가 수정 폼으로 전환:
```
[제목 입력창] (기존값 채워진 상태)
[담당자 입력창] + 등록된 담당자 칩
[우선순위 선택]
[업무 내용 textarea]
[저장] [취소]
```

구현:
```javascript
function editTask(id, e) {
  e.stopPropagation();
  editingId = id;
  renderTasks();
}

// renderTasks에서 editingId === t.id 이면 카드 대신 수정 폼 렌더링
```

수정 저장 시 기존 task 업데이트 후 editingId = null, renderTasks()

---

# 작업 순서
1. 04_FAQ_v1.html — category 필드 추가 + 필터 칩 + 태그 표시
2. 02_Task_v1.html — 담당자 칩 + 업무내용 textarea + 필터 태그 + 체크박스 + 수정 기능

---

# 작업 완료 후
git add . && git commit -m "feat: FAQ category filter, task overhaul with edit/filter/checkbox" && git push
