# 52G_Order_Gemini_Source_Number_v1.0.md

작성일: 2026-06-30
작업 번호: Task #52-G
작업명: Gemini 출처 번호 표시 수정
대상 파일: docs/06_Dooly_v1.html
선행 조건: Task #52-F 완료 (커밋 9a24c94)

---

## 목표

Gemini AI 답변 하단에 출처 태그가 표시될 때
번호 없이 카테고리명만 나오는 문제를 수정한다.

### 현재 (문제)
```
FAQ Q: 복사기가 종이를 먹었어요
SOP 복사기/스캔 SOP
```

### 목표 (수정 후)
```
FAQ Q1
SOP 1
```

---

## 수정 내용

### 1. 시스템 프롬프트 수정

`docs/06_Dooly_v1.html` 안에서 Gemini에게 전달하는 시스템 프롬프트를 찾는다.
아래와 같이 출처 형식 지시를 명확하게 수정한다.

**찾을 텍스트 (기존 출처 지시 부분):**
```
출처를 표시할 때는 [FAQ Q1], [SOP 10] 형식으로 표시하세요.
```
또는 유사한 출처 관련 지시문

**교체할 내용:**
```
답변 마지막에 참고한 자료를 반드시 아래 형식으로만 표시하세요.
FAQ를 참고했으면: [FAQ Q1] 또는 [FAQ Q2] (숫자만, 제목 없이)
SOP를 참고했으면: [SOP 1] 또는 [SOP 3] (숫자만, 카테고리명 없이)
형식을 절대 바꾸지 마세요. 제목이나 카테고리명을 붙이지 마세요.
```

---

### 2. parseGeminiSources() 함수 수정

`docs/06_Dooly_v1.html` 안의 `parseGeminiSources()` 함수를 찾아서
아래 코드로 교체한다.

```javascript
function parseGeminiSources(text) {
  const sources = [];

  // FAQ Q1, FAQ Q2, ... 패턴 매칭
  const faqMatches = text.match(/\[FAQ\s*Q(\d+)\]/gi) || [];
  faqMatches.forEach(match => {
    const num = match.match(/\d+/)[0];
    if (!sources.find(s => s.label === `FAQ Q${num}`)) {
      sources.push({ label: `FAQ Q${num}`, type: 'faq' });
    }
  });

  // SOP 1, SOP 2, ... 패턴 매칭
  const sopMatches = text.match(/\[SOP\s*(\d+)\]/gi) || [];
  sopMatches.forEach(match => {
    const num = match.match(/\d+/)[0];
    if (!sources.find(s => s.label === `SOP ${num}`)) {
      sources.push({ label: `SOP ${num}`, type: 'sop' });
    }
  });

  return sources;
}
```

---

### 3. 출처 태그 렌더링 함수 확인

출처 태그를 화면에 그리는 함수(renderSources 또는 유사 함수)가
`source.label` 값을 그대로 출력하는지 확인한다.

정상이면 수정 불필요.
만약 label 대신 다른 필드를 쓰고 있으면 `source.label` 을 쓰도록 수정한다.

---

## 파일 정리 (Claude Code 프롬프트 템플릿)

```
아래 작업을 순서대로 실행해줘.

## 1. 작업지시서 이동
C:\Users\USER\Downloads\52G_Order_Gemini_Source_Number_v1.0.md 파일을
C:\Obsidian\Dooly\03_Claude_Code\52G_Order_Gemini_Source_Number_v1.0.md 로 이동

## 2. 작업 실행
위 작업지시서 내용대로 docs/06_Dooly_v1.html 수정

## 3. git push
cd C:\Obsidian\Dooly
git add .
git commit -m "fix: Gemini 출처 번호 표시 수정 (FAQ Q1, SOP 1 형식)"
git push
```

---

## 테스트

1. Dooly 챗봇 열기
2. "복사기 종이 먹었어요" 질문
3. 답변 하단 태그 확인:
   - ✅ `FAQ Q1` (초록 태그)
   - ✅ `SOP 1` (주황 태그)
   - ❌ "복사기가 종이를 먹었어요" 텍스트 없어야 함
   - ❌ "복사기/스캔 SOP" 카테고리명 없어야 함

---

## 완료 기준

- [ ] FAQ 태그: `FAQ Q숫자` 형식으로 표시
- [ ] SOP 태그: `SOP 숫자` 형식으로 표시
- [ ] 제목/카테고리명 미표시 확인
- [ ] git push 완료

---

## END OF ORDER
