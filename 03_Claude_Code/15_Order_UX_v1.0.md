# 15_Order_UX_v1.0.md
# KING Assistant OS — UX 전체 수정 작업지시서

---

# 수정 대상
C:\Obsidian\Dooly\04_Runtime\index.html
C:\Obsidian\Dooly\04_Runtime\02_Task_v1.html
C:\Obsidian\Dooly\04_Runtime\03_SOP_v1.html
C:\Obsidian\Dooly\04_Runtime\04_FAQ_v1.html
C:\Obsidian\Dooly\04_Runtime\05_Notice_v1.html

---

# [수정 1] 전체 파일 — "King" → "KING" 텍스트 수정

모든 HTML 파일에서:
- <title>King Assistant OS</title> → <title>KING Assistant OS</title>
- header h1: "King Assistant OS" → "KING Assistant OS"
- body 내 "King Assistant OS" 전부 → "KING Assistant OS"

---

# [수정 2] 02_Task_v1.html — JSON 버튼 레이아웃 수정

현재: 헤더에 📥 📤 아이콘 버튼
변경: 헤더 아이콘 버튼 제거 → main 최상단에 SOP와 동일한 스타일로 배치

변경 후 구조:
```
Header: 업무 관리  |  + 업무 추가
─────────────────────────────
[📥 JSON 다운로드]  [📤 JSON 업로드]
─────────────────────────────
업무 추가 폼 (토글)
업무 리스트
```

버튼 스타일 (03_SOP_v1.html의 .data-btn-row와 동일하게):
```css
.data-btn-row { display: flex; gap: 10px; margin-bottom: 16px; }
.btn-download, .btn-upload {
  flex: 1; background: #1c2333;
  border: 1px solid rgba(77,163,255,0.3);
  color: #4da3ff; border-radius: 8px;
  font-size: 14px; padding: 10px;
  cursor: pointer; min-height: 44px;
}
```

---

# [수정 3] 우선순위 한글화 — 02_Task_v1.html + index.html

urgent → 즉시
today  → 오늘
normal → 보통

변경 위치:
1. 02_Task_v1.html
   - 업무 추가 폼 select 옵션 텍스트
   - signal 함수의 레이블
2. index.html
   - signal 함수의 레이블

구현:
```javascript
var PRIORITY_LABEL = { urgent: '즉시', today: '오늘', normal: '보통' };

function signal(priority) {
  var p = priority || 'normal';
  var color = PRIORITY_COLOR[p] || PRIORITY_COLOR.normal;
  var label = PRIORITY_LABEL[p] || p;
  return '<span class="signal" style="color:' + color + '">● ' + label + '</span>';
}
```

select 옵션:
```html
<option value="normal">보통</option>
<option value="today">오늘</option>
<option value="urgent">즉시</option>
```

---

# [수정 4] FAQ 번호 표시 — 04_FAQ_v1.html

질문 앞에 Q1. Q2. Q3. 순번 표시

렌더링 시:
```javascript
filtered.map(function(f, index) {
  // 질문 텍스트 앞에 'Q' + (index+1) + '.' 추가
})
```

표시 형식:
Q1. 복사기가 종이를 먹었어요
Q2. 학생이 복테를 못 찾겠어요

번호 스타일:
```css
.faq-num { color: #4da3ff; font-weight: 700; margin-right: 4px; }
```

기존 .faq-q-text::before { content: 'Q. '; } 제거 (번호로 대체)

---

# [수정 5] SOP 번호 표시 — 03_SOP_v1.html

제목 앞에 1. 2. 3. 순번 표시

렌더링 시:
```javascript
filtered.map(function(s, index) {
  // 제목 앞에 (index+1) + '.' 추가
})
```

표시 형식:
1. 복테 제출함 관리 SOP
2. 복테 제작 SOP

번호 스타일:
```css
.sop-num { color: #4da3ff; font-weight: 700; margin-right: 4px; }
```

---

# [수정 6] JSON 다운로드 파일명에 날짜 포함 — 전체 파일

날짜 함수:
```javascript
function getToday() {
  var d = new Date();
  return d.getFullYear() + '-' +
    String(d.getMonth() + 1).padStart(2, '0') + '-' +
    String(d.getDate()).padStart(2, '0');
}
```

파일명 변경:
- 02_Task_v1.html  → 'task_' + getToday() + '.json'
- 03_SOP_v1.html   → 'sop_' + getToday() + '.json'
- 04_FAQ_v1.html   → 'faq_' + getToday() + '.json'
- 05_Notice_v1.html → 'notice_' + getToday() + '.json'

업로드는 변경 없음.
브라우저가 마지막으로 열었던 폴더를 자동 기억하므로
한 번 같은 폴더에서 업로드하면 이후 동일 폴더가 자동으로 열림.

PWA 전환 시 폴더 경로 직접 선택/고정 기능 추가 예정.
지금은 이 방식으로 진행.

---

# [수정 7] 드래그 정렬 기능 추가 — 4개 파일

적용 대상:
- 02_Task_v1.html
- 03_SOP_v1.html
- 04_FAQ_v1.html
- 05_Notice_v1.html

