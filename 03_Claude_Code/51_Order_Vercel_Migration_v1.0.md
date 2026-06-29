# 51_Order_Vercel_Migration_v1.0.md

작성일: 2026-06-29
작업: Cloudflare Pages/Worker → Vercel 완전 이전
이유: Cloudflare Worker에서 Gemini API 호출 시 한국 서버 위치로 인한 차단 문제

---

# 배경

Cloudflare Worker가 아시아/한국 서버에서 실행되면서
Gemini API가 "User location is not supported" 오류로 차단됨.
Vercel은 미국 서버 기반이라 Gemini API 차단 없음.

---

# 변경 구조

```
변경 전:
GitHub → Cloudflare Pages (PWA 서빙)
              ↓
       Cloudflare Worker (프록시) → Gemini API (차단)

변경 후:
GitHub → Vercel (PWA 서빙 + 프록시)
              ↓
         Gemini API (미국 서버 → 정상)
```

---

# Step 1 — Vercel 가입 및 GitHub 연동 (수동 작업)

1. https://vercel.com 접속
2. **Sign Up** → **Continue with GitHub** 클릭
3. GitHub 계정으로 로그인
4. **Add New Project** 클릭
5. `2passion/Dooly` 저장소 선택 → **Import**
6. 설정 변경 없이 **Deploy** 클릭
7. 배포 완료 후 URL 확인 (예: `https://dooly-xxxx.vercel.app`)

---

# Step 2 — Vercel Function 생성 (Claude Code 실행)

## 생성할 파일
`api/gemini.js` (저장소 루트에 생성)

## 파일 내용

```javascript
export const config = {
  runtime: 'edge',
};

export default async function handler(request) {
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

    const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${process.env.GEMINI_API_KEY}`;

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
    const answer = geminiData.candidates?.[0]?.content?.parts?.[0]?.text || JSON.stringify(geminiData);

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
}
```

---

# Step 3 — PWA JS WORKER_URL 변경 (Claude Code 실행)

## 수정 파일
`docs/06_Dooly_v1.html`

## 변경 내용

```javascript
// 변경 전
var WORKER_URL = 'https://dooly-claude-proxy.2davidpassion.workers.dev';

// 변경 후
var WORKER_URL = 'https://dooly-xxxx.vercel.app/api/gemini';
```

> 주의: `dooly-xxxx.vercel.app` 부분은 Step 1에서 확인한 실제 Vercel URL로 교체

---

# Step 4 — Vercel 환경변수 설정 (수동 작업)

1. https://vercel.com 접속 → 프로젝트 선택
2. **Settings** → **Environment Variables**
3. 아래와 같이 추가:

| Name | Value | Environment |
|------|-------|-------------|
| `GEMINI_API_KEY` | `AIza...` (보유 중인 키) | Production |

4. **Save** 클릭
5. **Deployments** → 최신 배포 → **Redeploy** 클릭

---

# Step 5 — git push 및 배포 (Claude Code 실행)

```bash
git add .
git commit -m "feat: Vercel 이전 + Gemini API 프록시 (api/gemini.js)"
git push
```

---

# Step 6 — 최종 테스트

1. Vercel 배포 URL 접속 (예: `https://dooly-xxxx.vercel.app/06_Dooly_v1`)
2. **Gemini AI — Dooly 모드 (온라인)** 선택
3. "복사기가 종이를 먹었어요" 입력
4. 한글 답변 확인

---

# Step 7 — Cloudflare 정리 (선택사항)

Vercel에서 정상 작동 확인 후:
- Cloudflare Worker `dooly-claude-proxy` 삭제 (선택)
- Cloudflare Pages 프로젝트 삭제 (선택)
- GitHub 연동은 Vercel만 유지

---

# 완료 조건

- [ ] Vercel 배포 완료
- [ ] `api/gemini.js` 생성 완료
- [ ] GEMINI_API_KEY 환경변수 설정 완료
- [ ] PWA WORKER_URL Vercel URL로 변경 완료
- [ ] git push 완료
- [ ] 한글 답변 정상 수신 확인

---

# 파일 정리 (작업 완료 후 Claude Code 실행)

## 1. SESSION_HANDOVER 백업
현재 `02_SESSION_HANDOVER.md`를 아래 경로로 복사:
```
C:\Obsidian\Dooly\00_System\HANDOVER_HISTORY\14_SESSION_HANDOVER_v9.0.md
```

## 2. SESSION_HANDOVER 업데이트
다운로드된 새 파일을 아래 경로로 덮어쓰기:
```
원본: C:\Users\USER\Downloads\02_SESSION_HANDOVER_v10.0.md
대상: C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md
```

## 3. 작업지시서 이동
```
원본: C:\Users\USER\Downloads\51_Order_Vercel_Migration_v1.0.md
대상: C:\Obsidian\Dooly\03_Claude_Code\51_Order_Vercel_Migration_v1.0.md
```

## 4. git push
```bash
git add .
git commit -m "feat: Vercel 이전 + Gemini API 프록시 (Task #51)"
git push
```

---

# 다음 작업

Task #52 — Supabase Task 동기화
