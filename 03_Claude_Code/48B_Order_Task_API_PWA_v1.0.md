# 48B_Order_Task_API_PWA_v1.0.md
# King Assistant OS v1.0
# 작업지시서 #48B — PWA Task 화면 FastAPI 연동

작성일: 2026-06-28
실행 위치: 노트북(화이트) Claude Code
우선순위: 높음
선행 작업: 48A 완료 ✅

---

## 1. 작업 개요

PWA Task 화면(02_Task_v1.html)을 수정한다.
기존 localStorage 방식에서 FastAPI 연동 방식으로 변경한다.

핵심 기능:
- 🟢 온라인 / 🔴 오프라인 상태 표시
- 온라인: FastAPI에서 Task 실시간 조회/추가/수정/삭제
- 오프라인: localStorage에 임시 저장
- [🔄 동기화] 버튼: 오프라인 상태일 때만 활성화

현재 접속 방식: 학원 내부 와이파이 전용
향후 계획: 외부 접속은 50번(Cloudflare Tunnel)에서 추가 예정

---

## 2. 환경 정보

| 항목 | 내용 |
|------|------|
| 수정 파일 | C:\Obsidian\Dooly\04_Runtime\02_Task_v1.html |
| 동기화 파일 | C:\Obsidian\Dooly\docs\02_Task_v1.html |
| API 주소 (학원 내부) | http://192.168.0.10:8001 |
| 연결 확인 엔드포인트 | GET /ping |

---

## 3. 작업 내용

### Step 1 — 02_Task_v1.html 상단에 아래 스크립트 추가

기존 <script> 태그 안 최상단에 아래 내용 추가:

```javascript
// ─── Task API 설정 ───────────────────────────────────────
const API_BASE = "http://192.168.0.10:8001";
const OFFLINE_KEY = "tasks_offline";
let isOnline = false;

// 온라인 상태 확인
async function checkOnlineStatus() {
  try {
    const res = await fetch(`${API_BASE}/ping`, {
      signal: AbortSignal.timeout(3000)
    });
    const data = await res.json();
    isOnline = data.status === "online";
  } catch {
    isOnline = false;
  }
  updateStatusBadge();
}

// 상태 뱃지 업데이트
function updateStatusBadge() {
  const badge = document.getElementById("sync-status");
  const syncBtn = document.getElementById("sync-btn");
  if (isOnline) {
    badge.textContent = "🟢 온라인";
    badge.style.color = "green";
    syncBtn.style.display = "none";
  } else {
    badge.textContent = "🔴 오프라인";
    badge.style.color = "red";
    syncBtn.style.display = "inline-block";
  }
}

// Task 전체 불러오기
async function loadTasks() {
  if (isOnline) {
    const res = await fetch(`${API_BASE}/tasks`);
    return await res.json();
  } else {
    return JSON.parse(localStorage.getItem(OFFLINE_KEY) || "[]");
  }
}

// Task 추가
async function addTask(task) {
  if (isOnline) {
    await fetch(`${API_BASE}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(task)
    });
  } else {
    const tasks = JSON.parse(localStorage.getItem(OFFLINE_KEY) || "[]");
    task.id = Date.now();
    task.created_at = new Date().toLocaleString("ko-KR");
    tasks.push(task);
    localStorage.setItem(OFFLINE_KEY, JSON.stringify(tasks));
  }
}

