# 52E_Order_SW_Cache_Gemini_UI_v1.0.md
# Task #52-E — 서비스워커 캐시 갱신 + Gemini 출처 태그 UI 개선

작성일: 2026-06-29
작업자: Claude Code
우선순위: 높음

---

## 1. 작업 개요

| 번호 | 항목 | 내용 |
|------|------|------|
| 52-E1 | 서비스워커 캐시 버전 업그레이드 | king-assistant-v2 → king-assistant-v3 |
| 52-E2 | Gemini 출처 태그 UI 개선 | 텍스트 출처 → FAQ 초록 / SOP 주황 태그로 변환 |
| 52-E3 | Gemini 답변 줄바꿈 처리 | 번호 목록마다 줄바꿈 적용 |

---

## 2. 수정 대상 파일 경로

```
C:\Obsidian\Dooly\
└── docs\
    ├── service-worker.js     ← 52-E1: 캐시 버전 수정
    └── 06_Dooly_v1.html      ← 52-E2, 52-E3: Gemini 출처 태그 + 줄바꿈
```

---

## 52-E1: 서비스워커 캐시 버전 업그레이드

### 파일 경로
```
C:\Obsidian\Dooly\docs\service-worker.js
```

### 수정 내용

#### 기존 코드 찾기
```javascript
king-assistant-v2
```

#### 변경 코드
```javascript
king-assistant-v3
```

> ⚠️ 파일 내 `king-assistant-v2` 문자열을 전부 `king-assistant-v3` 으로 교체한다.
> `CACHE_NAME`, `urlsToCache` 등 버전이 명시된 모든 위치에 적용한다.

---

## 52-E2: Gemini 출처 태그 UI 개선

### 파일 경로
```
C:\Obsidian\Dooly\docs\06_Dooly_v1.html
```

### 작업 내용

Gemini 답변 끝에 붙는 출처 텍스트를 Mock 모드처럼 시각적 태그로 변환한다.

#### 출처 파싱 함수 추가

`06_Dooly_v1.html`의 JavaScript 영역에 아래 함수를 추가한다:

```javascript
function parseGeminiSources(text) {
  // "참고: [FAQ Q1], [SOP 10], [SOP 21]" 형식 파싱
  const sourcePattern = /참고[:：]\s*(.+)$/m;
  const match = text.match(sourcePattern);
  
  if (!match) return { cleanText: text, tags: [] };
  
  const cleanText = text.replace(sourcePattern, '').trim();
  const sourceStr = match[1];
  
  // 대괄호 안 항목 추출
  const items = sourceStr.match(/\[([^\]]+)\]/g) || [];
  const tags = items.map(item => {
    const label = item.replace(/[\[\]]/g, '').trim();
    if (label.startsWith('FAQ')) {
      return { type: 'faq', label: label };
    } else if (label.startsWith('SOP')) {
      return { type: 'sop', label: label };
    } else {
      return { type: 'sop', label: label };
    }
  });
  
  return { cleanText, tags };
}

function renderGeminiTags(tags) {
  if (!tags || tags.length === 0) return '';
  const tagHtml = tags.map(tag => {
    const cls = tag.type === 'faq' ? 'source-tag faq-tag' : 'source-tag sop-tag';
    return `<span class="${cls}">${tag.label}</span>`;
  }).join('');
  return `<div class="source-tags">${tagHtml}</div>`;
}
```

#### CSS 추가

`06_Dooly_v1.html`의 `<style>` 영역에 아래 CSS를 추가한다:

```css
.source-tags {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.source-tag {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  cursor: default;
}
.faq-tag {
  background-color: #1a4a2e;
  color: #4caf82;
  border: 1px solid #4caf82;
}
.sop-tag {
  background-color: #4a2e1a;
  color: #ff9944;
  border: 1px solid #ff9944;
}
```

#### Gemini 답변 렌더링 부분 수정

Gemini 응답을 화면에 표시하는 코드에서 출처 파싱 및 태그 렌더링을 적용한다.

기존 Gemini 답변 표시 코드를 찾아 아래와 같이 수정한다:

```javascript
// 기존: 답변 텍스트를 그대로 표시하는 부분 찾기
// (appendMessage 또는 displayMessage 함수 내부)

// 수정: parseGeminiSources 적용
const { cleanText, tags } = parseGeminiSources(answerText);
const formattedText = cleanText.replace(/\n/g, '<br>');
const tagsHtml = renderGeminiTags(tags);
// 말풍선에 formattedText + tagsHtml 을 함께 표시
```

> ⚠️ 실제 함수명은 파일을 열어 확인 후 적용한다.
> Gemini 모드일 때만 파싱 적용, Mock 모드는 기존 방식 유지.

---

## 52-E3: Gemini 답변 줄바꿈 처리

### 파일 경로
```
C:\Obsidian\Dooly\docs\06_Dooly_v1.html
```

### 작업 내용

Gemini 답변의 `\n` 을 `<br>` 로 변환하여 번호 목록마다 줄바꿈이 적용되도록 한다.

52-E2의 렌더링 코드에 이미 포함됨:
```javascript
const formattedText = cleanText.replace(/\n/g, '<br>');
```

> ⚠️ 말풍선 컨테이너에 `white-space: pre-wrap` 대신 innerHTML로 표시해야 줄바꿈이 적용된다.

---

## 3. Git 커밋

모든 작업 완료 후:

```bash
cd C:\Obsidian\Dooly
git add .
git commit -m "feat: 서비스워커 v3 캐시 갱신 + Gemini 출처 태그 UI + 답변 줄바꿈"
git push
```

---

## 4. 작업 완료 확인

| 항목 | 확인 방법 |
|------|-----------|
| 52-E1 캐시 갱신 | 스마트폰에서 Dooly 접속 시 자동으로 새 버전 감지 |
| PWA 아이콘 | 홈 화면 삭제 후 재설치 → 공룡 아이콘 표시 확인 |
| 52-E2 출처 태그 | Gemini 모드로 질문 → FAQ 초록 / SOP 주황 태그 표시 확인 |
| 52-E3 줄바꿈 | 답변에서 번호 목록이 줄바꿈되어 표시 확인 |

---

## END OF TASK #52-E
