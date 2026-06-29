# 52_Order_PWA_Icon_Gemini_Fix_v1.0.md
# Task #52 — PWA 아이콘 교체 + Gemini 출처 번호 + 말풍선 색상 수정

작성일: 2026-06-29
작업자: Claude Code
우선순위: 높음

---

## 1. 작업 개요

| 번호 | 항목 | 내용 |
|------|------|------|
| 52-A | PWA 아이콘 교체 | 새 공룡 아이콘(흰색 배경)으로 교체 |
| 52-B | manifest.json 경로 수정 | Vercel Root Directory(docs/) 기준으로 아이콘 경로 수정 |
| 52-C | Gemini 출처 번호 표시 | 시스템 프롬프트 수정 → FAQ Q1, SOP 10 형식 출처 표시 |
| 52-D | 질문 말풍선 텍스트 색상 | 파란 배경 + 파란 텍스트 → 파란 배경 + 흰색 텍스트 |

---

## 2. 수정 대상 파일 경로

```
C:\Obsidian\Dooly\
├── docs\
│   ├── manifest.json              ← 52-B: 아이콘 경로 수정
│   ├── icons\
│   │   ├── icon-192x192.png       ← 52-A: 새 아이콘 파일 복사
│   │   └── icon-512x512.png       ← 52-A: 새 아이콘 파일 복사
│   ├── api\
│   │   └── gemini.js              ← 52-C: 시스템 프롬프트 수정
│   └── 06_Dooly_v1.html           ← 52-D: 말풍선 CSS 수정
```

---

## 52-A: PWA 아이콘 파일 교체

### 작업 내용

다운로드 폴더의 아이콘 파일을 docs/icons/ 폴더로 복사한다.

```
C:\Users\USER\Downloads\icon-192x192.png → C:\Obsidian\Dooly\docs\icons\icon-192x192.png
C:\Users\USER\Downloads\icon-512x512.png → C:\Obsidian\Dooly\docs\icons\icon-512x512.png
```

> ⚠️ 아이콘 파일(icon-192x192.png, icon-512x512.png)은 claude.ai에서 다운로드한 파일을 사용한다.

### PowerShell 명령어

```powershell
Copy-Item "C:\Users\USER\Downloads\icon-192x192.png" "C:\Obsidian\Dooly\docs\icons\icon-192x192.png" -Force
Copy-Item "C:\Users\USER\Downloads\icon-512x512.png" "C:\Obsidian\Dooly\docs\icons\icon-512x512.png" -Force
```

---

## 52-B: manifest.json 아이콘 경로 수정

### 파일 경로
```
C:\Obsidian\Dooly\docs\manifest.json
```

### 전체 내용으로 덮어쓰기

```json
{
  "name": "둘리 (Dooly)",
  "short_name": "둘리",
  "description": "킹수학 조교 AI 비서",
  "start_url": "/06_Dooly_v1.html",
  "display": "standalone",
  "background_color": "#0b0f1a",
  "theme_color": "#4da3ff",
  "icons": [
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
```

---

## 52-C: Gemini 시스템 프롬프트 수정 (출처 번호 표시)

### 파일 경로
```
C:\Obsidian\Dooly\docs\api\gemini.js
```

### 수정 내용

시스템 프롬프트(systemPrompt 변수)에 아래 지시를 추가한다.

#### 기존 시스템 프롬프트 끝 부분 찾기
```
당신은 킹수학 학원의 AI 비서 둘리(Dooly)입니다.
```
(실제 파일의 systemPrompt 변수 내용 끝에 아래 내용 추가)

#### 추가할 내용
```
답변 시 반드시 참고한 항목을 명시하라.
형식 예시: [FAQ Q1], [SOP 10], [SOP 21]
참고한 항목이 없거나 불확실한 경우 "확인이 필요합니다."라고 답변하라.
출처는 답변 마지막에 "참고: [FAQ Q1], [SOP 10]" 형식으로 표시하라.
```

> ⚠️ systemPrompt 변수의 실제 위치를 파일에서 확인 후 적용한다.

---

## 52-D: 질문 말풍선 텍스트 색상 수정

### 파일 경로
```
C:\Obsidian\Dooly\docs\06_Dooly_v1.html
```

### 수정 내용

말풍선 CSS에서 사용자 메시지(user-message) 텍스트 색상을 흰색으로 변경한다.

#### 기존 코드 (파일에서 검색)
```css
.user-message {
```

#### 추가/수정할 속성
```css
.user-message {
  color: #ffffff;          /* 추가: 흰색 텍스트 */
  -webkit-user-select: text;
  user-select: text;       /* 추가: 꾹 눌러서 복사 가능 */
}
```

> ⚠️ 기존 `.user-message` CSS 블록을 찾아 위 속성을 추가한다. 기존 속성은 유지한다.

---

## 3. Git 커밋

모든 작업 완료 후:

```bash
cd C:\Obsidian\Dooly
git add .
git commit -m "feat: PWA 아이콘 교체 + Gemini 출처 표시 + 말풍선 색상 수정"
git push
```

---

## 4. 작업 완료 확인

| 항목 | 확인 방법 |
|------|-----------|
| 52-A 아이콘 | docs/icons/ 폴더에 파일 존재 확인 |
| 52-B manifest | JSON 문법 오류 없는지 확인 |
| 52-C Gemini 출처 | Vercel 배포 후 Dooly에 질문 → 출처 번호 표시 확인 |
| 52-D 말풍선 | 질문 입력 후 파란 배경에 흰 텍스트 확인 |
| PWA 아이콘 | PWA 재설치 후 홈 화면 아이콘 확인 |

---

## 5. 주의사항

- Vercel은 git push 후 자동 배포 (1~2분 소요)
- PWA 아이콘 변경은 **기존 설치된 PWA 삭제 후 재설치** 필요
- manifest.json의 `start_url`은 `/06_Dooly_v1.html` (Vercel Root = docs/ 기준)
- 아이콘 경로 `/icons/...` 는 Vercel에서 `docs/icons/...` 로 자동 매핑됨

---

## END OF TASK #52
