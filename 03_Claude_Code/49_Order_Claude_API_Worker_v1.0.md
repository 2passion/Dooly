# 50_Order_Claude_API_Worker_v1.0.md
# King Assistant OS v2.0
# 작업: Claude API + Cloudflare Workers 연동 (Dooly 챗봇 실제 AI 답변)

작성일: 2026-06-29
작업번호: 50
우선순위: 높음

---

## 목표

현재 Dooly 챗봇은 Mock 모드(data.js 기반 정적 답변)로 동작 중이다.
이번 작업에서 Claude API를 연동하여 실제 AI 답변으로 업그레이드한다.

### 아키텍처 (A안 — Cloudflare Workers 프록시)

```
PWA (Cloudflare Pages)
    ↓ fetch POST
Cloudflare Worker (프록시)
    ↓ API 키 주입
Claude API (claude-sonnet-4-6)
    ↓ 응답
PWA 챗봇 화면
```

**선택 이유:**
- API 키가 프론트엔드 코드에 노출되지 않음
- CORS 문제 없음 (Worker가 same-origin 처리)
- Cloudflare 무료 플랜으로 충분 (일 10만 요청)

---

## 작업 범위

1. Cloudflare Worker 생성 및 배포
2. Worker에 Claude API 키 환경변수 설정
3. PWA 챗봇 JS — Worker 엔드포인트 호출로 변경
4. Mock 모드 / AI 모드 전환 토글 유지
5. 동작 확인

---

## Step 1 — Cloudflare Worker 생성

### 1-1. Cloudflare 대시보드 접속
```
https://dash.cloudflare.com
→ 왼쪽 메뉴: Workers & Pages
→ Overview 탭
→ "Create" 버튼 클릭
→ "Create Worker" 선택
```

### 1-2. Worker 이름 설정
```
이름: dooly-claude-proxy
→ Deploy 버튼 클릭 (기본 코드로 일단 배포)
```

### 1-3. Worker 코드 교체
배포 후 "Edit code" 버튼 클릭 → 아래 코드로 전체 교체:

```javascript
export default {
  async fetch(request, env) {
    // CORS preflight 처리
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
      });
    }

    if (request.method !== 'POST') {
      return new Response('Method Not Allowed', { status: 405 });
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return new Response('Invalid JSON', { status: 400 });
    }

    const { messages, system } = body;

    if (!messages || !Array.isArray(messages)) {
      return new Response('messages 필드가 필요합니다.', { status: 400 });
    }

    const claudePayload = {
      model: 'claude-sonnet-4-6',
      max_tokens: 1024,
      system: system || '',
      messages: messages,
    };

    const claudeRes = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': env.CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify(claudePayload),
    });

    const claudeData = await claudeRes.json();

    return new Response(JSON.stringify(claudeData), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  },
};
```

→ 우측 상단 "Deploy" 버튼 클릭

---

## Step 2 — API 키 환경변수 설정

### 2-1. Worker 설정 페이지 이동
```
Workers & Pages
→ dooly-claude-proxy 클릭
→ Settings 탭
→ Variables and Secrets 섹션
→ "Add" 버튼 클릭
```

### 2-2. 환경변수 추가
```
Type: Secret
Variable name: CLAUDE_API_KEY
Value: [Anthropic Console에서 복사한 API 키]
→ Deploy 클릭
```

### Anthropic API 키 발급 위치
```
https://console.anthropic.com
→ API Keys 메뉴
→ Create Key
```

---

## Step 3 — Worker URL 확인

배포 완료 후 Worker URL 메모:
```
형식: https://dooly-claude-proxy.{계정명}.workers.dev
예시: https://dooly-claude-proxy.2davidpassion.workers.dev
```

---

## Step 4 — PWA 챗봇 JS 수정

### 수정 대상 파일
```
GitHub 저장소 내 챗봇 관련 JS 파일
(현재 Mock 모드 답변 처리 부분)
```

### 4-1. Worker URL 상수 추가 (파일 상단)
```javascript
// Claude API Worker 엔드포인트
const CLAUDE_WORKER_URL = 'https://dooly-claude-proxy.{계정명}.workers.dev';
```

### 4-2. AI 모드 답변 함수 추가
기존 Mock 답변 함수 아래에 추가:

```javascript
async function getClaudeAnswer(userMessage, dataContext) {
  const systemPrompt = `당신은 King Assistant OS의 AI 비서 둘리(Dooly)이다.
목표는 조교 교육, 업무 관리, SOP 관리, 운영 기록 관리를 지원하는 것이다.

핵심 원칙:
1. 추측 금지 — 모르면 "확인이 필요합니다." 라고 답변
2. SOP 우선 — FAQ → SOP → 공지사항 순으로 검색
3. 최신 문서 우선 — 충돌 시 최신 버전 기준
4. 조교 지원 우선 — 신규 조교 교육, 업무 안내, FAQ 응답
5. 원장 지시 우선

참고 데이터:
${dataContext}

금지사항:
- 추측 답변
- 없는 규정 생성
- 원장 승인 없는 규칙 변경
- 학생/학부모에게 직접 지시`;

  const response = await fetch(CLAUDE_WORKER_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      system: systemPrompt,
      messages: [{ role: 'user', content: userMessage }],
    }),
  });

  if (!response.ok) {
    throw new Error(`Worker 오류: ${response.status}`);
  }

  const data = await response.json();

  // Claude API 응답에서 텍스트 추출
  const text = data.content
    ?.filter(block => block.type === 'text')
    ?.map(block => block.text)
    ?.join('') || '답변을 가져올 수 없습니다.';

  return text;
}
```

