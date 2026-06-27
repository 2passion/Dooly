# 30_Order_Dooly_ChatHistory_v1.0.md
# KING Assistant OS — Dooly 대화 기록 유지 (localStorage)

---

# 문제
Dooly 탭을 벗어나면 대화 내용이 사라짐

# 해결
대화 내용을 localStorage에 저장
→ 탭 이동 후 돌아와도 대화 기록 유지
→ 브라우저 새로고침 후에도 유지

---

# 수정 대상
C:\Obsidian\Dooly\04_Runtime\06_Dooly_v1.html

---

# [수정 1] JS에 대화 기록 저장/불러오기 함수 추가

기존 `escHtml` 함수 바로 위에 아래 코드 추가:

```javascript
  /* ── 대화 기록 저장/불러오기 ── */
  var CHAT_STORAGE_KEY = 'dooly_chat_history';

  function saveChatHistory() {
    var area = document.getElementById('chatArea');
    if (!area) return;
    localStorage.setItem(CHAT_STORAGE_KEY, area.innerHTML);
  }

  function loadChatHistory() {
    var saved = localStorage.getItem(CHAT_STORAGE_KEY);
    if (!saved) return false;
    var area = document.getElementById('chatArea');
    if (!area) return false;
    area.innerHTML = saved;
    area.scrollTop = area.scrollHeight;
    return true;
  }

  function clearChatHistory() {
    localStorage.removeItem(CHAT_STORAGE_KEY);
    var area = document.getElementById('chatArea');
    if (area) area.innerHTML = '';
    addMsg('dooly', '안녕하세요! 무엇이든 질문하세요.');
  }
```

---

# [수정 2] 초기화 코드 수정

기존 마지막 줄:
```javascript
  addMsg('dooly', '안녕하세요! 무엇이든 질문하세요.');
```

변경:
```javascript
  // 저장된 대화 기록 불러오기, 없으면 초기 메시지
  if (!loadChatHistory()) {
    addMsg('dooly', '안녕하세요! 무엇이든 질문하세요.');
  }
```

---

# [수정 3] sendMessage() 함수에서 답변 저장 추가

기존 fetch 응답 처리 부분:
```javascript
        loadingEl.querySelector('.msg-bubble').textContent = data.answer;

        if (data.sources && data.sources.length > 0) {
```

변경:
```javascript
        loadingEl.querySelector('.msg-bubble').textContent = data.answer;

        saveChatHistory();

        if (data.sources && data.sources.length > 0) {
```

출처 태그 추가 후에도 저장:
기존:
```javascript
          loadingEl.appendChild(sourcesDiv);
        }
      }
    })
```

변경:
```javascript
          loadingEl.appendChild(sourcesDiv);
          saveChatHistory();
        }
      }
    })
```

---

# [수정 4] 대화 초기화 버튼 추가

## 4-1. CSS 추가
기존 `.model-select option` 아래에 추가:

```css
  .clear-btn {
    background: transparent;
    border: 1px solid rgba(255,80,80,0.3);
    color: rgba(255,80,80,0.6);
    border-radius: 6px;
    font-size: 11px;
    padding: 3px 8px;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
  }
  .clear-btn:active { background: rgba(255,80,80,0.1); }
```

## 4-2. 모델 선택 행에 초기화 버튼 추가

기존:
```html
<div class="model-select-row">
  <span class="model-label">모델</span>
  <select class="model-select" id="modelSelect">
    <option value="qwen2.5:7b">모델 A — qwen2.5:7b (고품질)</option>
    <option value="qwen2.5:3b">모델 B — qwen2.5:3b (빠름)</option>
    <option value="gemma3:4b">모델 C — gemma3:4b (균형)</option>
  </select>
</div>
```

변경:
```html
<div class="model-select-row">
  <span class="model-label">모델</span>
  <select class="model-select" id="modelSelect">
    <option value="qwen2.5:7b">모델 A — qwen2.5:7b (고품질)</option>
    <option value="qwen2.5:3b">모델 B — qwen2.5:3b (빠름)</option>
    <option value="gemma3:4b">모델 C — gemma3:4b (균형)</option>
  </select>
  <button class="clear-btn" onclick="clearChatHistory()">대화 초기화</button>
</div>
```

---

# 작업 완료 후

```
git add 04_Runtime/06_Dooly_v1.html && git commit -m "feat: Dooly chat history persist in localStorage + clear button" && git push
```
