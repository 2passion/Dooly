# 24_Order_MergeNotice_v1.0.md
# KING Assistant OS — 공지 탭을 홈으로 통합

---

# 작업 개요
- 홈(index.html) 공지사항 섹션에 JSON 다운로드/업로드 + 드래그 정렬 추가
- 전체 nav에서 공지 탭 제거 (7탭 → 6탭)
- 05_Notice_v1.html → 홈으로 리다이렉트

---

# 수정 대상
C:\Obsidian\Dooly\04_Runtime\index.html
C:\Obsidian\Dooly\04_Runtime\02_Task_v1.html
C:\Obsidian\Dooly\04_Runtime\03_SOP_v1.html
C:\Obsidian\Dooly\04_Runtime\04_FAQ_v1.html
C:\Obsidian\Dooly\04_Runtime\05_Notice_v1.html
C:\Obsidian\Dooly\04_Runtime\06_Dooly_v1.html
C:\Obsidian\Dooly\04_Runtime\07_Settings_v1.html

---

# [수정 1] index.html — 공지사항 섹션 전면 개편

## 1-1. CSS 추가
기존 CSS `</style>` 바로 앞에 추가:

```css
  /* 공지 JSON 버튼 */
  .notice-btn-row { display: flex; gap: 10px; margin-bottom: 12px; }
  .notice-btn-dl { flex: 1; background: #1c2333; border: 1px solid rgba(77,163,255,0.3); color: #4da3ff; border-radius: 8px; font-size: 14px; padding: 10px; cursor: pointer; min-height: 44px; -webkit-tap-highlight-color: transparent; }
  .notice-btn-ul { flex: 1; background: #1c2333; border: 1px solid rgba(77,163,255,0.3); color: #4da3ff; border-radius: 8px; font-size: 14px; padding: 10px; cursor: pointer; min-height: 44px; -webkit-tap-highlight-color: transparent; }

  /* 드래그 핸들 */
  .notice-drag-handle {
    color: rgba(255,255,255,0.2);
    font-size: 18px;
    cursor: grab;
    flex-shrink: 0;
    user-select: none;
    padding-right: 8px;
  }
  .notice-item.dragging {
    opacity: 0.4;
    background: #263045 !important;
  }
```

## 1-2. 공지사항 섹션 HTML 교체

기존:
```html
  <div class="section-block">
    <p class="section-title">공지사항</p>
    <div id="noticeList"></div>
  </div>
```

변경:
```html
  <div class="section-block">
    <p class="section-title">공지사항</p>
    <div class="notice-btn-row">
      <button class="notice-btn-dl" onclick="downloadNotices()">📥 JSON 다운로드</button>
      <button class="notice-btn-ul" onclick="uploadNotices()">📤 JSON 업로드</button>
    </div>
    <div id="noticeList"></div>
  </div>
```

## 1-3. nav에서 공지 탭 제거
기존 nav에서 아래 항목 제거:
```html
  <a href="05_Notice_v1.html">
    <span class="nav-icon">📢</span>
    <span>공지</span>
  </a>
```

## 1-4. JS 전면 수정

### NOTICES 기본 데이터는 유지하되 아래 함수들을 추가/수정한다.

#### render() 함수 수정
공지 렌더링 부분에 드래그 핸들 추가:

```javascript
  function render() {
    var tasks = JSON.parse(localStorage.getItem('tasks') || '[]');
    document.getElementById('count-pending').textContent  = tasks.filter(function(t) { return t.status === 'pending'; }).length;
    document.getElementById('count-progress').textContent = tasks.filter(function(t) { return t.status === 'in_progress'; }).length;
    document.getElementById('count-done').textContent     = tasks.filter(function(t) { return t.status === 'completed'; }).length;

    var stored = localStorage.getItem('notices');
    var data = stored ? JSON.parse(stored) : NOTICES;

    document.getElementById('noticeList').innerHTML = data.map(function(n) {
      var isOpen = openId === n.id;
      return [
        '<div class="notice-item' + (isOpen ? ' open' : '') + '" draggable="true" data-id="' + String(n.id) + '">',
        '  <div class="notice-header" onclick="toggle(' + n.id + ')">',
        '    <span class="notice-drag-handle" onclick="event.stopPropagation()">&#10783;</span>',
        '    <div class="notice-left">',
        '      <div class="notice-title">' + escHtml(n.title) + '</div>',
        '      <div class="notice-date">' + n.date + '</div>',
        '    </div>',
        '    <span class="notice-arrow">▼</span>',
        '  </div>',
        '  <div class="notice-detail">' + escHtml(n.body).replace(/\n/g, '<br>') + '</div>',
        '</div>'
      ].join('');
    }).join('');

    initNoticeDrag();
  }
```

