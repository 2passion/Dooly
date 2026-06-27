# 45_Order_PWA_Icon_Update_v1.0.md
# King Assistant OS v1.0
# Claude Code 작업지시서

Version: v1.0
Date: 2026-06-28

---

# 작업 목표

공룡 이미지를 원형 + 흰색 배경 아이콘으로 변환
→ icon-192.png, icon-512.png 교체

---

# 작업 시작 전 필수 준비 (직접 진행)

원본 이미지 파일을 아래 경로에 저장한다.
```
C:\Obsidian\Dooly\99_Archive\dooly_source.png
```

---

# STEP 1 — Pillow 설치

```
pip install Pillow
```

---

# STEP 2 — 원형 아이콘 생성 (Python)

## 실행 위치

```
cd C:\Obsidian\Dooly
```

## 실행 명령어

```python
python -c "
from PIL import Image, ImageDraw
import os

def make_circle_icon(src_path, size, out_path):
    # 원본 이미지 열기
    img = Image.open(src_path).convert('RGBA')
    
    # 정사각형으로 크롭 (중앙 기준)
    w, h = img.size
    min_side = min(w, h)
    left = (w - min_side) // 2
    top = (h - min_side) // 2
    img = img.crop((left, top, left + min_side, top + min_side))
    
    # 목표 크기로 리사이즈
    img = img.resize((size, size), Image.LANCZOS)
    
    # 흰색 배경 생성
    bg = Image.new('RGB', (size, size), (255, 255, 255))
    
    # 원형 마스크 생성
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((2, 2, size-2, size-2), fill=255)
    
    # 배경에 이미지 합성
    img_rgb = Image.new('RGB', (size, size), (255, 255, 255))
    img_rgb.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
    bg.paste(img_rgb, mask=mask)
    
    # 저장
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    bg.save(out_path, 'PNG')
    print('저장 완료:', out_path)

src = '99_Archive/dooly_source.png'
make_circle_icon(src, 192, 'docs/icons/icon-192.png')
make_circle_icon(src, 512, 'docs/icons/icon-512.png')
make_circle_icon(src, 192, '04_Runtime/icons/icon-192.png')
make_circle_icon(src, 512, '04_Runtime/icons/icon-512.png')
print('모든 아이콘 생성 완료')
"
```

## 완료 확인

```
✅ docs\icons\icon-192.png 교체됨
✅ docs\icons\icon-512.png 교체됨
✅ 04_Runtime\icons\icon-192.png 교체됨
✅ 04_Runtime\icons\icon-512.png 교체됨
```

---

# STEP 3 — git 커밋 및 push

```
cd C:\Obsidian\Dooly

git add docs\icons\ 04_Runtime\icons\
git commit -m "feat: 공룡 캐릭터 원형 아이콘으로 교체"
git push
```

---

# STEP 4 — 스마트폰 아이콘 갱신

```
갤럭시 Chrome:
1. https://2passion.github.io/Dooly/ 접속
2. 기존 Dooly 앱 제거
   (홈 화면 아이콘 길게 누르기 → 삭제)
3. 다시 설치
   메뉴(⋮) → "앱 설치"
4. 새 공룡 아이콘 확인
```

---

# 전체 작업 완료 조건

```
✅ STEP 1 완료 (Pillow 설치)
✅ STEP 2 완료 (원형 아이콘 생성)
✅ STEP 3 완료 (git push)
✅ STEP 4 완료 (스마트폰 아이콘 갱신)
```

---

# ⚠️ 주의사항

반드시 STEP 2 실행 전에:
```
원본 이미지 파일을
C:\Obsidian\Dooly\99_Archive\dooly_source.png
로 저장한 후 진행할 것
```

---

# END OF ORDER
