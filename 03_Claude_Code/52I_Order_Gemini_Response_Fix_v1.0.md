# 52I_Order_Gemini_Response_Fix_v1.0.md

작성일: 2026-06-30
작업 번호: Task #52-I
작업명: Gemini 응답 잘림 정확한 원인 수정
대상 파일: docs/api/gemini.js, docs/06_Dooly_v1.html
선행 조건: Task #52-H 완료 (커밋 8f6eccf)

---

## 상황

- maxOutputTokens 1000 → 2048 올렸더니 속도만 느려지고 여전히 잘림
- maxOutputTokens는 1000으로 복원
- 잘림 원인은 다른 곳에 있음 → 정확히 찾아서 수정

---

## 수정 1 — maxOutputTokens 복원

**api/gemini.js 와 docs/api/gemini.js 두 파일 모두:**

```javascript
maxOutputTokens: 2048  →  maxOutputTokens: 1000
```

---

## 수정 2 — 잘림 원인 찾기 및 수정

`docs/06_Dooly_v1.html` 에서 Gemini 응답을 받아서 화면에 출력하는
전체 흐름을 다음 순서로 확인한다.

### Step A — fetch 호출부 확인

Vercel Function 호출하는 fetch 코드를 찾는다.

```javascript
const response = await fetch('/api/gemini', { ... });
const data = await response.json();
```

`response.json()` 이후 `data` 에서 텍스트를 꺼내는 코드 전체를 확인한다.

### Step B — 응답 파싱 확인

Gemini API는 아래 구조로 응답한다:

```json
{
  "candidates": [
    {
      "content": {
        "parts": [{ "text": "전체 답변 텍스트" }]
      },
      "finishReason": "STOP"
    }
  ]
}
```

파싱 코드가 아래처럼 되어 있는지 확인:
```javascript
const text = data.candidates[0].content.parts[0].text;
```

만약 `data.answer` 또는 `data.text` 같은 다른 필드를 쓰고 있으면
Vercel Function이 응답을 가공하는 방식과 맞지 않아 잘릴 수 있음.

### Step C — Vercel Function 응답 구조 확인

`docs/api/gemini.js` 에서 Gemini 응답을 클라이언트에 내보내는 부분 확인:

```javascript
// 현재 방식 A: Gemini 원본 그대로 전달
res.json(geminiResponse);

// 또는 방식 B: answer 필드만 추출해서 전달
res.json({ answer: text });
```

클라이언트(HTML)의 파싱 코드와 Function의 응답 구조가
**일치하는지** 확인한다. 불일치하면 맞게 수정한다.

### Step D — 화면 출력 함수 확인

챗봇 말풍선에 텍스트를 넣는 함수를 찾는다.

```javascript
// 예시
bubble.innerHTML = formatText(answer);
// 또는
chatBox.innerHTML += `<div>${answer}</div>`;
```

`innerHTML` 에 넣기 전에 텍스트를 자르거나 길이를 제한하는 코드가 있으면 제거한다.

---

## 수정 방향 정리

위 Step A~D 확인 후:

1. **파싱 불일치** → 클라이언트 파싱 코드를 Function 응답 구조에 맞게 수정
2. **길이 제한 코드 발견** → 해당 코드 제거
3. **문제 없으면** → `docs/api/gemini.js` 에서 Gemini 원본 응답 전체를
   클라이언트에 그대로 전달하는 방식으로 변경

---

## 파일 정리 (Claude Code 프롬프트 템플릿)

```
아래 작업을 순서대로 실행해줘.

## 1. 작업지시서 이동
C:\Users\USER\Downloads\52I_Order_Gemini_Response_Fix_v1.0.md 파일을
C:\Obsidian\Dooly\03_Claude_Code\52I_Order_Gemini_Response_Fix_v1.0.md 로 이동

## 2. 작업 실행
위 작업지시서 내용대로 수정

## 3. git push
cd C:\Obsidian\Dooly
git add .
git commit -m "fix: maxOutputTokens 복원 + Gemini 응답 잘림 원인 수정"
git push
```

---

## 테스트

1. Dooly 챗봇 → Gemini AI 모드
2. "복사기 종이 먹었어요" 질문
3. 확인:
   - ✅ 속도가 이전처럼 빠름 (1~3초)
   - ✅ 답변이 끊기지 않고 완전하게 출력됨

---

## 완료 기준

- [ ] maxOutputTokens 1000으로 복원
- [ ] 응답 잘림 수정 (파싱 불일치 또는 길이 제한 코드 제거)
- [ ] 속도 정상 확인
- [ ] git push 완료

---

## END OF ORDER
