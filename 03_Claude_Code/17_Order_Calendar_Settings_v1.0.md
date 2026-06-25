# 17_Order_Calendar_Settings_v1.0.md
# KING Assistant OS — 홈 달력 + 설정 탭

---

# 수정/생성 대상
C:\Obsidian\Dooly\04_Runtime\index.html       (수정)
C:\Obsidian\Dooly\04_Runtime\07_Settings_v1.html  (신규 생성)
C:\Obsidian\Dooly\04_Runtime\*.html 전체       (네비게이션에 설정 탭 추가)

---

# [수정 1] index.html — 홈 달력 추가

## 달력 위치
업무 현황 카드 아래, 공지사항 섹션 위에 배치

## 달력 구조
```
[◀ 2026년 6월 ▶]

일  월  화  수  목  금  토
     1   2   3   4   5   6
 7   8   9  10  11  12  13
14  15  16  17  18  19  20
21  22  23  24  25  26  27
28  29  30
```

오늘 날짜: 파란 원으로 강조
업무 있는 날짜: 작은 점(●) 표시

## 주간 보기 토글
달력 헤더 옆에 [월간 / 주간] 토글 버튼:
- 월간: 전체 달력 표시
- 주간: 현재 주(일~토) 7일만 표시, 요일 헤더 포함

## 날짜 클릭 동작
날짜 클릭 시 달력 아래에 해당 날짜 업무 목록 표시:

```
2026년 6월 25일 업무
────────────────────
담당자별 그룹:
[조교A]
  ▼ 내신모의-중2초급 [즉시]
[조교B]
  ▼ 단원평가 초5A [보통]
```

담당자 클릭 시 드롭다운으로 해당 담당자 업무 목록 표시

## 구현 방식
tasks의 created_at 날짜 기준으로 날짜별 업무 매핑:
```javascript
function getTasksByDate(dateStr) {
  return loadTasks().filter(function(t) {
    return t.created_at === dateStr;
  });
}
```

날짜 업무 목록 HTML 구조:
```javascript
// 날짜 클릭 시
var tasks = getTasksByDate(dateStr);
// 담당자별 그룹화
var groups = {};
tasks.forEach(function(t) {
  if (!groups[t.assignee]) groups[t.assignee] = [];
  groups[t.assignee].push(t);
});
// 담당자 카드 렌더링
```

## CSS 추가
```css
.calendar-wrap { background: #1c2333; border-radius: 12px; padding: 16px; margin-bottom: 20px; }
.cal-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.cal-title { font-size: 15px; font-weight: 700; }
.cal-nav { background: transparent; border: none; color: #4da3ff; font-size: 18px; cursor: pointer; padding: 4px 8px; }
.cal-view-toggle { display: flex; gap: 6px; }
.cal-view-btn { background: #0b0f1a; border: 1px solid rgba(77,163,255,0.2); color: rgba(255,255,255,0.5); border-radius: 12px; font-size: 11px; padding: 3px 10px; cursor: pointer; }
.cal-view-btn.active { background: #4da3ff; border-color: #4da3ff; color: #0b0f1a; font-weight: 700; }
.cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px; }
.cal-day-header { text-align: center; font-size: 11px; opacity: 0.5; padding: 4px 0; }
.cal-day-header:first-child { color: #ff6b6b; }
.cal-day-header:last-child { color: #4da3ff; }
.cal-day { text-align: center; padding: 6px 2px; border-radius: 8px; cursor: pointer; font-size: 13px; position: relative; min-height: 32px; display: flex; flex-direction: column; align-items: center; gap: 2px; }
.cal-day:active { background: #263045; }
.cal-day.today { background: #4da3ff; color: #0b0f1a; font-weight: 700; border-radius: 50%; width: 28px; height: 28px; margin: 0 auto; display: flex; align-items: center; justify-content: center; }
.cal-day.selected { background: rgba(77,163,255,0.2); border-radius: 8px; }
.cal-dot { width: 4px; height: 4px; border-radius: 50%; background: #4da3ff; }
.cal-day.other-month { opacity: 0.25; }

/* 날짜별 업무 목록 */
.date-tasks { background: #1c2333; border-radius: 12px; padding: 16px; margin-bottom: 20px; }
.date-tasks-title { font-size: 13px; font-weight: 700; color: #4da3ff; margin-bottom: 12px; }
.assignee-group { margin-bottom: 10px; }
.assignee-group-header { background: #0b0f1a; border-radius: 8px; padding: 8px 12px; cursor: pointer; display: flex; align-items: center; justify-content: space-between; font-size: 14px; font-weight: 600; }
.assignee-group-body { display: none; padding: 8px 0 0 12px; }
.assignee-group.open .assignee-group-body { display: block; }
.assignee-task-item { font-size: 13px; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; align-items: center; gap: 8px; }
.no-task-msg { font-size: 13px; opacity: 0.4; text-align: center; padding: 12px 0; }
```

