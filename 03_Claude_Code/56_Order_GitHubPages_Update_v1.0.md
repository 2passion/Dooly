# 56_Order_GitHubPages_Update_v1.0.md
# King Assistant OS v2.0
# 작업지시서 #56 — GitHub Pages 최신버전 업데이트

작성일: 2026-06-30
우선순위: 낮음
전제조건: Task #53 완료 (커밋 82d593a)

---

## 1. 작업 개요

### 목적
GitHub Pages가 구버전 상태로 방치되어 있어 현재 Vercel 운영 버전과 동기화한다.

### 배경
- 운영 URL: https://dooly-eight.vercel.app (Vercel — 최신)
- Pages URL: https://2passion.github.io/Dooly (GitHub Pages — 구버전)
- Vercel 이전(Task #51) 이후 GitHub Pages 설정이 갱신되지 않은 상태

### 작업 범위
1. GitHub Pages 현재 설정 확인
2. Pages 빌드 소스를 `main` 브랜치 `docs/` 폴더로 지정
3. `docs/` 폴더에 Pages용 진입점(index.html) 존재 여부 확인
4. 필요 시 리다이렉트 또는 안내 페이지 추가
5. git push → Pages 자동 빌드 확인

---

## 2. 사전 확인 사항

Claude Code 실행 전 아래를 먼저 점검한다.

```
# 현재 repo 루트 및 docs/ 구조 확인
cd C:\Obsidian\Dooly
dir
dir docs
```

확인 항목:
- `docs/` 폴더 존재 여부
- `docs/index.html` 존재 여부
- `docs/api/` 폴더 존재 여부 (Vercel 프록시 파일들)

---

## 3. Step 1 — GitHub Pages 설정 확인 (브라우저에서 수동 확인)

Claude Code에서 실행하지 않고, 킹스가 직접 브라우저에서 확인한다.

```
브라우저 → https://github.com/2passion/Dooly
→ Settings 탭 → Pages 메뉴
→ Source 항목 확인:
    Branch: main
    Folder: /docs
```

설정이 위와 다르면 수동으로 변경 후 Save 클릭.

---

## 4. Step 2 — docs/ 폴더 진입점 확인 및 생성

### 4-1. docs/index.html 존재 확인

```
type C:\Obsidian\Dooly\docs\index.html
```

존재하면 → Step 3으로 이동
존재하지 않으면 → 4-2 실행

### 4-2. docs/index.html 생성 (없는 경우에만)

`C:\Obsidian\Dooly\docs\index.html` 파일을 아래 내용으로 생성한다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>King Assistant OS — Dooly</title>
  <meta http-equiv="refresh" content="0; url=https://dooly-eight.vercel.app">
  <style>
    body {
      font-family: sans-serif;
      background: #0b0f1a;
      color: #c0c8d8;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
      text-align: center;
    }
    a { color: #4da3ff; }
  </style>
</head>
<body>
  <div>
    <p>Dooly로 이동 중...</p>
    <p><a href="https://dooly-eight.vercel.app">바로가기</a></p>
  </div>
</body>
</html>
```

---

## 5. Step 3 — git push 및 Pages 빌드 트리거

```
cd C:\Obsidian\Dooly
git add docs/index.html
git commit -m "docs: GitHub Pages 진입점 추가 — Vercel로 리다이렉트"
git push
```

index.html이 이미 존재하여 변경사항이 없는 경우:

```
cd C:\Obsidian\Dooly
git commit --allow-empty -m "chore: GitHub Pages 빌드 재트리거"
git push
```

---

## 6. Step 4 — 빌드 결과 확인 (브라우저에서 수동 확인)

push 후 약 1~3분 대기 후 확인.

```
브라우저 → https://github.com/2passion/Dooly
→ Actions 탭 → pages build and deployment 워크플로우 확인
→ 녹색 체크 확인 후
→ https://2passion.github.io/Dooly 접속 확인
```

기대 결과:
- 페이지가 정상 로드되거나
- https://dooly-eight.vercel.app 으로 자동 리다이렉트됨

---

## 7. 완료 후 파일 정리

```
cd C:\Obsidian\Dooly

## 작업지시서 자기 자신 이동 (이미 이동된 경우 생략)
move "C:\Users\USER\Downloads\56_Order_GitHubPages_Update_v1.0.md" "C:\Obsidian\Dooly\03_Claude_Code\56_Order_GitHubPages_Update_v1.0.md"

## SESSION_HANDOVER 백업
copy "00_System\02_SESSION_HANDOVER.md" "00_System\HANDOVER_HISTORY\18_SESSION_HANDOVER_v14.0.md"

git add .
git commit -m "docs: Task #56 완료 — GitHub Pages 최신버전 업데이트"
git push
```

---

## 8. 완료 기준

| 항목 | 확인 방법 |
|------|-----------|
| Pages Source 설정: main/docs | GitHub Settings → Pages |
| docs/index.html 존재 | dir docs 확인 |
| git push 완료 | GitHub Actions 녹색 체크 |
| Pages URL 접속 가능 | 브라우저에서 https://2passion.github.io/Dooly |

---

## 9. 주의사항

- `docs/api/` 폴더 안의 Vercel 프록시 파일(gemini.js, tasks.js)은 GitHub Pages에서 실행되지 않는다. Pages는 정적 HTML만 서빙하며 Node.js 런타임을 지원하지 않는다.
- Pages URL은 운영용이 아닌 보조 접근 경로로만 활용한다. 실제 운영은 Vercel URL을 사용한다.
- Vercel Root Directory가 `docs`로 설정되어 있으므로 `docs/` 폴더 내 파일 수정이 곧 Vercel 배포에도 영향을 준다. 불필요한 파일을 추가하지 않는다.

---

# END OF ORDER #56
