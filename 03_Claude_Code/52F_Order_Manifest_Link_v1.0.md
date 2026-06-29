# 52F_Order_Manifest_Link_v1.0.md
# Task #52-F — manifest.json 링크 태그 추가 (PWA 아이콘 수정)

작성일: 2026-06-29
작업자: Claude Code
우선순위: 높음

---

## 1. 작업 개요

| 번호 | 항목 | 내용 |
|------|------|------|
| 52-F | manifest 링크 태그 추가 | 06_Dooly_v1.html `<head>`에 manifest 연결 태그 추가 |

### 원인
F12 → Application → Manifest에서 "No manifest detected" 확인.
`06_Dooly_v1.html`의 `<head>` 안에 manifest.json 연결 태그가 없어서
브라우저가 PWA manifest를 인식하지 못하고 기본 아이콘(V)을 표시함.

---

## 2. 수정 대상 파일

```
C:\Obsidian\Dooly\docs\06_Dooly_v1.html
```

---

## 3. 수정 내용

### 찾을 코드
`06_Dooly_v1.html` 파일에서 `<head>` 태그 안의 아무 `<meta>` 태그 바로 아래를 찾는다.

예시:
```html
<head>
  <meta charset="UTF-8">
```

### 추가할 코드
`<meta charset="UTF-8">` 바로 다음 줄에 아래 3줄을 추가한다:

```html
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#0b0f1a">
  <meta name="apple-mobile-web-app-capable" content="yes">
```

### 최종 결과 예시
```html
<head>
  <meta charset="UTF-8">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#0b0f1a">
  <meta name="apple-mobile-web-app-capable" content="yes">
```

---

## 4. Git 커밋

```bash
cd C:\Obsidian\Dooly
git add .
git commit -m "fix: manifest 링크 태그 추가 → PWA 아이콘 수정"
git push
```

---

## 5. 작업 완료 확인

| 항목 | 확인 방법 |
|------|-----------|
| manifest 인식 | F12 → Application → Manifest → 아이콘 미리보기 표시 확인 |
| PWA 아이콘 | 홈 화면 기존 둘리 삭제 → 재설치 → 공룡 아이콘 확인 |

---

## END OF TASK #52-F