---

# [신규 생성] 07_Settings_v1.html — 설정 탭

## 전체 구조
```
Header: 설정

[담당자 관리]
  등록된 담당자 목록 (삭제 가능)
  담당자 추가 입력창 + 추가 버튼

[DB 폴더 경로]
  현재: 브라우저 기본 다운로드 폴더 사용
  ⚠️ PWA 전환 후 폴더 직접 지정 가능합니다.
  (현재 HTML 버전에서는 브라우저 보안 정책으로
   폴더 경로 지정이 불가합니다.)

[데이터 초기화]
  [전체 데이터 초기화] 버튼 (확인 후 실행)

Bottom Nav (설정 탭 포함)
```

## 담당자 관리 구현

```javascript
// localStorage 'assignees' 키 사용 (02_Task_v1.html과 공유)
function loadAssignees() {
  return JSON.parse(localStorage.getItem('assignees') || '[]');
}
function saveAssignees(list) {
  localStorage.setItem('assignees', JSON.stringify(list));
}

function addAssignee() {
  var name = document.getElementById('inputAssigneeName').value.trim();
  if (!name) return;
  var list = loadAssignees();
  if (list.includes(name)) { alert('이미 등록된 담당자입니다.'); return; }
  list.push(name);
  saveAssignees(list);
  document.getElementById('inputAssigneeName').value = '';
  renderAssignees();
}

function deleteAssignee(name) {
  if (!confirm(name + '을(를) 삭제하시겠습니까?')) return;
  saveAssignees(loadAssignees().filter(function(a) { return a !== name; }));
  renderAssignees();
}

function renderAssignees() {
  var list = loadAssignees();
  var el = document.getElementById('assigneeList');
  if (list.length === 0) {
    el.innerHTML = '<p class="empty-msg">등록된 담당자가 없습니다.</p>';
    return;
  }
  el.innerHTML = list.map(function(a) {
    return '<div class="assignee-item">' +
      '<span class="assignee-name">' + escHtml(a) + '</span>' +
      '<button class="delete-btn" onclick="deleteAssignee(\'' + escHtml(a) + '\')">삭제</button>' +
      '</div>';
  }).join('');
}
```

## DB 폴더 경로 섹션

```html
<div class="settings-section">
  <div class="settings-title">DB 폴더 경로</div>
  <div class="settings-card">
    <div class="settings-row">
      <span class="settings-label">현재 저장 위치</span>
      <span class="settings-value">브라우저 기본 다운로드 폴더</span>
    </div>
    <div class="settings-notice">
      ⚠️ 현재 HTML 버전에서는 브라우저 보안 정책으로<br>
      폴더 경로를 직접 지정할 수 없습니다.<br><br>
      📌 PWA 전환 후 폴더 직접 지정 기능이 추가됩니다.<br>
      JSON 파일은 브라우저 기본 다운로드 폴더에 저장됩니다.<br>
      업로드 시 마지막으로 열었던 폴더가 자동으로 열립니다.
    </div>
  </div>
</div>
```

## 데이터 초기화 섹션

