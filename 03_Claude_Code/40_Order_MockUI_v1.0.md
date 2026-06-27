# 40_Order_MockUI_v1.0.md
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

1. Mock 모드 답변에 출처 태그 추가 (색깔 구별)
2. 모든 메시지에 날짜/시간 표시 추가

---

# STEP 1 — 날짜/시간 포맷 함수 추가

## 추가 위치

06_Dooly_v1.html 의 `<script>` 태그 안 맨 위 (다른 함수들 위)에 추가한다.

## 추가할 코드

```javascript
function getNow() {
  var d = new Date();
  var mm = String(d.getMonth() + 1).padStart(2, '0');
  var dd = String(d.getDate()).padStart(2, '0');
  var hh = String(d.getHours()).padStart(2, '0');
  var min = String(d.getMinutes()).padStart(2, '0');
  return d.getFullYear() + '-' + mm + '-' + dd + ' ' + hh + ':' + min;
}
```

---

# STEP 2 — addMsg 함수에 날짜/시간 추가

## 현재 addMsg 함수 (찾을 부분)

```javascript
  function addMsg(who, text) {
    var area = document.getElementById('chatArea');
    var div = document.createElement('div');
    div.className = 'msg ' + who;
    div.innerHTML = [
      '<div class="msg-sender">' + (who === 'dooly' ? 'Dooly' : '나') + '</div>',
      '<div class="msg-bubble">' + escHtml(text) + '</div>'
    ].join('');
    area.appendChild(div);
    area.scrollTop = area.scrollHeight;
  }
```

## 변경 후 코드

```javascript
  function addMsg(who, text) {
    var area = document.getElementById('chatArea');
    var div = document.createElement('div');
    div.className = 'msg ' + who;
    div.innerHTML = [
      '<div class="msg-sender">' + (who === 'dooly' ? 'Dooly' : '나') +
      '<span class="msg-time">' + getNow() + '</span></div>',
      '<div class="msg-bubble">' + escHtml(text) + '</div>'
    ].join('');
    area.appendChild(div);
    area.scrollTop = area.scrollHeight;
  }
```

---

# STEP 3 — 시간 표시 CSS 추가

## 추가 위치

`<style>` 태그 안 맨 아래에 추가한다.

## 추가할 CSS

```css
  .msg-time {
    font-size: 10px;
    opacity: 0.4;
    margin-left: 8px;
    font-weight: 400;
  }
```

---

# STEP 4 — Mock 모드 출처 태그 함수 추가

## 추가 위치

getNow() 함수 아래에 추가한다.

## 추가할 코드

```javascript
  function renderSourceTags(matched, type) {
    if (!matched) return '';
    var color = type === 'faq'
      ? 'background:#1a4a2e;color:#4ade80;border:1px solid #4ade80;'
      : 'background:#4a2e0a;color:#fb923c;border:1px solid #fb923c;';
    var label = type === 'faq'
      ? 'FAQ Q' + matched.id
      : 'SOP ' + matched.id;
    return '<div class="source-tags" style="margin-top:6px;">' +
      '<span style="' + color + 'border-radius:4px;font-size:11px;padding:2px 8px;font-weight:700;">' +
      label + '</span></div>';
  }
```

---

# STEP 5 — Mock 모드 분기에 출처 태그 적용

## 현재 Mock 분기 코드 (찾을 부분)

```javascript
    if (model === 'mock') {
      var loadingEl2 = document.getElementById(loadingId);
      if (loadingEl2) loadingEl2.remove();
      var mockAns = mockResponse(text);
      addMsg('dooly', mockAns + '\n\n[Mock 모드]');
      saveChatHistory();
      return;
    }
```

## 변경 후 코드

```javascript
    if (model === 'mock') {
      var loadingEl2 = document.getElementById(loadingId);
      if (loadingEl2) loadingEl2.remove();

      // FAQ 먼저 매칭
      var faqMatch = null;
      for (var fi = 0; fi < FAQS.length; fi++) {
        var f = FAQS[fi];
        var inQ = f.question.toLowerCase().includes(text.toLowerCase()) || text.toLowerCase().includes(f.question.toLowerCase());
        var inK = f.keywords && f.keywords.some(function(k){ return text.toLowerCase().includes(k.toLowerCase()); });
        if (inQ || inK) { faqMatch = f; break; }
      }

      // SOP 매칭
      var sopMatch = null;
      if (!faqMatch) {
        for (var si = 0; si < SOPS.length; si++) {
          var s = SOPS[si];
          var inT = s.title.toLowerCase().includes(text.toLowerCase()) || text.toLowerCase().includes(s.title.toLowerCase());
          var inSK = s.keywords && s.keywords.some(function(k){ return text.toLowerCase().includes(k.toLowerCase()); });
          if (inT || inSK) { sopMatch = s; break; }
        }
      }

      var mockAns = faqMatch
        ? '[FAQ ' + faqMatch.id + '] ' + faqMatch.question + '\n\n' + faqMatch.answer
        : sopMatch
          ? '[SOP-' + sopMatch.id + '] ' + sopMatch.title + '\n\n' + sopMatch.body
          : '확인이 필요합니다.\nSOP 또는 FAQ 탭에서 검색해보세요.';

      // 메시지 + 출처 태그 + Mock 뱃지
      var area = document.getElementById('chatArea');
      var div = document.createElement('div');
      div.className = 'msg dooly';
      var tagHtml = faqMatch
        ? renderSourceTags(faqMatch, 'faq')
        : sopMatch
          ? renderSourceTags(sopMatch, 'sop')
          : '';
      div.innerHTML = [
        '<div class="msg-sender">Dooly<span class="msg-time">' + getNow() + '</span></div>',
        '<div class="msg-bubble">' + escHtml(mockAns) + tagHtml +
        '<div style="margin-top:6px;"><span style="background:#1e3a5f;color:#60a5fa;border:1px solid #60a5fa;border-radius:4px;font-size:11px;padding:2px 8px;font-weight:700;">Mock</span></div></div>'
      ].join('');
      area.appendChild(div);
      area.scrollTop = area.scrollHeight;
      saveChatHistory();
      return;
    }
```

---

# STEP 6 — git 커밋 및 push

```
cd C:\Obsidian\Dooly

git add .
git commit -m "feat: Mock 출처 태그 + 날짜/시간 표시 추가"
git push
```

---

# 전체 작업 완료 조건

```
✅ STEP 1 완료 (getNow 함수 추가)
✅ STEP 2 완료 (addMsg 시간 표시)
✅ STEP 3 완료 (msg-time CSS 추가)
✅ STEP 4 완료 (renderSourceTags 함수 추가)
✅ STEP 5 완료 (Mock 분기 출처 태그 적용)
✅ STEP 6 완료 (git push)

✅ 메시지마다 날짜/시간 표시 확인
✅ Mock 답변 하단에 FAQ Q1 (초록) 또는 SOP 10 (주황) 태그 확인
✅ Mock 뱃지 (파란색) 확인
```

---

# 기대 화면

```
나                    2026-06-27 20:45
복사기 종이 먹었어요

Dooly                 2026-06-27 20:45
[FAQ 1] 복사기가 종이를 먹었어요

종이가 구겨진 경우 ADF를 사용하지 말고...

[FAQ Q1 초록태그] [Mock 파란태그]
```

---

# 다음 작업

41번 → PWA service-worker.js + 아이콘 추가 (192px, 512px)

---

# END OF ORDER