#### JSON 다운로드/업로드 함수 추가
```javascript
  function getToday() {
    var d = new Date();
    return d.getFullYear() + '-' +
      String(d.getMonth() + 1).padStart(2, '0') + '-' +
      String(d.getDate()).padStart(2, '0');
  }

  function downloadNotices() {
    var stored = localStorage.getItem('notices');
    var data = stored ? JSON.parse(stored) : NOTICES;
    var blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url; a.download = 'notice_' + getToday() + '.json'; a.click();
    URL.revokeObjectURL(url);
  }

  function uploadNotices() {
    var input = document.createElement('input');
    input.type = 'file'; input.accept = '.json';
    input.onchange = function(e) {
      var file = e.target.files[0]; if (!file) return;
      var reader = new FileReader();
      reader.onload = function(ev) {
        try {
          var data = JSON.parse(ev.target.result);
          localStorage.setItem('notices', JSON.stringify(data));
          openId = null;
          render();
        } catch(err) { alert('JSON 형식이 올바르지 않습니다.'); }
      };
      reader.readAsText(file);
    };
    input.click();
  }
```

#### 드래그 정렬 함수 추가
```javascript
  function initNoticeDrag() {
    var container = document.getElementById('noticeList');
    if (!container) return;

    var dragEl = null;

    container.addEventListener('dragstart', function(e) {
      dragEl = e.target.closest('[data-id]');
      if (dragEl) setTimeout(function() { dragEl.classList.add('dragging'); }, 0);
    });
    container.addEventListener('dragover', function(e) {
      e.preventDefault();
      if (!dragEl) return;
      var after = getNoticeDragAfter(container, e.clientY);
      if (after == null) container.appendChild(dragEl);
      else container.insertBefore(dragEl, after);
    });
    container.addEventListener('dragend', function() {
      if (!dragEl) return;
      dragEl.classList.remove('dragging');
      var newOrder = Array.from(container.querySelectorAll('[data-id]'))
        .map(function(el) { return el.getAttribute('data-id'); });
      saveNoticeOrder(newOrder);
      dragEl = null;
    });

    container.addEventListener('touchstart', function(e) {
      var handle = e.target.closest('.notice-drag-handle');
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
      var newOrder = Array.from(container.querySelectorAll('[data-id]'))
        .map(function(el) { return el.getAttribute('data-id'); });
      saveNoticeOrder(newOrder);
      dragEl = null;
    });
  }

  function getNoticeDragAfter(container, y) {
    var items = Array.from(container.querySelectorAll('[data-id]:not(.dragging)'));
    return items.reduce(function(closest, child) {
      var box = child.getBoundingClientRect();
      var offset = y - box.top - box.height / 2;
      if (offset < 0 && offset > closest.offset) return { offset: offset, element: child };
      return closest;
    }, { offset: Number.NEGATIVE_INFINITY }).element;
  }

  function saveNoticeOrder(newOrder) {
    var stored = localStorage.getItem('notices');
    var allNotices = stored ? JSON.parse(stored) : NOTICES;
    var sorted = newOrder.map(function(id) {
      return allNotices.find(function(n) { return String(n.id) === id; });
    }).filter(Boolean);
    localStorage.setItem('notices', JSON.stringify(sorted));
  }
```

---

# [수정 2] 05_Notice_v1.html — 홈으로 리다이렉트

05_Notice_v1.html 파일 전체 내용을 아래로 교체한다:

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0;url=index.html">
<title>공지사항</title>
</head>
<body>
<script>location.replace('index.html');</script>
</body>
</html>
```

---

# [수정 3] 나머지 6개 파일 nav에서 공지 탭 제거

아래 6개 파일 각각에서 공지 탭 HTML을 찾아서 제거한다.

제거 대상 (각 파일에서 동일한 패턴):
```html
  <a href="05_Notice_v1.html">
    <span class="nav-icon">📢</span>
    <span>공지</span>
  </a>
```

대상 파일:
- 02_Task_v1.html
- 03_SOP_v1.html
- 04_FAQ_v1.html
- 06_Dooly_v1.html
- 07_Settings_v1.html

---

# 작업 완료 후

git add . && git commit -m "feat: merge notice tab into home, remove notice nav tab" && git push