```javascript
function resetAllData() {
  if (!confirm('모든 데이터(업무, SOP, FAQ, 공지, 담당자)를 초기화하시겠습니까?\n이 작업은 되돌릴 수 없습니다.')) return;
  localStorage.removeItem('tasks');
  localStorage.removeItem('sops');
  localStorage.removeItem('faqs');
  localStorage.removeItem('notices');
  localStorage.removeItem('assignees');
  alert('초기화 완료되었습니다.');
  renderAssignees();
}
```

## CSS
```css
.settings-section { margin-bottom: 24px; }
.settings-title { font-size: 13px; opacity: 0.6; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 10px; }
.settings-card { background: #1c2333; border-radius: 12px; padding: 16px; }
.settings-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.settings-label { font-size: 14px; opacity: 0.7; }
.settings-value { font-size: 14px; color: #4da3ff; }
.settings-notice { font-size: 13px; line-height: 1.7; opacity: 0.6; background: rgba(255,200,50,0.08); border: 1px solid rgba(255,200,50,0.2); border-radius: 8px; padding: 12px; margin-top: 8px; }
.assignee-item { display: flex; align-items: center; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.06); }
.assignee-name { font-size: 15px; }
.add-row { display: flex; gap: 10px; margin-top: 12px; }
.add-input { flex: 1; background: #0b0f1a; border: 1px solid rgba(77,163,255,0.3); border-radius: 8px; color: #fff; font-size: 15px; padding: 10px 12px; outline: none; min-height: 44px; }
.add-btn-sm { background: #4da3ff; color: #0b0f1a; border: none; border-radius: 8px; font-size: 14px; font-weight: 700; padding: 0 16px; min-height: 44px; cursor: pointer; white-space: nowrap; }
.reset-btn { width: 100%; background: rgba(255,80,80,0.15); border: 1px solid rgba(255,80,80,0.3); color: #ff5050; border-radius: 8px; font-size: 15px; font-weight: 700; min-height: 48px; cursor: pointer; }
.empty-msg { text-align: center; opacity: 0.4; font-size: 14px; padding: 16px 0; }
```

---

# [수정 3] 전체 HTML 파일 — Bottom Nav에 설정 탭 추가

모든 HTML 파일 (index, 02_Task, 03_SOP, 04_FAQ, 05_Notice, 06_Dooly) 의
Bottom Nav에 설정 탭 추가:

```html
<a href="07_Settings_v1.html">
  <span class="nav-icon">⚙️</span>
  <span>설정</span>
</a>
```

07_Settings_v1.html의 nav에는 class="active" 추가

Nav 항목이 7개가 되므로 font-size를 9px로 조정:
```css
nav a { font-size: 9px; }
nav a .nav-icon { font-size: 18px; }
```

---

# PWA 인수인계 메모 (SESSION_HANDOVER.md에 추가)

아래 내용을 SESSION_HANDOVER.md 하단에 추가:

```
## PWA 전환 시 추가 구현 항목

### DB 폴더 경로 선택 기능
- File System Access API 사용
- 구현 방법:
  const dirHandle = await window.showDirectoryPicker();
  localStorage.setItem('dbDirHandle', JSON.stringify(dirHandle));
- 폴더 선택 → IndexedDB에 FileSystemDirectoryHandle 저장
- 이후 다운로드/업로드 시 해당 폴더 자동 사용
- 설정 탭에 "폴더 선택" 버튼 추가 (현재는 안내 텍스트만 표시)
- 관련 파일: 07_Settings_v1.html DB 폴더 경로 섹션
```

---

# 작업 순서
1. index.html — 달력 + 주간 토글 + 날짜 클릭 업무 목록
2. 07_Settings_v1.html — 신규 생성
3. 전체 파일 Bottom Nav에 설정 탭 추가
4. SESSION_HANDOVER.md PWA 인수인계 메모 추가

---

# 작업 완료 후
git add . && git commit -m "feat: home calendar, settings tab, PWA handover memo" && git push
