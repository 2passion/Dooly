# 20_Order_UI_Fix_v1.0.md
# KING Assistant OS — UI 수정 3가지

---

# 수정 대상
C:\Obsidian\Dooly\04_Runtime\02_Task_v1.html
C:\Obsidian\Dooly\04_Runtime\04_FAQ_v1.html
C:\Obsidian\Dooly\04_Runtime\07_Settings_v1.html

---

# 작업 방식
HTML 구조/디자인은 최소한으로 건드린다.
각 파일별 수정 범위를 정확히 지정하여 변경한다.

---

# [수정 1] 02_Task_v1.html — 체크박스 제거 + 업무진행상황 필터 추가

## 1-1. 체크박스 제거
- CSS에서 `.task-check` 관련 스타일 제거
- HTML 렌더링에서 `<input type="checkbox" class="task-check" ...>` 제거
- JS에서 `toggleCheck` 함수 제거
- task 객체에서 `checked: false` 초기값 제거
- `t.checked` 관련 코드 제거 (task-title 에서 `.checked` 클래스 적용 부분 포함)

## 1-2. 업무진행상황 필터 태그 추가
우선순위 필터와 담당자 필터 사이에 업무진행상황 필터 추가:

```html
<div class="filter-section" style="margin-bottom:8px;">
  <div class="filter-label">업무진행상황</div>
  <div class="filter-row" id="statusFilter"></div>
</div>
```

JS에서 다음 변수 추가:
```javascript
var activeStatus = '전체';
```

renderFilters() 함수에 statusFilter 렌더링 추가:
```javascript
var statuses = ['전체', '대기', '진행중', '완료'];
document.getElementById('statusFilter').innerHTML = statuses.map(function(s) {
  return '<button class="filter-chip' + (s === activeStatus ? ' active' : '') +
         '" onclick="setStatusFilter(\'' + s + '\')">' + s + '</button>';
}).join('');
```

setStatusFilter 함수 추가:
```javascript
function setStatusFilter(s) { activeStatus = s; renderFilters(); renderTasks(); }
```

renderTasks()의 filtered 조건에 status 필터 추가:
```javascript
var STATUS_MAP = { '대기': 'pending', '진행중': 'in_progress', '완료': 'completed' };

var filtered = tasks.filter(function(t) {
  var matchP = activePriority === '전체' || t.priority === PRIORITY_MAP[activePriority];
  var matchA = activeAssignee === '전체' || t.assignee === activeAssignee;
  var matchS = activeStatus === '전체' || t.status === STATUS_MAP[activeStatus];
  return matchP && matchA && matchS;
});
```

---

# [수정 2] 04_FAQ_v1.html — FAQ 카드에 카테고리 태그 표시 + 필터 연동 수정

## 2-1. FAQ 카드에 카테고리 태그 표시
현재 FAQS 배열에 category 필드가 있지만 화면에 표시되지 않는 문제.
(SOP처럼 카드 제목 아래에 카테고리 태그가 표시되어야 함)

faq-question div 안의 faq-q-main에 카테고리 배지 추가:
렌더링 HTML에서 아래와 같이 카테고리 태그를 추가한다:

```javascript
'    <div class="faq-q-main">',
'      <span class="faq-q-text"><span class="faq-num">Q' + (index + 1) + '.</span>' + escHtml(f.question) + '</span>',
'      <span class="faq-cat">' + escHtml(f.category || '') + '</span>',
'    </div>',
```

CSS에 faq-cat 스타일이 없으면 아래를 추가:
```css
.faq-cat {
  display: inline-block;
  background: rgba(77,163,255,0.15);
  color: #4da3ff;
  border-radius: 6px;
  font-size: 11px;
  padding: 2px 8px;
  align-self: flex-start;
}
```

## 2-2. CATEGORIES 배열 확인 및 필터 연동 수정
현재 FAQ 파일에 CATEGORIES 배열이 올바르게 있는지 확인한다.
CATEGORIES = ['전체', '복테', '오답노트', '채점', '비품', '제본기', '복사기', '파일관리', '학생관리', '루틴']