## 공통 CSS
```css
.drag-handle {
  color: rgba(255,255,255,0.2);
  font-size: 18px;
  cursor: grab;
  padding-right: 10px;
  flex-shrink: 0;
  user-select: none;
}
.dragging {
  opacity: 0.4;
  background: #263045 !important;
}
```

## 각 카드 구조 변경
카드 최상위 div에 draggable="true" 및 data-id 속성 추가.
카드 내부 맨 왼쪽에 드래그 핸들 추가:
```html
<span class="drag-handle">⠿</span>
```

data-id 값:
- task: t.id
- sop: String(s.id)
- faq: String(f.id)
- notice: String(n.id)

## PC 드래그 함수 (공통)
```javascript
function addMouseDrag(container, saveOrder) {
  var dragEl = null;
  container.addEventListener('dragstart', function(e) {
    dragEl = e.target.closest('[data-id]');
    if (dragEl) setTimeout(function() { dragEl.classList.add('dragging'); }, 0);
  });
  container.addEventListener('dragover', function(e) {
    e.preventDefault();
    if (!dragEl) return;
    var after = getDragAfterElement(container, e.clientY);
    if (after == null) container.appendChild(dragEl);
    else container.insertBefore(dragEl, after);
  });
  container.addEventListener('dragend', function() {
    if (!dragEl) return;
    dragEl.classList.remove('dragging');
    saveOrder(Array.from(container.querySelectorAll('[data-id]'))
      .map(function(el) { return el.getAttribute('data-id'); }));
    dragEl = null;
  });
}

function getDragAfterElement(container, y) {
  var items = Array.from(container.querySelectorAll('[data-id]:not(.dragging)'));
  return items.reduce(function(closest, child) {
    var box = child.getBoundingClientRect();
    var offset = y - box.top - box.height / 2;
    if (offset < 0 && offset > closest.offset) return { offset: offset, element: child };
    return closest;
  }, { offset: Number.NEGATIVE_INFINITY }).element;
}
```

## 모바일 터치 드래그 함수 (공통)
```javascript
function addTouchDrag(container, saveOrder) {
  var dragEl = null;
  container.addEventListener('touchstart', function(e) {
    var handle = e.target.closest('.drag-handle');
    if (!handle) return;
    dragEl = handle.closest('[data-id]');
    if (dragEl) dragEl.classList.add('dragging');
    e.preventDefault();
  }, { passive: false });
  container.addEventListener('touchmove', function(e) {
    if (!dragEl) return;
    e.preventDefault();
    var y = e.touches[0].clientY;
    var items = Array.from(container.querySelectorAll('[data-id]:not(.dragging)'));
    var after = items.find(function(item) {
      var rect = item.getBoundingClientRect();
      return y < rect.top + rect.height / 2;
    });
    if (after) container.insertBefore(dragEl, after);
    else container.appendChild(dragEl);
  }, { passive: false });
  container.addEventListener('touchend', function() {
    if (!dragEl) return;
    dragEl.classList.remove('dragging');
    saveOrder(Array.from(container.querySelectorAll('[data-id]'))
      .map(function(el) { return el.getAttribute('data-id'); }));
    dragEl = null;
  });
}
```

## 각 파일 초기화 (render 함수 맨 끝에 추가)

### 02_Task_v1.html
```javascript
var c = document.getElementById('taskList');
function taskSaveOrder(newOrder) {
  var tasks = loadTasks();
  var sorted = newOrder.map(function(id) {
    return tasks.find(function(t) { return t.id === id; });
  }).filter(Boolean);
  saveTasks(sorted);
}
addMouseDrag(c, taskSaveOrder);
addTouchDrag(c, taskSaveOrder);
```

### 03_SOP_v1.html
```javascript
var c = document.getElementById('sopList');
function sopSaveOrder(newOrder) {
  var allSops = JSON.parse(localStorage.getItem('sops') || 'null') || SOPS;
  var sorted = newOrder.map(function(id) {
    return allSops.find(function(s) { return String(s.id) === id; });
  }).filter(Boolean);
  localStorage.setItem('sops', JSON.stringify(sorted));
}
addMouseDrag(c, sopSaveOrder);
addTouchDrag(c, sopSaveOrder);
```

### 04_FAQ_v1.html — 동일 패턴, 'faqList' / 'faqs' 키 사용

### 05_Notice_v1.html — 동일 패턴, 'noticeList' / 'notices' 키 사용

---

# 작업 순서

1. 전체 파일 "King" → "KING"
2. 02_Task JSON 버튼 레이아웃 수정
3. 우선순위 한글화 (즉시/오늘/보통)
4. FAQ 번호 표시 (Q1. Q2. ...)
5. SOP 번호 표시 (1. 2. ...)
6. 전체 파일 다운로드 파일명 날짜 포함
7. 드래그 정렬 (Task → SOP → FAQ → Notice 순서)

---

# 작업 완료 후

git add . && git commit -m "feat: KING text, Korean priority, numbering, date filename, drag reorder" && git push
