# 29_Order_Dooly_ModelSource_v1.0.md
# KING Assistant OS — Dooly 모델 선택 + 출처 표시

---

# 작업 개요
1. Dooly 헤더에 모델 선택 드롭다운 추가 (모델 A/B/C 이름으로 표시)
2. 답변 하단에 구체적 출처 표시 (예: FAQ Q1 / SOP 2)
3. server.py에서 모델을 동적으로 받고 출처 정보를 상세하게 반환

---

# 수정 대상
C:\Obsidian\Dooly\04_Runtime\06_Dooly_v1.html
C:\Obsidian\Dooly\05_RAG\server.py

---

# [수정 1] server.py — 모델 동적 수신 + 출처 상세 반환

## 1-1. ChatRequest 모델에 model 필드 추가

기존:
```python
class ChatRequest(BaseModel):
    message: str
```

변경:
```python
class ChatRequest(BaseModel):
    message: str
    model: str = "qwen2.5:7b"
```

## 1-2. chat() 함수에서 model 동적 사용

기존:
```python
        response = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt}
            ]
        )
```

변경:
```python
        selected_model = req.model if req.model else MODEL
        response = ollama.chat(
            model=selected_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt}
            ]
        )
```

## 1-3. 출처 정보 상세 파싱 후 반환

기존 return 부분:
```python
        answer = response["message"]["content"]
        return {"answer": answer, "sources": results["metadatas"][0] if results["metadatas"] else []}
```

변경:
```python
        answer = response["message"]["content"]

        # 출처 상세 파싱
        sources = []
        if results["metadatas"] and results["metadatas"][0]:
            for meta in results["metadatas"][0]:
                source_file = meta.get("source", "")
                chunk_index = meta.get("chunk", 0)

                if "faq_data" in source_file:
                    sources.append({
                        "type": "FAQ",
                        "label": "Q" + str(chunk_index + 1),
                        "file": source_file
                    })
                elif "sop_data" in source_file:
                    sources.append({
                        "type": "SOP",
                        "label": str(chunk_index + 1),
                        "file": source_file
                    })
                else:
                    sources.append({
                        "type": "DOC",
                        "label": source_file.replace(".txt", ""),
                        "file": source_file
                    })

        return {"answer": answer, "sources": sources}
```

---

# [수정 2] 06_Dooly_v1.html — 모델 선택 드롭다운 + 출처 표시 UI

## 2-1. CSS 추가
`</style>` 바로 앞에 추가:

```css
  /* 모델 선택 */
  .model-select-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 8px 16px;
    background: #1c2333;
    border-bottom: 1px solid rgba(77,163,255,0.1);
    flex-shrink: 0;
  }
  .model-label { font-size: 11px; opacity: 0.5; }
  .model-select {
    background: #0b0f1a;
    border: 1px solid rgba(77,163,255,0.3);
    border-radius: 8px;
    color: #4da3ff;
    font-size: 12px;
    padding: 4px 10px;
    outline: none;
    cursor: pointer;
    -webkit-appearance: none;
  }
  .model-select option { background: #0b0f1a; color: #fff; }

  /* 출처 표시 */
  .msg-sources {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-top: 6px;
  }
  .source-tag {
    border-radius: 4px;
    font-size: 10px;
    padding: 2px 7px;
    cursor: default;
  }
  .source-tag.faq { background: rgba(60,200,100,0.1); border: 1px solid rgba(60,200,100,0.3); color: #3cc864; }
  .source-tag.sop { background: rgba(255,180,50,0.1); border: 1px solid rgba(255,180,50,0.3); color: #ffb432; }
  .source-tag.doc { background: rgba(180,130,255,0.1); border: 1px solid rgba(180,130,255,0.3); color: #b482ff; }
```

## 2-2. HTML 구조 수정

`<div class="chat-area" id="chatArea"></div>` 바로 앞에 추가:

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

## 2-3. sendMessage() 함수 수정

선택된 모델을 fetch 요청에 포함하고 출처를 표시하도록 교체:

기존:
```javascript
    fetch(RAG_SERVER + '/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    })
    .then(function(res) { return res.json(); })
    .then(function(data) {
      var loadingEl = document.getElementById(loadingId);
      if (loadingEl) {
        loadingEl.querySelector('.msg-bubble').textContent = data.answer;
      }
    })
    .catch(function(err) {
      var loadingEl = document.getElementById(loadingId);
      if (loadingEl) {
        loadingEl.querySelector('.msg-bubble').textContent =
          'RAG 서버에 연결할 수 없습니다.\nC:\\Obsidian\\Dooly\\05_RAG\\start.bat 을 실행해주세요.';
      }
    });
```

변경:
```javascript
    var selectedModel = document.getElementById('modelSelect').value;

    fetch(RAG_SERVER + '/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, model: selectedModel })
    })
    .then(function(res) { return res.json(); })
    .then(function(data) {
      var loadingEl = document.getElementById(loadingId);
      if (loadingEl) {
        loadingEl.querySelector('.msg-bubble').textContent = data.answer;

        if (data.sources && data.sources.length > 0) {
          var sourcesDiv = document.createElement('div');
          sourcesDiv.className = 'msg-sources';

          var seen = {};
          data.sources.forEach(function(s) {
            var key = s.type + s.label;
            if (seen[key]) return;
            seen[key] = true;

            var tag = document.createElement('span');
            tag.className = 'source-tag ' + s.type.toLowerCase();
            tag.textContent = s.type + ' ' + s.label;
            tag.title = s.file;
            sourcesDiv.appendChild(tag);
          });

          loadingEl.appendChild(sourcesDiv);
        }
      }
    })
    .catch(function(err) {
      var loadingEl = document.getElementById(loadingId);
      if (loadingEl) {
        loadingEl.querySelector('.msg-bubble').textContent =
          'RAG 서버에 연결할 수 없습니다.\nrun_server.bat 을 실행해주세요.';
      }
    });
```

---

# 작업 완료 후

서버 재시작:
1. 현재 서버 창 Ctrl+C 종료
2. run_server.bat 다시 더블클릭

```
git add . && git commit -m "feat: Dooly model A/B/C selector + source tag display" && git push
```