FAQS 배열의 각 항목에 category 필드가 실제로 있는지 확인한다.
19번 작업에서 추가된 id 13~22 항목들에 category 필드가 누락되었을 수 있다.
누락된 항목에 category를 추가한다:
- id 13: category: '복테'
- id 14: category: '채점'
- id 15: category: '채점'
- id 16: category: '채점'
- id 17: category: '오답노트'
- id 18: category: '파일관리'
- id 19: category: '파일관리'
- id 20: category: '학생관리'
- id 21: category: '학생관리'
- id 22: category: '루틴'

필터 렌더링 함수 initFilters()가 올바르게 호출되는지 확인한다.
render() 함수에서 category 필터가 올바르게 적용되는지 확인한다:
```javascript
var matchCat = activeCategory === '전체' || f.category === activeCategory;
```

---

# [수정 3] 07_Settings_v1.html — 담당자 이름 클릭 시 수정 가능하게

## 3-1. 담당자 수정 기능 추가
현재: 담당자 이름 표시 + 삭제 버튼만 있음
변경: 담당자 이름 클릭 → 아래에 수정 UI 펼쳐짐 (이름 변경 + 메모 입력 5줄)

### CSS 추가
```css
.assignee-item { cursor: pointer; flex-direction: column; gap: 0; }
.assignee-item-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 12px 0;
}
.assignee-item-body {
  display: none;
  padding: 8px 0 12px 0;
  border-top: 1px solid rgba(255,255,255,0.06);
  width: 100%;
}
.assignee-item.open .assignee-item-body { display: block; }

.edit-name-input {
  width: 100%;
  background: #0b0f1a;
  border: 1px solid rgba(77,163,255,0.3);
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
  padding: 8px 12px;
  outline: none;
  margin-bottom: 8px;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
}
.edit-memo-input {
  width: 100%;
  background: #0b0f1a;
  border: 1px solid rgba(77,163,255,0.3);
  border-radius: 8px;
  color: #fff;
  font-size: 13px;
  padding: 8px 12px;
  outline: none;
  resize: none;
  height: 100px;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
  line-height: 1.5;
  margin-bottom: 8px;
}
.edit-action-row {
  display: flex;
  gap: 8px;
}
.btn-save-assignee {
  flex: 1;
  background: #4da3ff;
  color: #0b0f1a;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 700;
  padding: 8px;
  cursor: pointer;
  min-height: 36px;
}
.btn-delete-assignee {
  background: rgba(255,80,80,0.12);
  border: 1px solid rgba(255,80,80,0.25);
  color: #ff5050;
  border-radius: 8px;
  font-size: 13px;
  padding: 8px 16px;
  cursor: pointer;
  min-height: 36px;
}
```

### JS 수정
localStorage의 assignees 키를 문자열 배열 대신 객체 배열로 마이그레이션:
```javascript
// 기존 ['조교A', '조교B'] 형태를 [{name:'조교A', memo:''}, ...] 로 마이그레이션
function loadAssignees() {
  var raw = JSON.parse(localStorage.getItem('assignees') || '[]');
  // 마이그레이션: 문자열이면 객체로 변환
  return raw.map(function(a) {
    if (typeof a === 'string') return { name: a, memo: '' };
    return a;
  });
}
function saveAssignees(list) {
  localStorage.setItem('assignees', JSON.stringify(list));
}
```

