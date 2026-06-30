# 57_Order_TaskFilter_Sync_v1.0.md
# King Assistant OS v2.0
# 작업지시서 #57 — Task 화면 담당자 필터 동기화 확인

작성일: 2026-06-30
우선순위: 보통
전제조건: Task #53 완료 (Supabase Task 동기화, 커밋 82d593a)

---

## 1. 작업 개요

### 목적
Task #53에서 Supabase 연동을 완료했으나, 담당자 필터 기능이 기기 간에 정상적으로 동기화되는지 검증하고 문제가 있으면 수정한다.

### 확인 항목 3가지

| 번호 | 항목 | 설명 |
|------|------|------|
| A | 필터 쿼리 정확성 | Supabase에 담당자별 where절이 올바르게 전달되는지 |
| B | 기기 간 실시간 동기화 | 기기 A에서 Task 추가/변경 시 기기 B에 즉시 반영되는지 |
| C | 필터 상태 유지 | 새로고침 후에도 선택된 필터가 유지되는지 |

---

## 2. 사전 파악 — 현재 코드 구조 확인

Claude Code에서 아래 파일을 읽고 현재 Task 필터 구현 방식을 파악한다.

```
# Task 화면 HTML 확인
type C:\Obsidian\Dooly\docs\02_Task_v1.html

# Vercel Task API 프록시 확인
type C:\Obsidian\Dooly\docs\api\tasks.js
```

파악 포인트:
- 담당자 필터 UI 구현 방식 (드롭다운 / 버튼 / 기타)
- Supabase 쿼리 시 담당자 필터 파라미터 전달 여부
- 필터 상태 저장 방식 (localStorage / URL 파라미터 / 메모리)

---

## 3. Step 1 — 필터 쿼리 정확성 확인 (항목 A)

### 3-1. docs/api/tasks.js 확인 포인트

`tasks.js`에서 아래 로직이 정상인지 확인한다.

```javascript
// 기대하는 형태 (GET 요청 시)
const assignee = req.query.assignee;  // 또는 req.body.assignee
if (assignee && assignee !== '전체') {
  query = query.eq('assignee', assignee);  // Supabase 필터
}
```

문제가 있으면 아래 기준으로 수정한다.

#### tasks.js 수정 기준 (GET 핸들러)

```javascript
// 수정 전 (필터 미적용 예시)
const { data, error } = await supabase
  .from('tasks')
  .select('*');

// 수정 후 (담당자 필터 적용)
const assignee = req.query.assignee;
let query = supabase.from('tasks').select('*');
if (assignee && assignee !== '전체' && assignee !== '') {
  query = query.eq('assignee', assignee);
}
const { data, error } = await query.order('created_at', { ascending: false });
```

### 3-2. 02_Task_v1.html 확인 포인트

Task 화면에서 Supabase API 호출 시 담당자 파라미터가 포함되는지 확인한다.

```javascript
// 기대하는 형태
async function loadTasks(assigneeFilter = '전체') {
  const params = assigneeFilter !== '전체'
    ? `?assignee=${encodeURIComponent(assigneeFilter)}`
    : '';
  const res = await fetch(`/api/tasks${params}`);
  // ...
}
```

---

## 4. Step 2 — 기기 간 실시간 동기화 확인 (항목 B)

### 4-1. 현재 동기화 방식 파악

Task #53 구현이 polling 방식인지 확인한다.

```javascript
// polling 방식 예시 (02_Task_v1.html에서 확인)
// setInterval로 주기적 fetch 여부 확인
```

### 4-2. polling 미구현 시 추가

polling이 없으면 아래 코드를 `02_Task_v1.html`에 추가한다.

추가 위치: DOMContentLoaded 이벤트 핸들러 내부 (기존 loadTasks() 호출 아래)

```javascript
// 30초마다 Task 목록 새로고침 (기기 간 동기화)
let currentFilter = '전체';
setInterval(() => {
  loadTasks(currentFilter);
}, 30000);
```

`currentFilter` 변수는 필터 버튼/드롭다운 클릭 시 업데이트되도록 연결한다.

---

