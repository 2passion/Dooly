# 41_Order_MockMultiResult_v1.0.md
# King Assistant OS v1.0
# Claude Code 작업지시서

Version: v1.0
Date: 2026-06-27

---

# 작업 시작 전 필수 확인

아래 파일을 읽어라.

```
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md
C:\Obsidian\Dooly\04_Runtime\06_Dooly_v1.html
```

---

# 작업 목표

Mock 모드에서 키워드 매칭 결과를 전체 목록으로 표시
클릭하면 내용이 펼쳐지는 아코디언 방식 적용

현재:
```
"복테" 입력 → 첫 번째 매칭 1개만 답변
```

수정 후:
```
"복테" 입력 → 관련 FAQ/SOP 전체 목록 표시
              제목 클릭 시 내용 펼치기/접기
```

---

# STEP 1 — CSS 추가 (아코디언 스타일)

## 추가 위치

`<style>` 태그 안 맨 아래 (기존 .msg-time 아래)에 추가한다.

## 추가할 CSS

```css
  .result-list { margin-top: 8px; display: flex; flex-direction: column; gap: 6px; }
  .result-item { border-radius: 8px; overflow: hidden; }
  .result-item-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 12px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 700;
    gap: 8px;
    -webkit-tap-highlight-color: transparent;
  }
  .result-item-header.faq-header { background: rgba(74,222,128,0.12); color: #4ade80; }
  .result-item-header.sop-header { background: rgba(251,146,60,0.12); color: #fb923c; }
  .result-item-body {
    display: none;
    padding: 10px 12px;
    font-size: 13px;
    line-height: 1.7;
    white-space: pre-wrap;
    background: rgba(255,255,255,0.04);
    color: rgba(255,255,255,0.85);
  }
  .result-item.open .result-item-body { display: block; }
  .result-arrow { font-size: 11px; opacity: 0.6; flex-shrink: 0; }
  .result-summary {
    font-size: 13px;
    opacity: 0.6;
    margin-bottom: 6px;
  }
```

---

# STEP 2 — Mock 분기 코드 전체 교체

## 수정 대상

06_Dooly_v1.html 안의 Mock 분기 전체를 찾아서 교체한다.

## 찾을 부분 (시작)

```javascript
    if (model === 'mock') {
```

## 찾을 부분 (끝)

```javascript
      return;
    }
```

위 블록 전체를 아래 코드로 교체한다.

## 교체할 코드

