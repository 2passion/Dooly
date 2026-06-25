# 23_Order_Fix_Combined_v1.0.md
# KING Assistant OS — 3가지 수정 한번에

---

# 수정 대상
C:\Obsidian\Dooly\04_Runtime\index.html
C:\Obsidian\Dooly\04_Runtime\03_SOP_v1.html
C:\Obsidian\Dooly\04_Runtime\04_FAQ_v1.html

---

# [수정 1] index.html — 주간 달력 ◀▶ 화살표 버그 수정

## 문제
주간 보기에서 ◀ ▶ 클릭해도 주간이 이동하지 않음.
원인: prevMonth()/nextMonth() 함수에 `if (calView === 'week') return;` 이 있어서 주간 모드에서 아무 동작도 하지 않음.

## 1-1. 변수 선언 추가
`var selectedDate = null;` 바로 아래에 아래 줄 추가:
```javascript
  var weekOffset = 0;
```

## 1-2. prevMonth() 함수 교체

### 기존 코드
```javascript
  function prevMonth() {
    if (calView === 'week') return;
    calMonth--;
    if (calMonth < 0) { calMonth = 11; calYear--; }
    renderCalendar();
  }
```

### 변경 코드
```javascript
  function prevMonth() {
    if (calView === 'week') {
      weekOffset--;
      renderCalendar();
      return;
    }
    calMonth--;
    if (calMonth < 0) { calMonth = 11; calYear--; }
    renderCalendar();
  }
```

## 1-3. nextMonth() 함수 교체

### 기존 코드
```javascript
  function nextMonth() {
    if (calView === 'week') return;
    calMonth++;
    if (calMonth > 11) { calMonth = 0; calYear++; }
    renderCalendar();
  }
```

### 변경 코드
```javascript
  function nextMonth() {
    if (calView === 'week') {
      weekOffset++;
      renderCalendar();
      return;
    }
    calMonth++;
    if (calMonth > 11) { calMonth = 0; calYear++; }
    renderCalendar();
  }
```

## 1-4. setCalView() 함수 교체

### 기존 코드
```javascript
  function setCalView(v) {
    calView = v;
    document.getElementById('btnMonth').className = 'cal-view-btn' + (v === 'month' ? ' active' : '');
    document.getElementById('btnWeek').className  = 'cal-view-btn' + (v === 'week'  ? ' active' : '');
    renderCalendar();
  }
```

### 변경 코드
```javascript
  function setCalView(v) {
    calView = v;
    weekOffset = 0;
    document.getElementById('btnMonth').className = 'cal-view-btn' + (v === 'month' ? ' active' : '');
    document.getElementById('btnWeek').className  = 'cal-view-btn' + (v === 'week'  ? ' active' : '');
    renderCalendar();
  }
```

## 1-5. renderCalendar() 주간 분기 교체

### 기존 코드
```javascript
    } else {
      var sun = new Date(now);
      sun.setDate(now.getDate() - now.getDay());
      var sat = new Date(sun); sat.setDate(sun.getDate() + 6);
      title = (sun.getMonth() + 1) + '월 ' + sun.getDate() + '일 ~ ' +
              (sat.getMonth() + 1) + '월 ' + sat.getDate() + '일';

      for (var i = 0; i < 7; i++) {
        var day = new Date(sun); day.setDate(sun.getDate() + i);
        var ds  = formatDate(day.getFullYear(), day.getMonth() + 1, day.getDate());
        var cls = 'cal-day';
        if (ds === todayStr)    cls += ' today';
        if (ds === selectedDate) cls += ' selected';
        var dot = (taskDates[ds] && ds !== todayStr) ? '<span class="cal-dot"></span>' : '';
        cells.push('<div class="' + cls + '" onclick="selectDate(\'' + ds + '\')">' + day.getDate() + dot + '</div>');
      }
    }
```