## 5. Step 3 — 필터 상태 유지 확인 (항목 C)

### 5-1. 현재 필터 상태 저장 방식 확인

`02_Task_v1.html`에서 필터 선택 시 상태 저장 여부를 확인한다.

### 5-2. localStorage 저장 미구현 시 추가

필터 상태가 저장되지 않으면 아래 로직을 추가한다.

```javascript
// 필터 선택 시 저장
function setFilter(assignee) {
  currentFilter = assignee;
  localStorage.setItem('task_filter_assignee', assignee);
  loadTasks(assignee);
  // 필터 버튼 UI 업데이트 (기존 로직 유지)
}

// 페이지 로드 시 복원
document.addEventListener('DOMContentLoaded', () => {
  const saved = localStorage.getItem('task_filter_assignee') || '전체';
  currentFilter = saved;
  loadTasks(saved);
  // 저장된 필터에 맞게 버튼 UI 활성화 (기존 로직 연동)
});
```

---

## 6. Step 4 — 실기기 테스트 체크리스트

코드 수정 완료 후 킹스가 직접 아래 순서로 테스트한다.

```
□ 테스트 환경 준비
  - Galaxy S25: https://dooly-eight.vercel.app/02_Task_v1.html 접속
  - iPhone 또는 PC: 동일 URL 접속

□ 항목 A 테스트 (필터 쿼리)
  - Galaxy에서 담당자 필터 선택
  - 해당 담당자 Task만 표시되는지 확인
  - F12(PC) 또는 브라우저 개발자도구에서 네트워크 탭:
    /api/tasks?assignee=XXX 형태로 요청되는지 확인

□ 항목 B 테스트 (기기 간 동기화)
  - Galaxy에서 새 Task 추가 (담당자 지정)
  - iPhone/PC에서 30초 이내 새로고침 없이 반영되는지 확인
  - 또는 수동 새로고침 후 반영 확인

□ 항목 C 테스트 (필터 상태 유지)
  - Galaxy에서 특정 담당자 필터 선택
  - 브라우저 새로고침
  - 동일 필터가 선택된 상태로 복원되는지 확인
```

---

## 7. 테스트 결과별 처리

### Pass (모든 항목 정상)

```
cd C:\Obsidian\Dooly
git add .
git commit -m "fix: Task #57 — 담당자 필터 동기화 확인 완료 (코드 수정 없음)"
git push
```

### Fail (수정 발생)

```
cd C:\Obsidian\Dooly
git add docs/02_Task_v1.html docs/api/tasks.js
git commit -m "fix: Task #57 — 담당자 필터 쿼리 및 동기화 수정"
git push
```

---

## 8. 완료 후 파일 정리

```
cd C:\Obsidian\Dooly

## 작업지시서 자기 자신 이동 (이미 이동된 경우 생략)
move "C:\Users\USER\Downloads\57_Order_TaskFilter_Sync_v1.0.md" "C:\Obsidian\Dooly\03_Claude_Code\57_Order_TaskFilter_Sync_v1.0.md"

git add .
git commit -m "docs: Task #57 완료 — 담당자 필터 동기화 확인"
git push
```

---

## 9. 완료 기준

| 항목 | 기준 |
|------|------|
| A. 필터 쿼리 | /api/tasks?assignee=XXX 형태로 Supabase 쿼리 정상 전달 |
| B. 기기 간 동기화 | 한 기기에서 추가한 Task가 다른 기기에서 새로고침 후 표시 |
| C. 필터 상태 유지 | 새로고침 후 마지막 선택 필터 복원 |
| git push | 커밋 및 Vercel 자동 배포 완료 |

---

## 10. 주의사항

- `buildDataContext()` 함수는 절대 수정하지 않는다.
- 기존 Task CRUD 기능(추가/삭제/상태변경)이 동작하는지 수정 전후로 확인한다.
- Supabase RLS는 현재 비활성화 상태이므로 Auth 없이도 쿼리가 동작한다.
- polling 간격은 30초로 설정한다. 너무 짧으면 Supabase 무료 플랜 요청 한도에 영향을 줄 수 있다.

---

# END OF ORDER #57
