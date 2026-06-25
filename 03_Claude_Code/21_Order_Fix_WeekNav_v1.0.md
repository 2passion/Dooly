# 21_Order_Fix_WeekNav_v1.0.md
# KING Assistant OS — 주간 달력 좌우 화살표 수정

---

# 수정 대상
C:\Obsidian\Dooly\04_Runtime\index.html

---

# 문제
주간 보기에서 ◀ ▶ 화살표를 클릭해도 주간이 이동하지 않음.
원인: prevMonth()/nextMonth() 함수에 `if (calView === 'week') return;` 이 있어서 주간 모드에서 아무 동작도 하지 않음.

---

# 수정 방법

index.html의 JS에서 prevMonth()와 nextMonth() 함수를 아래와 같이 교체한다.

## 기존 코드 (제거)
```javascript
  function prevMonth() {
    if (calView === 'week') return;
    calMonth--;
    if (calMonth < 0) { calMonth = 11; calYear--; }
    renderCalendar();
  }
  function nextMonth() {
    if (calView === 'week') return;
    calMonth++;
    if (calMonth > 11) { calMonth = 0; calYear++; }
    renderCalendar();
  }
```

## 변경 코드 (교체)
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

---

# 추가: weekOffset 변수 선언

JS 변수 선언 부분에서 `var selectedDate = null;` 아래에 아래 줄을 추가한다:

```javascript
  var weekOffset = 0;
```

---

# 추가: renderCalendar() 주간 부분 수정

renderCalendar() 함수의 주간(week) 분기에서 현재 날짜 기준으로 고정된 주를 사용하고 있음.
weekOffset을 반영하도록 수정한다.

## 기존 주간 코드 (제거)
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

## 변경 주간 코드 (교체)
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

# 추가: setCalView() 함수에 weekOffset 초기화

월간↔주간 전환 시 weekOffset을 0으로 리셋한다.

## 기존 코드
```javascript
  function setCalView(v) {
    calView = v;
    document.getElementById('btnMonth').className = 'cal-view-btn' + (v === 'month' ? ' active' : '');
    document.getElementById('btnWeek').className  = 'cal-view-btn' + (v === 'week'  ? ' active' : '');
    renderCalendar();
  }
```

## 변경 코드
```javascript
  function setCalView(v) {
    calView = v;
    weekOffset = 0;
    document.getElementById('btnMonth').className = 'cal-view-btn' + (v === 'month' ? ' active' : '');
    document.getElementById('btnWeek').className  = 'cal-view-btn' + (v === 'week'  ? ' active' : '');
    renderCalendar();
  }
```

---

# 작업 완료 후

git add 04_Runtime/index.html && git commit -m "fix: weekly calendar prev/next navigation with weekOffset" && git push