### 변경 코드
```javascript
    } else {
      var sun = new Date(now);
      sun.setDate(now.getDate() - now.getDay() + (weekOffset * 7));
      var sat = new Date(sun); sat.setDate(sun.getDate() + 6);
      title = (sun.getMonth() + 1) + '월 ' + sun.getDate() + '일 ~ ' +
              (sat.getMonth() + 1) + '월 ' + sat.getDate() + '일';

      for (var i = 0; i < 7; i++) {
        var day = new Date(sun); day.setDate(sun.getDate() + i);
        var ds  = formatDate(day.getFullYear(), day.getMonth() + 1, day.getDate());
        var cls = 'cal-day';
        if (ds === todayStr)    cls += ' today';
        if (ds === selectedDate) cls += ' selected';
        var dot = (taskDates[ds] && ds !== todayStr) ? '<span class="cal-dot"></span>' : '';
        cells.push('<div class="' + cls + '" onclick="selectDate(\'' + ds + '\')">' + day.getDate() + dot + '</div>');
      }
    }
```

---

# [수정 2] 03_SOP_v1.html — URL 링크 + 로컬 경로 복사 버튼

## 2-1. CSS 추가
`</style>` 태그 바로 앞에 아래 CSS 추가:

```css
  .path-copy-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(77,163,255,0.12);
    border: 1px solid rgba(77,163,255,0.3);
    color: #4da3ff;
    border-radius: 6px;
    font-size: 12px;
    padding: 4px 10px;
    cursor: pointer;
    margin: 2px 0;
    word-break: break-all;
    text-align: left;
    -webkit-tap-highlight-color: transparent;
  }
  .path-copy-btn:active { background: rgba(77,163,255,0.25); }

  .toast-msg {
    position: fixed;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(77,163,255,0.9);
    color: #0b0f1a;
    font-size: 13px;
    font-weight: 700;
    padding: 8px 20px;
    border-radius: 20px;
    z-index: 999;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s;
  }
  .toast-msg.show { opacity: 1; }
```

## 2-2. </body> 바로 앞에 토스트 div 추가
```html
<div class="toast-msg" id="toastMsg">경로가 복사되었습니다 📋</div>
```

## 2-3. JS에서 escHtml 함수 아래에 아래 두 함수 추가

```javascript
  function linkify(str) {
    // http/https URL → 클릭 가능한 링크
    str = str.replace(/(https?:\/\/[^\s<>"]+)/g, function(url) {
      return '<a href="' + url + '" target="_blank" rel="noopener noreferrer" style="color:#4da3ff;text-decoration:underline;">' + url + '</a>';
    });
    // C:\ 또는 \\ 로 시작하는 로컬 경로 → 복사 버튼
    str = str.replace(/((?:C:\\|D:\\|E:\\|\\\\)[^\s<>"<br>]+)/g, function(path) {
      var escaped = path.replace(/'/g, "\\'");
      return '<button class="path-copy-btn" onclick="copyPath(\'' + escaped + '\')">📋 ' + path + '</button>';
    });
    return str;
  }

  function copyPath(path) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(path).then(function() { showToast(); });
    } else {
      var ta = document.createElement('textarea');
      ta.value = path;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      showToast();
    }
  }

  function showToast() {
    var t = document.getElementById('toastMsg');
    t.classList.add('show');
    setTimeout(function() { t.classList.remove('show'); }, 2000);
  }
```

## 2-4. render() 함수에서 sop-detail 렌더링 수정

### 기존 코드
```javascript
        '  <div class="sop-detail">' + escHtml(s.body).replace(/\n/g, '<br>') + '</div>',
```

### 변경 코드
```javascript
        '  <div class="sop-detail">' + linkify(escHtml(s.body).replace(/\n/g, '<br>')) + '</div>',
```

---

# [수정 3] 04_FAQ_v1.html — URL 링크 + 로컬 경로 복사 버튼

03_SOP_v1.html에 적용한 수정 2-1 ~ 2-4와 동일하게 04_FAQ_v1.html에도 적용한다.

단, 수정 2-4에서 대상은 faq-answer 렌더링 부분이다:

### 기존 코드
```javascript
        '  <div class="faq-answer">' + escHtml(f.answer) + '</div>',
```

### 변경 코드
```javascript
        '  <div class="faq-answer">' + linkify(escHtml(f.answer)) + '</div>',
```

---

# 작업 완료 후

git add 04_Runtime/index.html 04_Runtime/03_SOP_v1.html 04_Runtime/04_FAQ_v1.html && git commit -m "fix: week calendar nav, SOP/FAQ URL link + local path copy button" && git push