### 4-3. 기존 답변 처리 로직 수정
Mock/AI 모드 분기 처리:

```javascript
async function handleUserMessage(userInput) {
  const isAIMode = localStorage.getItem('dooly_mode') === 'ai';

  if (isAIMode) {
    try {
      // data.js 데이터를 컨텍스트로 전달
      const dataContext = buildDataContext(); // 기존 FAQ/SOP 데이터 문자열화
      const answer = await getClaudeAnswer(userInput, dataContext);
      displayAnswer(answer, 'ai');
    } catch (err) {
      console.error('Claude API 오류:', err);
      displayAnswer('AI 연결에 실패했습니다. Mock 모드로 답변합니다.', 'error');
      // fallback: Mock 모드 실행
      const mockAnswer = getMockAnswer(userInput);
      displayAnswer(mockAnswer, 'mock');
    }
  } else {
    const mockAnswer = getMockAnswer(userInput);
    displayAnswer(mockAnswer, 'mock');
  }
}
```

### 4-4. data.js 컨텍스트 빌더 함수 추가
```javascript
function buildDataContext() {
  // 기존 data.js의 FAQ, SOP 데이터를 문자열로 변환
  // (data.js가 로드되어 있다고 가정)
  let context = '';

  if (typeof FAQ_DATA !== 'undefined') {
    context += '=== FAQ ===\n';
    FAQ_DATA.forEach(item => {
      context += `Q: ${item.question}\nA: ${item.answer}\n\n`;
    });
  }

  if (typeof SOP_DATA !== 'undefined') {
    context += '=== SOP ===\n';
    SOP_DATA.forEach(item => {
      context += `[${item.category}] ${item.title}\n${item.content}\n\n`;
    });
  }

  return context || '(참고 데이터 없음)';
}
```

---

## Step 5 — 모드 전환 토글 UI (기존 유지 확인)

기존 Mock/AI 토글이 있다면 그대로 유지.
없다면 설정 화면에 추가:

```html
<!-- 설정 탭 또는 챗봇 화면 내 -->
<div class="mode-toggle">
  <label>
    <input type="checkbox" id="aiModeToggle" onchange="toggleMode(this)">
    AI 모드 (Claude API)
  </label>
  <span class="mode-label" id="modeLabel">Mock 모드</span>
</div>
```

```javascript
function toggleMode(checkbox) {
  const mode = checkbox.checked ? 'ai' : 'mock';
  localStorage.setItem('dooly_mode', mode);
  document.getElementById('modeLabel').textContent =
    mode === 'ai' ? 'AI 모드 (Claude API)' : 'Mock 모드';
}

// 페이지 로드 시 토글 상태 복원
document.addEventListener('DOMContentLoaded', () => {
  const savedMode = localStorage.getItem('dooly_mode') || 'mock';
  const toggle = document.getElementById('aiModeToggle');
  if (toggle) {
    toggle.checked = savedMode === 'ai';
    document.getElementById('modeLabel').textContent =
      savedMode === 'ai' ? 'AI 모드 (Claude API)' : 'Mock 모드';
  }
});
```

---

## Step 6 — git push 및 배포

```bash
git add .
git commit -m "feat: Claude API Worker 연동 (Task #50)"
git push
```

Cloudflare Pages는 GitHub push 후 자동 배포.
약 1분 후 https://dooly-f4m.pages.dev 에서 확인.

---

## 완료 확인 체크리스트

```
□ Cloudflare Worker 배포 완료
□ CLAUDE_API_KEY 환경변수 설정 완료
□ Worker URL 확인 및 메모
□ PWA JS 파일 수정 완료 (Worker URL 입력)
□ git push 완료
□ Cloudflare Pages 자동 배포 완료 (약 1분)
□ 챗봇에서 AI 모드 토글 ON
□ 테스트 질문 입력 → Claude 실제 답변 확인
□ Mock 모드 토글 OFF → Mock 답변 정상 동작 확인
□ 에러 시 Mock fallback 동작 확인
```

---

## 예상 소요 시간

| 단계 | 시간 |
|------|------|
| Worker 생성 + 코드 입력 | 10분 |
| API 키 설정 | 5분 |
| PWA JS 수정 | 20분 |
| 배포 + 테스트 | 10분 |
| **합계** | **약 45분** |

---

## 주의사항

1. **API 키 절대 코드에 직접 입력 금지** — 반드시 Worker 환경변수(Secret)로 관리
2. Worker URL은 `CLAUDE_WORKER_URL` 상수로 관리 (하드코딩 분산 금지)
3. AI 모드 기본값은 **Mock** — 조교가 의도적으로 켜야 AI 모드 작동
4. data.js 구조가 변경된 경우 `buildDataContext()` 함수 맞게 수정 필요

---

## Claude Code 실행 명령

작업지시서 저장 후 Claude Code 입력창에 입력:

```
C:\Obsidian\Dooly\03_Claude_Code\50_Order_Claude_API_Worker_v1.0.md 파일을 읽고
Step 4 (PWA JS 수정) 부터 순서대로 진행해줘.
Step 1~3 (Cloudflare Worker 생성/설정) 은 수동으로 진행했어.
Worker URL은 [실제 URL 입력] 이야.
```

---

## 다음 작업

50번 완료 후 → **51번: Supabase Task 동기화**
