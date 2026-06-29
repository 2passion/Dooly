# 50_Order_Gemini_API_Worker_v2.0.md

작성일: 2026-06-29
작업: Task #50 — Gemini API + Cloudflare Worker 연동 (v2.0)
변경 이유: Claude API → Gemini API (하단 시행착오 참고)

---

# 배경

원래 Task #50은 Claude API 연동으로 계획됐으나,
Anthropic Console에서 크레딧 구매 버튼이 비활성화되는 문제로
기존에 발급된 Gemini API로 변경하여 진행한다.

---

# 현재 완료된 상태

- ✅ Cloudflare Worker 생성 완료
  - Worker 이름: `dooly-claude-proxy`
  - URL: `https://dooly-claude-proxy.2davidpassion.workers.dev`
- ✅ Worker에 Claude API 프록시 코드 배포 완료 (Gemini용으로 교체 필요)
- ❌ API 키 환경변수 미설정

---

# 작업 목표

Cloudflare Worker 코드를 Gemini API 호출로 교체하고
PWA JS에서 Gemini 답변을 받아 표시한다.

---

# Step 1 — Cloudflare Worker 코드 교체 (수동 작업)

Cloudflare Dashboard에서 직접 수행:

1. https://dash.cloudflare.com 접속
2. Workers & Pages → `dooly-claude-proxy` 클릭
3. Edit code 클릭
4. 기존 코드 전체 삭제 후 아래 코드로 교체

```javascript
export default {
  async fetch(request, env) {
    // CORS 처리
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

    try {
      const body = await request.json();
      const userMessage = body.message || '';
      const dataContext = body.context || '';

      // Gemini API 호출
      const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${env.GEMINI_API_KEY}`;

      const geminiResponse = await fetch(geminiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [
            {
              parts: [
                {
                  text: `당신은 킹수학 학원의 AI 비서 둘리(Dooly)입니다.
조교들의 업무를 돕고, FAQ와 SOP를 기반으로 정확하게 답변합니다.
모르는 내용은 추측하지 말고 "확인이 필요합니다."라고 답변하세요.

=== 참고 데이터 ===
${dataContext}

=== 조교 질문 ===
${userMessage}`
                }
              ]
            }
          ],
          generationConfig: {
            maxOutputTokens: 1000,
            temperature: 0.3,
          }
        }),
      });

      const geminiData = await geminiResponse.json();
      const answer = geminiData.candidates?.[0]?.content?.parts?.[0]?.text || '답변을 생성할 수 없습니다.';

      return new Response(JSON.stringify({ answer }), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      });

    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      });
    }
  },
};
```

5. **Deploy** 클릭

---

# Step 2 — Worker 환경변수 설정 (수동 작업)

Cloudflare Dashboard에서:

1. `dooly-claude-proxy` Worker → **Settings** 탭
2. **Variables and Secrets** 클릭
3. **Add variable** 클릭
4. 아래와 같이 입력:

| 항목 | 값 |
|------|------|
| Variable name | `GEMINI_API_KEY` |
| Type | **Secret** |
| Value | 기존 Gemini API 키 (`AIza...`) |

5. **Save** 클릭
6. Worker **재배포** (Deploy 버튼)

---

# Step 3 — Worker 동작 테스트 (수동 작업)

PowerShell 또는 터미널에서:

```powershell
curl -X POST https://dooly-claude-proxy.2davidpassion.workers.dev `
  -H "Content-Type: application/json" `
  -d '{"message": "복사기가 종이를 먹었어요", "context": "FAQ: 복사기 오류 시 전원을 끄고 용지함을 확인하세요."}'
```

응답에 `answer` 필드가 있으면 성공.

---

# Step 4 — PWA JS 수정 (Claude Code 실행)

## 수정 파일
`app.js` (또는 메인 JS 파일)

## 추가할 코드

### 상수 추가 (파일 상단)
```javascript
const WORKER_URL = 'https://dooly-claude-proxy.2davidpassion.workers.dev';
```

### buildDataContext() 함수 추가
```javascript
function buildDataContext() {
  const faqItems = DATA.faq.map(f => `Q: ${f.question}\nA: ${f.answer}`).join('\n\n');
  const sopItems = DATA.sop.map(s => `[${s.category}] ${s.title}: ${s.content}`).join('\n\n');
  return `=== FAQ ===\n${faqItems}\n\n=== SOP ===\n${sopItems}`;
}
```

### getGeminiAnswer() 함수 추가
```javascript
async function getGeminiAnswer(userMessage) {
  const context = buildDataContext();
  const response = await fetch(WORKER_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: userMessage, context }),
  });
  const data = await response.json();
  return data.answer || '답변을 가져올 수 없습니다.';
}
```

### handleUserMessage() 분기 처리
```javascript
async function handleUserMessage(message) {
  const mode = getCurrentMode(); // 'mock' or 'ai'

  if (mode === 'mock') {
    return getMockAnswer(message); // 기존 Mock 답변
  } else {
    showLoadingIndicator();
    const answer = await getGeminiAnswer(message);
    hideLoadingIndicator();
    return answer;
  }
}
```

---

# Step 5 — git push 및 배포 (Claude Code 실행)

```bash
git add .
git commit -m "feat: Gemini API 연동 (Task #50 v2.0)"
git push
```

---

# Step 6 — 최종 테스트

1. https://dooly-f4m.pages.dev 접속
2. AI 모드 토글 ON
3. "복사기가 종이를 먹었어요" 입력
4. Gemini 답변 수신 확인

---

# 완료 조건

- [ ] Worker Gemini API 코드 배포 완료
- [ ] GEMINI_API_KEY 환경변수 설정 완료
- [ ] Worker 테스트 응답 정상
- [ ] PWA AI 모드에서 Gemini 답변 표시
- [ ] git push 완료

---

# 다음 작업

Task #51 — Supabase Task 동기화
