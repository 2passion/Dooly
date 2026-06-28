# 48B_Order_Task_API_PWA_v1.1.md
# King Assistant OS v1.0
# 작업지시서 #48B 수정 — PWA Task API IP 주소 수정

작성일: 2026-06-28
실행 위치: 노트북(화이트) Claude Code
우선순위: 높음

---

## 1. 작업 개요

02_Task_v1.html 안의 API_BASE IP 주소를 수정한다.

| 항목 | 내용 |
|------|------|
| 수정 전 | http://192.168.219.100:8001 |
| 수정 후 | http://192.168.0.10:8001 |

---

## 2. 수정 파일

- C:\Obsidian\Dooly\04_Runtime\02_Task_v1.html
- C:\Obsidian\Dooly\docs\02_Task_v1.html

---

## 3. 작업 내용

### Step 1 — 04_Runtime\02_Task_v1.html 수정

아래 한 줄을 찾아서 교체한다.

수정 전:
```
const API_BASE = "http://192.168.219.100:8001";
```

수정 후:
```
const API_BASE = "http://192.168.0.10:8001";
```

---

### Step 2 — docs 폴더 동기화

```
copy C:\Obsidian\Dooly\04_Runtime\02_Task_v1.html C:\Obsidian\Dooly\docs\02_Task_v1.html
```

---

### Step 3 — git push

```
cd C:\Obsidian\Dooly
git add .
git commit -m "fix: Task API IP 주소 수정 192.168.219.100 → 192.168.0.10 (#48B-fix)"
git push
```

---

## 4. 완료 확인

- [ ] 04_Runtime\02_Task_v1.html IP 수정 확인
- [ ] docs\02_Task_v1.html 동기화 확인
- [ ] git push 완료 확인
- [ ] 스마트폰 PWA에서 🟢 온라인 표시 확인
