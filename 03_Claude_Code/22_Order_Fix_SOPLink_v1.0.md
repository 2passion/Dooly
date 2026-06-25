# 22_Order_Fix_SOPLink_v1.0.md
# KING Assistant OS — SOP 본문 URL 링크 클릭 가능하게 수정

---

# 수정 대상
C:\Obsidian\Dooly\04_Runtime\03_SOP_v1.html

---

# 문제
SOP 상세 내용(body)에 URL이 일반 텍스트로 표시되어 클릭이 안 됨.
예: 신규 조교 온보딩 SOP의 http://crims.police.go.kr

---

# 수정 1: escHtml 후 URL을 링크로 변환하는 함수 추가

JS에서 기존 `escHtml` 함수 아래에 아래 함수를 추가한다:

```javascript
  function linkify(str) {
    return str.replace(/(https?:\/\/[^\s<>"]+)/g, function(url) {
      return '<a href="' + url + '" target="_blank" rel="noopener noreferrer" style="color:#4da3ff;text-decoration:underline;">' + url + '</a>';
    });
  }
```

---

# 수정 2: SOP 상세 내용 렌더링 시 linkify 적용

render() 함수에서 sop-detail 내용을 렌더링하는 부분을 수정한다.

## 기존 코드
```javascript
        '  <div class="sop-detail">' + escHtml(s.body).replace(/\n/g, '<br>') + '</div>',
```

## 변경 코드
```javascript
        '  <div class="sop-detail">' + linkify(escHtml(s.body).replace(/\n/g, '<br>')) + '</div>',
```

---

# 작업 완료 후

git add 04_Runtime/03_SOP_v1.html && git commit -m "feat: SOP body URL auto-link clickable" && git push