```javascript
    if (selectedModel === 'mock') {
      var loadingEl2 = document.getElementById(loadingId);
      if (loadingEl2) loadingEl2.remove();

      var lowerText = text.toLowerCase();

      // FAQ 전체 매칭
      var faqMatches = FAQS.filter(function(f) {
        var inQ = f.question.toLowerCase().includes(lowerText) || lowerText.includes(f.question.toLowerCase());
        var inK = f.keywords && f.keywords.some(function(k){ return lowerText.includes(k.toLowerCase()); });
        return inQ || inK;
      });

      // SOP 전체 매칭
      var sopMatches = SOPS.filter(function(s) {
        var inT = s.title.toLowerCase().includes(lowerText) || lowerText.includes(s.title.toLowerCase());
        var inK = s.keywords && s.keywords.some(function(k){ return lowerText.includes(k.toLowerCase()); });
        return inT || inK;
      });

      var totalCount = faqMatches.length + sopMatches.length;
      var area = document.getElementById('chatArea');
      var div = document.createElement('div');
      div.className = 'msg dooly';
      var msgId = 'mock_' + Date.now();

      if (totalCount === 0) {
        // 매칭 없음
        div.innerHTML = [
          '<div class="msg-sender">Dooly<span class="msg-time">' + getNow() + '</span></div>',
          '<div class="msg-bubble">확인이 필요합니다.<br>SOP 또는 FAQ 탭에서 검색해보세요.',
          '<div style="margin-top:6px;"><span style="background:#1e3a5f;color:#60a5fa;border:1px solid #60a5fa;border-radius:4px;font-size:11px;padding:2px 8px;font-weight:700;">Mock</span></div>',
          '</div>'
        ].join('');
      } else {
        // 결과 목록 생성
        var itemsHtml = '';

        faqMatches.forEach(function(f, idx) {
          var itemId = msgId + '_faq_' + idx;
          itemsHtml += [
            '<div class="result-item" id="' + itemId + '">',
            '  <div class="result-item-header faq-header" onclick="toggleResultItem(\'' + itemId + '\')">',
            '    <span>FAQ Q' + f.id + ' ' + escHtml(f.question) + '</span>',
            '    <span class="result-arrow">▼</span>',
            '  </div>',
            '  <div class="result-item-body">' + escHtml(f.answer) + '</div>',
            '</div>'
          ].join('');
        });

        sopMatches.forEach(function(s, idx) {
          var itemId = msgId + '_sop_' + idx;
          itemsHtml += [
            '<div class="result-item" id="' + itemId + '">',
            '  <div class="result-item-header sop-header" onclick="toggleResultItem(\'' + itemId + '\')">',
            '    <span>SOP ' + s.id + ' ' + escHtml(s.title) + '</span>',
            '    <span class="result-arrow">▼</span>',
            '  </div>',
            '  <div class="result-item-body">' + escHtml(s.body) + '</div>',
            '</div>'
          ].join('');
        });

        div.innerHTML = [
          '<div class="msg-sender">Dooly<span class="msg-time">' + getNow() + '</span></div>',
          '<div class="msg-bubble">',
          '<div class="result-summary">관련 항목 ' + totalCount + '개를 찾았습니다.</div>',
          '<div class="result-list">' + itemsHtml + '</div>',
          '<div style="margin-top:8px;"><span style="background:#1e3a5f;color:#60a5fa;border:1px solid #60a5fa;border-radius:4px;font-size:11px;padding:2px 8px;font-weight:700;">Mock</span></div>',
          '</div>'
        ].join('');
      }

      area.appendChild(div);
      area.scrollTop = area.scrollHeight;
      saveChatHistory();
      return;
    }
```

---

# STEP 3 — toggleResultItem 함수 추가

## 추가 위치

getNow() 함수 아래에 추가한다.

## 추가할 코드

```javascript
  function toggleResultItem(id) {
    var el = document.getElementById(id);
    if (el) el.classList.toggle('open');
  }
```

---

# STEP 4 — git 커밋 및 push

```
cd C:\Obsidian\Dooly

git add .
git commit -m "feat: Mock 다중 결과 표시 + 아코디언 펼치기"
git push
```

---

# 전체 작업 완료 조건

```
✅ STEP 1 완료 (아코디언 CSS 추가)
✅ STEP 2 완료 (Mock 분기 전체 교체)
✅ STEP 3 완료 (toggleResultItem 함수 추가)
✅ STEP 4 완료 (git push)

✅ "복테" 입력 시 FAQ 4개 + SOP 4개 = 8개 목록 표시
✅ 제목 클릭 시 내용 펼쳐짐
✅ 다시 클릭 시 접힘
✅ FAQ → 초록 헤더, SOP → 주황 헤더
✅ 매칭 없을 시 "확인이 필요합니다" 출력
```

---

# 기대 화면

```
Dooly  2026-06-27 23:45
관련 항목 8개를 찾았습니다.

[FAQ Q2  학생이 복테를 못 찾겠어요    ▼] ← 초록
[FAQ Q8  복테 보관함 배치 순서...      ▼] ← 초록
[FAQ Q11 복테 완료 기준이 뭐예요?     ▼] ← 초록
[FAQ Q13 복테랑 오답노트가 뭐가 달라요? ▼] ← 초록
[SOP 1   복테 제출함 관리 SOP         ▼] ← 주황
[SOP 2   복테 제작 SOP               ▼] ← 주황
[SOP 3   복테 보관함 운영 SOP         ▼] ← 주황
[SOP 4   복테 처리 및 폐기 SOP        ▼] ← 주황

[Mock 파란뱃지]
```

---

# 다음 작업

42번 → PWA service-worker.js + 아이콘 추가 (192px, 512px)

---

# END OF ORDER
