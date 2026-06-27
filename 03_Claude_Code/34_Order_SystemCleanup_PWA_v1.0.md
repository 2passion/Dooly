# 34_Order_SystemCleanup_PWA_v1.0.md
# King Assistant OS v1.0
# Claude Code 작업지시서

Version: v1.0
Date: 2026-06-27

---

# 작업 시작 전 필수 확인

아래 파일을 순서대로 읽어라.

```
C:\Obsidian\Dooly\00_System\01_PROJECT_MASTER.md
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md
C:\Obsidian\Dooly\00_System\03_DEVELOPMENT_RULE_v1.0.md
```

---

# 작업 목표

1. 파일명 버전 표기 통일 (v1_0 → v1.0)
2. 인수인계 파일 최신화 및 히스토리 보관
3. PWA 전환 1단계 (manifest.json) 생성

작업은 반드시 아래 순서대로 진행한다.
한 STEP 완료 후 다음 STEP으로 넘어간다.

---

# STEP 1 — 파일명 버전 표기 통일

## 작업 내용

00_System 폴더 내 파일명의 버전 표기를 규칙에 맞게 수정한다.

```
규칙: v1.0 (점 사용)
현재: v1_0 (언더스코어 사용) → 수정 대상
```

## 수정 대상 파일

| 현재 파일명 | 변경할 파일명 |
|---|---|
| 03_DEVELOPMENT_RULE_v1_0.md | 03_DEVELOPMENT_RULE_v1.0.md |
| 04_PROJECT_GUIDE_v1_0.md | 04_PROJECT_GUIDE_v1.0.md |

## 실행 명령어

```
cd C:\Obsidian\Dooly

git mv "00_System\03_DEVELOPMENT_RULE_v1_0.md" "00_System\03_DEVELOPMENT_RULE_v1.0.md"
git mv "00_System\04_PROJECT_GUIDE_v1_0.md" "00_System\04_PROJECT_GUIDE_v1.0.md"

git add .
git commit -m "docs: fix filename version format v1_0 → v1.0"
git push
```

## 완료 확인

```
✅ 00_System\03_DEVELOPMENT_RULE_v1.0.md 존재
✅ 00_System\04_PROJECT_GUIDE_v1.0.md 존재
✅ v1_0 형식 파일 없음
✅ git push 완료
```

---

# STEP 2 — 인수인계 파일 정리

## 작업 내용

현재 02_SESSION_HANDOVER.md 를 히스토리로 보관하고,
최신 인수인계 파일(v4.0)로 덮어쓴다.

```
구조 원칙:
02_SESSION_HANDOVER.md     → 항상 최신 버전만 유지
HANDOVER_HISTORY\          → 이전 버전 시간순 보관
```

## 실행 순서

### 작업 1 — 현재 파일을 히스토리로 복사

현재 C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md 파일을
C:\Obsidian\Dooly\00_System\HANDOVER_HISTORY\08_SESSION_HANDOVER_v4.0.md 로 복사해줘.

```
copy "C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md" "C:\Obsidian\Dooly\00_System\HANDOVER_HISTORY\08_SESSION_HANDOVER_v4.0.md"
```

기존 02_SESSION_HANDOVER.md 는 수정하지 않는다.

### 작업 2 — 최신 인수인계 내용으로 덮어쓰기

C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md 파일을
아래 경로의 파일 내용으로 덮어써줘.

```
원본 파일:
C:\Obsidian\Dooly\99_Archive\2 구현-클로드\2 클로드 대화-2\6 인수인계\02_SESSION_HANDOVER_FINAL.md
```

### 작업 3 — git 커밋

```
cd C:\Obsidian\Dooly

git add .
git commit -m "docs: SESSION_HANDOVER v4.0 업데이트 + HANDOVER_HISTORY 보관"
git push
```

## 완료 확인

```
✅ HANDOVER_HISTORY\08_SESSION_HANDOVER_v4.0.md 생성됨
✅ 02_SESSION_HANDOVER.md 내용이 v4.0으로 업데이트됨
✅ git push 완료
```

---

# STEP 3 — PWA 전환 1단계 (manifest.json)

## 작업 개요

PWA 전환 1단계: manifest.json 생성 및 FastAPI 연동
앱 이름, 아이콘, 시작 URL, 표시 모드, 테마 색상 정의

## 수정 대상 파일

| 구분 | 경로 |
|---|---|
| 신규 | C:\Obsidian\Dooly\04_Runtime\manifest.json |
| 신규 | C:\Obsidian\Dooly\04_Runtime\icons\ 폴더 |
| 수정 | C:\Obsidian\Dooly\05_RAG\server.py |
| 수정 | C:\Obsidian\Dooly\04_Runtime\index.html |

## 작업 내용

### 작업 1 — manifest.json 생성

경로: C:\Obsidian\Dooly\04_Runtime\manifest.json

```json
{
  "name": "KING Assistant OS",
  "short_name": "KING",
  "description": "킹수학 조교 운영 시스템",
  "start_url": "/app",
  "display": "standalone",
  "background_color": "#0b0f1a",
  "theme_color": "#4da3ff",
  "orientation": "portrait",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### 작업 2 — server.py 수정

기존 라우트 아래에 아래 3개 라우트를 추가한다.

```python
@app.get("/manifest.json")
async def manifest():
    return FileResponse(RUNTIME_DIR / "manifest.json", media_type="application/manifest+json")

@app.get("/service-worker.js")
async def service_worker():
    return FileResponse(RUNTIME_DIR / "service-worker.js", media_type="application/javascript")

@app.get("/icons/{filename}")
async def icons(filename: str):
    return FileResponse(RUNTIME_DIR / "icons" / filename)
```

주의: FileResponse 가 import 되어 있는지 확인하고, 없으면 추가한다.

```python
from fastapi.responses import FileResponse, RedirectResponse
```

### 작업 3 — index.html 수정

index.html 의 `<head>` 안에 아래 내용을 추가한다.

```html
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#4da3ff">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="KING">
```

### 작업 4 — icons 폴더 생성

아래 폴더를 생성한다. (아이콘 PNG 파일은 35번 작업에서 추가)

```
C:\Obsidian\Dooly\04_Runtime\icons\
```

### 작업 5 — git 커밋

```
cd C:\Obsidian\Dooly

git add .
git commit -m "feat: PWA manifest.json + FastAPI route + index.html meta tags"
git push
```

## 완료 확인

```
✅ 04_Runtime\manifest.json 생성됨
✅ 04_Runtime\icons\ 폴더 생성됨
✅ server.py 에 3개 라우트 추가됨
✅ index.html <head> 에 PWA 메타태그 추가됨
✅ http://localhost:8001/manifest.json 접속 시 JSON 응답 확인
✅ git push 완료
```

---

# 전체 작업 완료 조건

```
✅ STEP 1 완료 (파일명 v1.0 통일)
✅ STEP 2 완료 (인수인계 최신화)
✅ STEP 3 완료 (PWA manifest 생성)
✅ 모든 STEP git push 완료
```

---

# 세션 종료 전 필수

```
1. 02_SESSION_HANDOVER.md 업데이트 확인
2. git add .
3. git commit -m "docs: 34번 작업 완료"
4. git push
```

---

# 다음 작업

35_Order_PWA_ServiceWorker_v1.0.md
→ service-worker.js 생성 + 아이콘 파일 추가

---

# END OF ORDER
