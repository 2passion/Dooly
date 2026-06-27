# 43_Order_PWA_ServiceWorker_v1.0.md
# King Assistant OS v1.0
# Claude Code 작업지시서

Version: v1.0
Date: 2026-06-28

---

# 작업 시작 전 필수 확인

아래 파일을 읽어라.

```
C:\Obsidian\Dooly\00_System\02_SESSION_HANDOVER.md
```

---

# 작업 목표

PWA 완성: service-worker.js + 아이콘 생성
→ 갤럭시/아이폰 홈 화면에 앱 설치 가능

---

# 배경

현재 상태:
```
docs\manifest.json ✅ (42번에서 완료)
docs\icons\ 폴더  ✅ (비어있음)
service-worker.js  ❌ (없음)
아이콘 PNG 파일    ❌ (없음)
```

이번 작업:
```
docs\service-worker.js  ← 신규 생성
docs\icons\icon-192.png ← 신규 생성 (Python으로 생성)
docs\icons\icon-512.png ← 신규 생성 (Python으로 생성)
docs\index.html         ← service-worker 등록 코드 추가
```

---

# STEP 1 — service-worker.js 생성

## 생성 경로

```
C:\Obsidian\Dooly\docs\service-worker.js
```

## 파일 내용

```javascript
// service-worker.js
// King Assistant OS v1.0 PWA

const CACHE_NAME = 'king-assistant-v1';
const URLS_TO_CACHE = [
  '/Dooly/',
  '/Dooly/index.html',
  '/Dooly/02_Task_v1.html',
  '/Dooly/03_SOP_v1.html',
  '/Dooly/04_FAQ_v1.html',
  '/Dooly/05_Notice_v1.html',
  '/Dooly/06_Dooly_v1.html',
  '/Dooly/07_Settings_v1.html',
  '/Dooly/data.js',
  '/Dooly/manifest.json',
  '/Dooly/icons/icon-192.png',
  '/Dooly/icons/icon-512.png'
];

// 설치: 모든 파일 캐시에 저장
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(URLS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

// 활성화: 이전 캐시 삭제
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.filter(function(name) {
          return name !== CACHE_NAME;
        }).map(function(name) {
          return caches.delete(name);
        })
      );
    })
  );
  self.clients.claim();
});

// 요청: 캐시 우선, 없으면 네트워크
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});
```

---

# STEP 2 — 아이콘 PNG 파일 생성 (Python)

## 아이콘 생성 스크립트 실행

아래 Python 코드를 실행해서 아이콘 2개를 생성한다.

```python
# 아이콘 생성 스크립트 (cmd에서 실행)
python -c "
import struct, zlib, os

def make_png(size, filename):
    def chunk(name, data):
        c = name + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    # 배경색 #0b0f1a, 텍스트 없는 단색 아이콘
    bg = (11, 15, 26)      # #0b0f1a (다크 배경)
    ac = (77, 163, 255)    # #4da3ff (포인트 색)
    
    rows = []
    for y in range(size):
        row = bytearray([0])
        cx, cy = size // 2, size // 2
        r_outer = int(size * 0.42)
        r_inner = int(size * 0.28)
        for x in range(size):
            dx, dy = x - cx, y - cy
            dist = (dx*dx + dy*dy) ** 0.5
            if dist <= r_outer and dist >= r_inner:
                row.extend(ac)
            elif dist < r_inner:
                row.extend([255, 255, 255])
            else:
                row.extend(bg)
        rows.append(bytes(row))
    
    raw = b''.join(rows)
    compressed = zlib.compress(raw)
    
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', compressed)
    png += chunk(b'IEND', b'')
    
    os.makedirs('docs/icons', exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(png)
    print(f'생성 완료: {filename}')

make_png(192, 'docs/icons/icon-192.png')
make_png(512, 'docs/icons/icon-512.png')
"
```

## 실행 위치

```
cd C:\Obsidian\Dooly
위 python 명령어 실행
```

## 완료 확인

```
✅ docs\icons\icon-192.png 생성됨
✅ docs\icons\icon-512.png 생성됨
```

---

# STEP 3 — docs/index.html에 service-worker 등록 코드 추가

## 수정 대상

```
C:\Obsidian\Dooly\docs\index.html
```

## 찾을 부분

```html
</body>
```

## 변경 후 (</body> 바로 앞에 추가)

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

# STEP 4 — 04_Runtime에도 동일하게 적용

docs 폴더와 04_Runtime 폴더를 동기화한다.

```
copy docs\service-worker.js 04_Runtime\service-worker.js
copy docs\icons\icon-192.png 04_Runtime\icons\icon-192.png
copy docs\icons\icon-512.png 04_Runtime\icons\icon-512.png
```

04_Runtime\index.html 에도 동일하게 service-worker 등록 코드 추가:

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

※ 04_Runtime은 경로가 /service-worker.js (docs는 /Dooly/service-worker.js)

---

# STEP 5 — git 커밋 및 push

```
cd C:\Obsidian\Dooly

git add .
git commit -m "feat: PWA service-worker.js + 아이콘 추가"
git push
```

---

# 전체 작업 완료 조건

```
✅ STEP 1 완료 (service-worker.js 생성)
✅ STEP 2 완료 (icon-192.png, icon-512.png 생성)
✅ STEP 3 완료 (docs/index.html SW 등록)
✅ STEP 4 완료 (04_Runtime 동기화)
✅ STEP 5 완료 (git push)

✅ https://2passion.github.io/Dooly/ 접속
✅ 브라우저 주소창에 설치 아이콘 표시 확인
```

---

# STEP 6 — PWA 설치 테스트 (브라우저에서 직접)

## 갤럭시 (Chrome)

```
1. Chrome에서 https://2passion.github.io/Dooly/ 접속
2. 주소창 오른쪽 설치 아이콘 클릭 (⊕ 또는 ⬇)
   또는 메뉴(⋮) → "앱 설치" 또는 "홈 화면에 추가"
3. 홈 화면에 KING 아이콘 생성 확인
4. 아이콘 클릭 → 앱처럼 실행 확인
```

## 아이폰 (Safari)

```
1. Safari에서 https://2passion.github.io/Dooly/ 접속
2. 하단 공유 버튼(□↑) 클릭
3. "홈 화면에 추가" 클릭
4. "추가" 클릭
5. 홈 화면에 KING 아이콘 생성 확인
```

---

# 다음 작업

44번 → 갤럭시 PWA 설치 테스트 결과 확인 및 수정
45번 → 아이폰 PWA 설치 테스트 결과 확인 및 수정

---

# END OF ORDER
