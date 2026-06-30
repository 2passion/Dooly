# 54_Order_Dooly_Manifest_ErrorHandling_v1.0.md
# Task #54 — manifest 링크 태그 추가 + Gemini 에러 한국어 처리

작성일: 2026-06-30
대상 파일: C:\Obsidian\Dooly\docs\06_Dooly_v1.html

---

# 작업 개요

| 항목 | 내용 |
|------|------|
| 작업 번호 | Task #54 |
| 작업명 | manifest 링크 태그 추가 + Gemini 에러 한국어 처리 |
| 대상 파일 | docs/06_Dooly_v1.html |
| 작업 유형 | HTML 수정 |
| 예상 소요 | 5분 이내 |

---

# 작업 1 — manifest 링크 태그 추가

## 원인
06_Dooly_v1.html의 <head>에 manifest 링크 태그가 없어
PWA 설치 버튼이 나타나지 않고 "No manifest detected" 오류 발생.

## 수정 위치
C:\Obsidian\Dooly\docs\06_Dooly_v1.html

## 수정 내용

아래 코드를 찾아:
```
<script src="data.js"></script>
</head>
```

위 코드 바로 앞에 아래 3줄 추가:
```html
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#0b0f1a">
<meta name="apple-mobile-web-app-capable" content="yes">
```

수정 후 결과:
```html
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#0b0f1a">
<meta name="apple-mobile-web-app-capable" content="yes">
<script src="data.js"></script>
</head>
```

---

# 작업 2 — Gemini 에러 한국어 처리

## 원인
Gemini API 에러 발생 시 JSON 원문이 그대로 말풍선에 출력됨.
에러 코드별로 한국어 안내 메시지를 표시하도록 수정.

## 수정 위치
C:\Obsidian\Dooly\docs\06_Dooly_v1.html
→ getGeminiAnswer 함수 아래 .catch 블록

## 에러 메시지 함수 추가

아래 코드를 찾아:
```
  async function getGeminiAnswer(userMessage) {
```

바로 위에 아래 함수 전체를 추가:
```javascript
  function getKoreanErrorMessage(err, responseStatus) {
    // 네트워크 끊김
    if (!navigator.onLine || (err && err.message && err.message.includes('fetch'))) {
      return '📶 인터넷 연결을 확인해 주세요.\nWi-Fi 또는 데이터 연결이 끊어진 것 같아요.\n연결 후 다시 질문해 주세요.';
    }
    var status = responseStatus || 0;
    if (status === 503) {
      return '⚠️ AI 서버가 잠시 바쁩니다.\n지금 Gemini 서버에 접속자가 많아요.\n잠시 후 다시 질문해 주세요. (보통 1~2분 내 복구)';
    }
    if (status === 429) {
      return '🚫 잠시 대기가 필요해요.\nAI 요청 횟수 한도에 도달했어요.\n1분 정도 기다린 후 다시 질문해 주세요.';
    }
    if (status === 500) {
      return '🔧 AI에 일시적인 오류가 발생했어요.\n잠시 후 같은 질문을 다시 해 주세요.\n계속 오류가 나면 원장님께 알려주세요.';
    }
    if (status === 401 || status === 403) {
      return '🔑 AI 연결 설정에 문제가 있어요.\n조교가 해결할 수 없는 오류예요.\n원장님께 바로 알려주세요.';
    }
    if (err && err.name === 'AbortError') {
      return '⏱️ 응답이 너무 오래 걸리고 있어요.\n질문을 더 짧게 나눠서 다시 시도해 주세요.';
    }
    return '⚠️ AI 서버가 잠시 바쁩니다.\n잠시 후 다시 질문해 주세요.';
  }
```

## getGeminiAnswer 함수 수정

아래 코드를 찾아:
```
  async function getGeminiAnswer(userMessage) {
    var context = buildDataContext();
    var response = await fetch(WORKER_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userMessage, context: context })
    });
    var data = await response.json();
    return data.answer || '답변을 가져올 수 없습니다.';
  }
```

아래 코드로 교체:
```javascript
  async function getGeminiAnswer(userMessage) {
    var context = buildDataContext();
    var controller = new AbortController();
    var timeoutId = setTimeout(function() { controller.abort(); }, 30000);
    var response = await fetch(WORKER_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userMessage, context: context }),
      signal: controller.signal
    });
    clearTimeout(timeoutId);
    if (!response.ok) {
      var errMsg = getKoreanErrorMessage(null, response.status);
      throw { message: errMsg, status: response.status };
    }
    var data = await response.json();
    return data.answer || '답변을 가져올 수 없습니다.';
  }
```

## .catch 블록 수정

아래 코드를 찾아:
```
        .catch(function(err) {
          var loadingEl = document.getElementById(loadingId);
          if (loadingEl) loadingEl.remove();
          addMsg('dooly', '오류가 발생했습니다: ' + err.message);
          saveChatHistory();
        });
```

아래 코드로 교체:
```javascript
        .catch(function(err) {
          var loadingEl = document.getElementById(loadingId);
          if (loadingEl) loadingEl.remove();
          var korMsg = (err && err.message && (
            err.message.includes('📶') ||
            err.message.includes('⚠️') ||
            err.message.includes('🚫') ||
            err.message.includes('🔧') ||
            err.message.includes('🔑') ||
            err.message.includes('⏱️')
          )) ? err.message : getKoreanErrorMessage(err, 0);
          addMsg('dooly', korMsg);
          saveChatHistory();
        });
```

---

# 작업 3 — git push

아래 명령어 순서대로 실행:

```
cd C:\Obsidian\Dooly
git add docs/06_Dooly_v1.html
git commit -m "fix: manifest 링크 태그 추가 + Gemini 에러 한국어 처리 (#54)"
git push
```

---

# 완료 확인

## 확인 1 — manifest
1. https://dooly-eight.vercel.app/06_Dooly_v1.html 열기
2. F12 → Application → Manifest 탭
3. "No manifest detected" 가 사라지고 manifest 내용이 보이면 ✅
4. 주소창 오른쪽에 설치 버튼(모니터+화살표) 나타나면 ✅

## 확인 2 — 에러 메시지
1. Gemini AI 모드 선택
2. 질문 입력 후 에러 발생 시
3. JSON 원문 대신 한국어 안내 메시지가 보이면 ✅

---

# 주의사항

- buildDataContext() 함수는 절대 수정하지 않는다
- getGeminiAnswer 함수 수정 시 fetch 구조 유지할 것
- 문제 발생 시 롤백 커밋: 82d593a

---

# END
