# 53_Order_Supabase_Task_Sync_v1.0.md

작성일: 2026-06-30
작업 번호: Task #53
작업명: Supabase Task 동기화
대상 파일: docs/06_Dooly_v1.html, docs/api/tasks.js (신규), Vercel 환경변수
선행 조건: Task #52-Y 완료 (커밋 35f7576)

---

## 0. 사전 준비 (수동 작업 — Claude Code 실행 전)

아래 3단계는 브라우저에서 직접 수행한다.

### Step 0-1. Supabase 프로젝트 생성

1. https://supabase.com 접속 → 신규 가입
2. New Project 생성
   - Name: dooly
   - Region: Northeast Asia (Seoul) 권장

### Step 0-2. tasks 테이블 생성

Supabase 대시보드 → SQL Editor → 아래 쿼리 실행:

```sql
create table tasks (
  id uuid default gen_random_uuid() primary key,
  title text not null,
  status text not null default 'Pending',
  priority text not null default 'Medium',
  assignee text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create or replace function update_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger tasks_updated_at
  before update on tasks
  for each row execute function update_updated_at();

alter table tasks disable row level security;
```

### Step 0-3. API 키 확인

Supabase 대시보드 → Settings → API 에서 아래 두 값 복사:
- Project URL : https://xxxxxxxxxxxx.supabase.co
- anon public key : eyJ...

---

## 1. Vercel 환경변수 추가 (수동 작업)

Vercel 대시보드 → dooly-eight → Settings → Environment Variables

| Key | Value |
|-----|-------|
| SUPABASE_URL | Step 0-3의 Project URL |
| SUPABASE_ANON_KEY | Step 0-3의 anon public key |

추가 후 Vercel Redeploy 필요.

---

## 2. 파일 작업 (Claude Code 실행)

### 2-1. Vercel Function 신규 생성

파일 경로: docs/api/tasks.js

```javascript
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();

  const headers = {
    'Content-Type': 'application/json',
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
    'Prefer': 'return=representation'
  };

  try {
    if (req.method === 'GET') {
      const response = await fetch(
        `${SUPABASE_URL}/rest/v1/tasks?order=created_at.asc`,
        { headers }
      );
      const data = await response.json();
      return res.status(200).json(data);
    }

    if (req.method === 'POST') {
      const response = await fetch(`${SUPABASE_URL}/rest/v1/tasks`, {
        method: 'POST', headers,
        body: JSON.stringify(req.body)
      });
      const data = await response.json();
      return res.status(201).json(data);
    }

    if (req.method === 'PATCH') {
      const { id, ...updates } = req.body;
      const response = await fetch(
        `${SUPABASE_URL}/rest/v1/tasks?id=eq.${id}`,
        { method: 'PATCH', headers, body: JSON.stringify(updates) }
      );
      const data = await response.json();
      return res.status(200).json(data);
    }

    if (req.method === 'DELETE') {
      const { id } = req.body;
      await fetch(`${SUPABASE_URL}/rest/v1/tasks?id=eq.${id}`,
        { method: 'DELETE', headers });
      return res.status(204).end();
    }

    return res.status(405).json({ error: 'Method not allowed' });

  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
```

### 2-2. docs/06_Dooly_v1.html — Task API 엔드포인트 교체

기존 FastAPI 로컬 서버(192.168.0.10:8001) 호출 코드를 찾아서
Vercel Function(/api/tasks)으로 교체한다.

찾을 패턴:
```javascript
const TASK_API = 'http://192.168.0.10:8001'
// 또는
fetch('http://192.168.0.10:8001/tasks'
```

교체:
```javascript
const TASK_API = '/api/tasks';
```

loadTasks, updateTaskStatus, createTask 함수에서
위 상수를 사용하도록 확인 및 수정.

완료 후 git push:
```
cd C:\Obsidian\Dooly
git add .
git commit -m "feat: Task #53 Supabase Task 동기화"
git push
```

---

## 3. 파일 정리 (Claude Code 프롬프트 템플릿)

```
아래 작업을 순서대로 실행해줘.

## 1. SESSION_HANDOVER 백업
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md 파일을
C:\Obsidian\Dooly\00_System\HANDOVER_HISTORY\17_SESSION_HANDOVER_v13.0.md 로 복사

## 2. SESSION_HANDOVER 업데이트
C:\Users\USER\Downloads\02_SESSION_HANDOVER_v13.0.md 파일을
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md 로 덮어쓰기

## 3. 작업지시서 이동
C:\Users\USER\Downloads\53_Order_Supabase_Task_Sync_v1.0.md 파일을
C:\Obsidian\Dooly\03_Claude_Code\53_Order_Supabase_Task_Sync_v1.0.md 로 이동

## 4. git push
cd C:\Obsidian\Dooly
git add .
git commit -m "docs: SESSION_HANDOVER v13.0 업데이트"
git push
```

---

## 4. 테스트 순서

1. Vercel 배포 완료 확인
2. https://dooly-eight.vercel.app/api/tasks GET → 빈 배열 [] 응답 확인
3. PWA Task 화면에서 목록 로드 확인
4. Task 상태 변경 → Supabase Table Editor에서 반영 확인
5. 다른 기기에서 동일 PWA 접속 → 동기화 확인

---

## 5. 완료 기준

- [ ] Supabase tasks 테이블 생성
- [ ] Vercel 환경변수 2개 추가 + Redeploy
- [ ] /api/tasks GET 정상 응답
- [ ] PWA Task 목록 로드 정상
- [ ] 상태 변경 후 Supabase 반영 확인
- [ ] 2개 기기 동기화 확인

---

## 6. 주의사항

- SUPABASE_ANON_KEY는 Vercel Function 안에서만 사용 (클라이언트 노출 금지)
- RLS 비활성화 상태 → 나중에 Auth 추가 시 활성화
- 기존 tasks.json 삭제 금지 (롤백 대비 보관)
- Vercel Root Directory = docs (공백 없이)

---

## END OF ORDER