### renderAssignees() 수정
```javascript
function renderAssignees() {
  var list = loadAssignees();
  var el = document.getElementById('assigneeList');
  if (list.length === 0) {
    el.innerHTML = '<p class="empty-msg">등록된 담당자가 없습니다.</p>';
    return;
  }
  el.innerHTML = list.map(function(a, i) {
    return [
      '<div class="assignee-item" id="aitem_' + i + '">',
      '  <div class="assignee-item-header" onclick="toggleAssigneeEdit(' + i + ')">',
      '    <span class="assignee-name">' + escHtml(a.name) + '</span>',
      '    <span style="font-size:12px;opacity:0.4;">✏️ 클릭하여 수정</span>',
      '  </div>',
      '  <div class="assignee-item-body">',
      '    <input type="text" class="edit-name-input" id="editName_' + i + '" value="' + escAttr(a.name) + '" placeholder="이름 변경" onclick="event.stopPropagation()">',
      '    <textarea class="edit-memo-input" id="editMemo_' + i + '" placeholder="메모 (5줄)" onclick="event.stopPropagation()">' + escHtml(a.memo || '') + '</textarea>',
      '    <div class="edit-action-row">',
      '      <button class="btn-save-assignee" onclick="saveAssigneeEdit(' + i + ')">저장</button>',
      '      <button class="btn-delete-assignee" onclick="deleteAssignee(' + i + ')">삭제</button>',
      '    </div>',
      '  </div>',
      '</div>'
    ].join('');
  }).join('');
}
```

### toggleAssigneeEdit 함수 추가
```javascript
function toggleAssigneeEdit(index) {
  var item = document.getElementById('aitem_' + index);
  if (item) item.classList.toggle('open');
}
```

### saveAssigneeEdit 함수 추가
```javascript
function saveAssigneeEdit(index) {
  var name = document.getElementById('editName_' + index).value.trim();
  var memo = document.getElementById('editMemo_' + index).value;
  if (!name) { alert('이름을 입력해 주세요.'); return; }
  var list = loadAssignees();
  if (index >= 0 && index < list.length) {
    list[index].name = name;
    list[index].memo = memo;
    saveAssignees(list);
    renderAssignees();
  }
}
```

### deleteAssignee 함수 수정 (index 기반으로 변경)
```javascript
function deleteAssignee(index) {
  var list = loadAssignees();
  if (!confirm(list[index].name + '을(를) 삭제하시겠습니까?')) return;
  list.splice(index, 1);
  saveAssignees(list);
  renderAssignees();
}
```

### addAssignee 함수 수정 (객체로 추가)
```javascript
function addAssignee() {
  var name = document.getElementById('inputAssigneeName').value.trim();
  if (!name) { alert('이름을 입력해 주세요.'); return; }
  var list = loadAssignees();
  if (list.some(function(a) { return a.name === name; })) {
    alert('이미 등록된 담당자입니다.'); return;
  }
  list.push({ name: name, memo: '' });
  saveAssignees(list);
  document.getElementById('inputAssigneeName').value = '';
  renderAssignees();
}
```

### 02_Task_v1.html의 loadAssignees / addAssigneeIfNew 함수도 수정
02_Task_v1.html에서 담당자 칩을 렌더링할 때 객체 배열을 처리하도록 수정:

```javascript
// loadAssignees는 이름 문자열 배열로 반환하는 헬퍼로 수정
function loadAssigneeNames() {
  var raw = JSON.parse(localStorage.getItem('assignees') || '[]');
  return raw.map(function(a) {
    return typeof a === 'string' ? a : a.name;
  });
}
```

02_Task_v1.html 내에서 `loadAssignees()` 를 호출하는 모든 곳을 `loadAssigneeNames()` 로 변경한다.
단, `saveAssignees` 를 호출할 때는 기존 형식(객체 배열)을 유지해야 하므로:

```javascript
function addAssigneeIfNew(name) {
  if (!name || name === '미지정') return;
  var raw = JSON.parse(localStorage.getItem('assignees') || '[]');
  var names = raw.map(function(a) { return typeof a === 'string' ? a : a.name; });
  if (names.indexOf(name) === -1) {
    raw.push({ name: name, memo: '' });
    localStorage.setItem('assignees', JSON.stringify(raw));
  }
}
```

---

# 작업 완료 후

git add . && git commit -m "fix: task checkbox remove+status filter, FAQ category tag+filter, settings assignee edit" && git push