// Task 수정
async function updateTask(id, updated) {
  if (isOnline) {
    await fetch(`${API_BASE}/tasks/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updated)
    });
  } else {
    const tasks = JSON.parse(localStorage.getItem(OFFLINE_KEY) || "[]");
    const idx = tasks.findIndex(t => t.id === id);
    if (idx !== -1) tasks[idx] = { ...tasks[idx], ...updated };
    localStorage.setItem(OFFLINE_KEY, JSON.stringify(tasks));
  }
}

// Task 삭제
async function deleteTask(id) {
  if (isOnline) {
    await fetch(`${API_BASE}/tasks/${id}`, { method: "DELETE" });
  } else {
    const tasks = JSON.parse(localStorage.getItem(OFFLINE_KEY) || "[]");
    localStorage.setItem(OFFLINE_KEY,
      JSON.stringify(tasks.filter(t => t.id !== id)));
  }
}

// 수동 동기화
async function syncTasks() {
  const syncBtn = document.getElementById("sync-btn");
  const badge = document.getElementById("sync-status");
  badge.textContent = "🟡 동기화 중...";
  badge.style.color = "orange";
  syncBtn.disabled = true;

  await checkOnlineStatus();

  if (isOnline) {
    const offlineTasks = JSON.parse(localStorage.getItem(OFFLINE_KEY) || "[]");
    for (const task of offlineTasks) {
      await fetch(`${API_BASE}/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(task)
      });
    }
    localStorage.removeItem(OFFLINE_KEY);
    badge.textContent = "✅ 동기화 완료";
    badge.style.color = "green";
    setTimeout(() => updateStatusBadge(), 2000);
  } else {
    badge.textContent = "🔴 오프라인 (동기화 실패)";
    badge.style.color = "red";
  }
  syncBtn.disabled = false;
  await renderTasks();
}

// 페이지 로드 시 실행
window.addEventListener("load", async () => {
  await checkOnlineStatus();
  await renderTasks();
  // 30초마다 자동 상태 확인
  setInterval(checkOnlineStatus, 30000);
});
```

---

### Step 2 — Task 화면 상단 UI에 상태 표시 영역 추가

Task 화면 <body> 안 최상단에 아래 HTML 추가:

```html
<!-- 동기화 상태 표시 -->
<div style="padding: 8px 16px; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid #eee;">
  <span id="sync-status" style="font-size: 14px; font-weight: bold;">🟡 확인 중...</span>
  <button id="sync-btn"
    onclick="syncTasks()"
    style="display:none; padding: 4px 12px; font-size: 13px;
           background: #4CAF50; color: white; border: none;
           border-radius: 6px; cursor: pointer;">
    🔄 동기화
  </button>
</div>
```

---

### Step 3 — 기존 localStorage Task 코드 교체

기존 코드에서 아래 패턴을 찾아 교체한다.

```javascript
// 기존 (localStorage)
const tasks = JSON.parse(localStorage.getItem('tasks') || '[]');
localStorage.setItem('tasks', JSON.stringify(tasks));

// 교체 후 (FastAPI 함수 사용)
const tasks = await loadTasks();
await addTask(task);
await updateTask(id, updated);
await deleteTask(id);
```

기존 Task 목록 표시 함수(renderTasks 등)는
loadTasks() 결과를 받아서 화면에 표시하도록 수정한다.

---

### Step 4 — docs 폴더 동기화

수정 완료 후 반드시 docs 폴더도 동일하게 복사:

```
copy C:\Obsidian\Dooly\04_Runtime\02_Task_v1.html C:\Obsidian\Dooly\docs\02_Task_v1.html
```

---

### Step 5 — git push

```
cd C:\Obsidian\Dooly
git add .
git commit -m "feat: Task API FastAPI 연동 + 오프라인 동기화 (#48B)"
git push
```

---

## 4. 완료 확인

- [ ] 🟢 온라인 상태 표시 확인 (자습실 PC 켜져 있을 때)
- [ ] 🔴 오프라인 상태 표시 확인 (자습실 PC 꺼져 있을 때)
- [ ] 오프라인 시 [🔄 동기화] 버튼 표시 확인
- [ ] Task 추가 → tasks.json 저장 확인
- [ ] 조교A 추가 → 조교B 스마트폰에서 보임 확인
- [ ] [🔄 동기화] 버튼 → ✅ 동기화 완료 표시 확인
- [ ] docs 폴더 동기화 확인
- [ ] git push 완료 확인

---

## 5. 참고 — 향후 외부 접속 추가 계획 (50번)

```
현재 (48번): 학원 내부 와이파이만
const API_BASE = "http://192.168.0.10:8001";

나중에 (50번): 외부 접속 추가 시
Cloudflare Tunnel 연동 후
API_BASE를 Cloudflare URL로 변경 예정
```
