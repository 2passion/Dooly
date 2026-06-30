# 52H_Order_Source_Tag_Fix_v1.0.md

작성일: 2026-06-30
작업 번호: Task #52-H
작업명: AI 답변 잘림 수정
대상 파일: docs/api/gemini.js, docs/06_Dooly_v1.html
선행 조건: Task #52-G 완료 (커밋 ed8f884)

---

## 수정 범위

Mock 모드 출처 태그는 현재 정상 동작 중 → 수정하지 않음
AI(Gemini) 모드 답변이 중간에 잘리는 문제만 수정한다.

---

## 문제 — AI 모드 답변이 중간에 잘림

### 현재 (문제)
```
"복사기 종이"에 대해 어떤 점이 궁금하신가요?
만약 복사기 종이를 먹었거나 종이 걸림이 발생했다면, 구
```
"구" 에서 답변이 끊김.

### 원인
`docs/api/gemini.js` 의 `maxOutputTokens` 값이 너무 낮거나
응답 파싱 시 텍스트를 자르는 코드가 있을 가능성.

---

## 수정 1 — docs/api/gemini.js

`maxOutputTokens` 값을 찾아서 2048로 올린다.

**찾을 패턴:**
```javascript
maxOutputTokens: 500
// 또는
maxOutputTokens: 800
// 또는 유사한 낮은 값
```

**교체:**
```javascript
maxOutputTokens: 2048
```

값이 없으면 `generationConfig` 블록 안에 추가:
```javascript
generationConfig: {
  maxOutputTokens: 2048,
  temperature: 0.7
}
```

`generationConfig` 블록 자체가 없으면 신규 추가:
```javascript
const requestBody = {
  contents: [...],
  generationConfig: {
    maxOutputTokens: 2048,
    temperature: 0.7
  }
};
```

---

## 수정 2 — docs/06_Dooly_v1.html 응답 파싱 확인

Gemini 응답에서 텍스트를 추출하는 부분을 찾는다.

**찾을 패턴:**
```javascript
data.candidates[0].content.parts[0].text
```

이 값을 `substring`, `slice`, `substr` 등으로 자르는 코드가 있으면 제거한다.

없으면 수정하지 않는다.

---

## 파일 정리 (Claude Code 프롬프트 템플릿)

```
아래 작업을 순서대로 실행해줘.

## 1. 작업지시서 이동
C:\Users\USER\Downloads\52H_Order_Source_Tag_Fix_v1.0.md 파일을
C:\Obsidian\Dooly\03_Claude_Code\52H_Order_Source_Tag_Fix_v1.0.md 로 이동

## 2. 작업 실행
위 작업지시서 내용대로
docs/api/gemini.js 와 docs/06_Dooly_v1.html 수정

## 3. git push
cd C:\Obsidian\Dooly
git add .
git commit -m "fix: AI 답변 잘림 수정 (maxOutputTokens 2048)"
git push
```

---

## 테스트

1. Dooly 챗봇 → Gemini AI 모드
2. "복사기 종이 먹었어요" 질문
3. 답변이 끊기지 않고 완전한 문장으로 출력되는지 확인

---

## 완료 기준

- [ ] AI 답변이 잘리지 않고 완전하게 출력됨
- [ ] git push 완료 확인

---

## END OF ORDER
