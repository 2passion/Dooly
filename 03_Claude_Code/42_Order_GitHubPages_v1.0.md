# 42_Order_GitHubPages_v1.0.md
# King Assistant OS v1.0
# Claude Code 작업지시서

Version: v1.0
Date: 2026-06-27

---

# 작업 시작 전 필수 확인

아래 파일을 읽어라.

```
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md
```

---

# 작업 목표

GitHub Pages 배포 설정
→ server.py 없이 HTML 파일을 직접 서빙
→ 24시간 항상 접속 가능
→ 자습실 PC, ngrok 불필요

---

# 배경 설명

현재 구조:
```
04_Runtime\
├── index.html
├── 02_Task_v1.html
├── 03_SOP_v1.html
├── 04_FAQ_v1.html
├── 05_Notice_v1.html
├── 06_Dooly_v1.html
├── 07_Settings_v1.html
├── data.js
├── manifest.json
└── icons\
```

GitHub Pages는 루트(/) 또는 docs/ 폴더를 기준으로 서빙한다.
현재 파일들이 04_Runtime\ 안에 있어서
GitHub Pages가 읽으려면 docs\ 폴더로 복사해야 한다.

변경 후 구조:
```
docs\               ← GitHub Pages 서빙 폴더
├── index.html
├── 02_Task_v1.html
├── 03_SOP_v1.html
├── 04_FAQ_v1.html
├── 05_Notice_v1.html
├── 06_Dooly_v1.html
├── 07_Settings_v1.html
├── data.js
├── manifest.json
└── icons\
```

---

# STEP 1 — docs 폴더 생성 및 파일 복사

## 실행 명령어

```
cd C:\Obsidian\Dooly

# docs 폴더 생성
mkdir docs
mkdir docs\icons

# 04_Runtime 파일 전체 복사
copy 04_Runtime\index.html docs\index.html
copy 04_Runtime\02_Task_v1.html docs\02_Task_v1.html
copy 04_Runtime\03_SOP_v1.html docs\03_SOP_v1.html
copy 04_Runtime\04_FAQ_v1.html docs\04_FAQ_v1.html
copy 04_Runtime\05_Notice_v1.html docs\05_Notice_v1.html
copy 04_Runtime\06_Dooly_v1.html docs\06_Dooly_v1.html
copy 04_Runtime\07_Settings_v1.html docs\07_Settings_v1.html
copy 04_Runtime\data.js docs\data.js
copy 04_Runtime\manifest.json docs\manifest.json
```

## 완료 확인

```
✅ docs\ 폴더 생성됨
✅ docs\ 안에 HTML 7개 + data.js + manifest.json 복사됨
✅ docs\icons\ 폴더 생성됨
```

---

# STEP 2 — docs 폴더의 manifest.json 수정

## 수정 대상

```
C:\Obsidian\Dooly\docs\manifest.json
```

## 현재 내용

```json
{
  "start_url": "/app",
  ...
}
```

## 변경 후 내용

GitHub Pages 주소 기준으로 수정한다.

```json
{
  "name": "KING Assistant OS",
  "short_name": "KING",
  "description": "킹수학 조교 운영 시스템",
  "start_url": "/Dooly/",
  "scope": "/Dooly/",
  "display": "standalone",
  "background_color": "#0b0f1a",
  "theme_color": "#4da3ff",
  "orientation": "portrait",
  "icons": [
    {
      "src": "/Dooly/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/Dooly/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

---

# STEP 3 — docs 폴더의 index.html manifest 링크 수정

## 수정 대상

```
C:\Obsidian\Dooly\docs\index.html
```

## 찾을 부분

```html
<link rel="manifest" href="/manifest.json">
```

## 변경 후

```html
<link rel="manifest" href="/Dooly/manifest.json">
```

---

# STEP 4 — .gitignore 확인

docs\ 폴더가 git에 포함되는지 확인한다.
.gitignore에 docs/ 가 있으면 제거한다.
없으면 그대로 진행한다.

---

# STEP 5 — git 커밋 및 push

```
cd C:\Obsidian\Dooly

git add .
git commit -m "feat: GitHub Pages 배포용 docs 폴더 추가"
git push
```

---

# STEP 6 — GitHub Pages 설정 안내

## Claude Code가 할 수 없는 작업 (브라우저에서 직접 진행)

아래 순서대로 GitHub에서 설정한다:

```
1. https://github.com/2passion/Dooly 접속

2. Settings 탭 클릭

3. 왼쪽 메뉴에서 Pages 클릭

4. Source 설정:
   Branch: main
   Folder: /docs
   Save 클릭

5. 잠시 후 아래 주소로 접속 확인:
   https://2passion.github.io/Dooly/
```

---

# 전체 작업 완료 조건

```
✅ STEP 1 완료 (docs 폴더 생성 + 파일 복사)
✅ STEP 2 완료 (manifest.json 경로 수정)
✅ STEP 3 완료 (index.html manifest 링크 수정)
✅ STEP 5 완료 (git push)
✅ STEP 6 완료 (GitHub Pages 설정)

✅ https://2passion.github.io/Dooly/ 접속 확인
✅ Dooly 탭에서 Mock 모드 답변 확인
```

---

# 배포 후 접속 주소

| 환경 | 주소 |
|---|---|
| GitHub Pages | https://2passion.github.io/Dooly/ |
| 기존 ngrok | https://polymer-distinct-feminize.ngrok-free.dev/app |

※ GitHub Pages 배포 확인 후 ngrok은 더 이상 사용하지 않아도 됩니다.

---

# 다음 작업

43번 → PWA service-worker.js + 아이콘 추가
        (docs 폴더 기준으로 작업)

---

# END OF ORDER
