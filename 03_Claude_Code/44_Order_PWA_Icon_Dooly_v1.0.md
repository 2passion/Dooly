# 44_Order_PWA_Icon_Dooly_v1.0.md
# King Assistant OS v1.0
# Claude Code 작업지시서

Version: v1.0
Date: 2026-06-28

---

# 작업 배경

43번 작업이 STEP 2까지 완료됨.
- service-worker.js 생성 완료 ✅
- icon-192.png, icon-512.png 임시 생성 완료 ✅
- docs/index.html SW 등록 코드 추가 미완료 ❌

이번 작업:
1. 아이콘을 공룡(Dooly) 스타일로 교체
2. 앱 이름 KING → Dooly로 수정
3. docs/index.html SW 등록 코드 추가 (43번 미완료 부분)
4. 04_Runtime 동기화
5. git push

---

# STEP 1 — 공룡 아이콘 생성 (Python)

## 실행 위치

```
cd C:\Obsidian\Dooly
```

## 실행 명령어

```python
python -c "
import struct, zlib, os, math

def make_png(size, filename):
    def chunk(name, data):
        c = name + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    pixels = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            cx, cy = size / 2, size / 2
            dx, dy = x - cx, y - cy
            dist = math.sqrt(dx*dx + dy*dy)
            r = size / 2

            # 흰색 원형 배경
            if dist > r:
                row.extend([240, 240, 240])
                continue

            # 공룡 그리기 (단순 실루엣)
            nx = (x / size)
            ny = (y / size)

            # 몸통 (타원)
            bx, by = 0.5, 0.58
            body = ((nx - bx)/0.22)**2 + ((ny - by)/0.28)**2 < 1

            # 머리 (원)
            hx, hy = 0.62, 0.32
            head = ((nx - hx)/0.16)**2 + ((ny - hy)/0.14)**2 < 1

            # 꼬리 (삼각형 영역)
            tail = (nx < 0.32 and ny > 0.52 and ny < 0.75 and
                    nx > 0.15 and (ny - 0.75) < (nx - 0.15) * 1.2)

            # 앞발
            arm = ((nx - 0.63)/0.07)**2 + ((ny - 0.54)/0.06)**2 < 1

            # 뒷발 왼쪽
            leg1 = ((nx - 0.42)/0.08)**2 + ((ny - 0.84)/0.07)**2 < 1
            # 뒷발 오른쪽
            leg2 = ((nx - 0.58)/0.08)**2 + ((ny - 0.84)/0.07)**2 < 1

            # 눈
            eye = ((nx - 0.67)/0.03)**2 + ((ny - 0.27)/0.03)**2 < 1

            # 배 (밝은 색)
            belly = ((nx - 0.54)/0.12)**2 + ((ny - 0.60)/0.18)**2 < 1

            if eye:
                row.extend([30, 30, 30])        # 눈: 거의 검정
            elif belly and body:
                row.extend([200, 230, 180])     # 배: 연한 초록
            elif body or head or tail or arm or leg1 or leg2:
                row.extend([60, 160, 70])       # 몸: 초록
            else:
                row.extend([255, 255, 255])     # 배경: 흰색

        pixels.append(bytes(row))

    raw = b''.join(pixels)
    compressed = zlib.compress(raw)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', compressed)
    png += chunk(b'IEND', b'')

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(png)
    print('생성 완료:', filename)

make_png(192, 'docs/icons/icon-192.png')
make_png(512, 'docs/icons/icon-512.png')
make_png(192, '04_Runtime/icons/icon-192.png')
make_png(512, '04_Runtime/icons/icon-512.png')
"
```

## 완료 확인

```
✅ docs\icons\icon-192.png 생성됨 (공룡 아이콘)
✅ docs\icons\icon-512.png 생성됨 (공룡 아이콘)
✅ 04_Runtime\icons\icon-192.png 생성됨
✅ 04_Runtime\icons\icon-512.png 생성됨
```

---

# STEP 2 — 앱 이름 KING → Dooly 수정

## 2-1. docs/manifest.json 수정

찾을 부분:
```json
"name": "KING Assistant OS",
"short_name": "KING",
```

변경 후:
```json
"name": "Dooly",
"short_name": "Dooly",
```

## 2-2. 04_Runtime/manifest.json 수정

동일하게 수정:
```json
"name": "Dooly",
"short_name": "Dooly",
```

---

# STEP 3 — docs/index.html SW 등록 코드 추가

## 수정 대상

```
C:\Obsidian\Dooly\docs\index.html
```

## 찾을 부분

```html
</body>
```

## </body> 바로 앞에 추가

```html
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
      navigator.serviceWorker.register('/Dooly/service-worker.js')
        .then(function(reg) { console.log('SW registered'); })
        .catch(function(err) { console.log('SW error:', err); });
    });
  }
</script>
</body>
```

---

# STEP 4 — 04_Runtime 동기화

```
copy docs\service-worker.js 04_Runtime\service-worker.js
```

04_Runtime\index.html 에도 SW 등록 코드 추가:

찾을 부분:
```html
</body>
```

추가할 내용:
```html
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
      navigator.serviceWorker.register('/service-worker.js')
        .then(function(reg) { console.log('SW registered'); })
        .catch(function(err) { console.log('SW error:', err); });
    });
  }
</script>
</body>
```

---

# STEP 5 — git 커밋 및 push

```
cd C:\Obsidian\Dooly

git add .
git commit -m "feat: PWA 공룡 아이콘 + 앱 이름 Dooly 변경"
git push
```

---

# 전체 작업 완료 조건

```
✅ STEP 1 완료 (공룡 아이콘 생성)
✅ STEP 2 완료 (앱 이름 Dooly 변경)
✅ STEP 3 완료 (docs/index.html SW 등록)
✅ STEP 4 완료 (04_Runtime 동기화)
✅ STEP 5 완료 (git push)
```

---

# STEP 6 — PWA 설치 테스트 (직접 진행)

## 갤럭시 Chrome

```
1~2분 후 GitHub Pages 배포 완료 대기

Chrome에서:
https://2passion.github.io/Dooly/ 접속
→ 주소창 오른쪽 설치 아이콘(⊕) 클릭
  또는 메뉴(⋮) → "앱 설치"
→ 홈 화면에 Dooly 공룡 아이콘 생성 확인
→ 아이콘 클릭 → 앱처럼 실행 확인
```

## 아이폰 Safari

```
Safari에서:
https://2passion.github.io/Dooly/ 접속
→ 하단 공유 버튼(□↑) 클릭
→ "홈 화면에 추가" 클릭
→ 이름: Dooly 확인 후 "추가"
→ 홈 화면에 Dooly 아이콘 생성 확인
```

---

# 다음 작업

45번 → PWA 설치 테스트 결과 확인 및 수정

---

# END OF ORDER
