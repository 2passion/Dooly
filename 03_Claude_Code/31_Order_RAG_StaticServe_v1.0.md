# 31_Order_RAG_StaticServe_v1.0.md
# KING Assistant OS — FastAPI에서 HTML 파일 서빙 (스마트폰 접속)

---

# 작업 개요
현재 server.py는 /chat API만 제공
스마트폰에서 HTML 앱 전체를 사용하려면
FastAPI에서 HTML 파일도 서빙해야 함

---

# 수정 대상
C:\Obsidian\Dooly\05_RAG\server.py
C:\Obsidian\Dooly\04_Runtime\06_Dooly_v1.html

---

# [수정 1] server.py — HTML 정적 파일 서빙 추가

## 1-1. import 추가

기존:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions
import ollama
```

변경:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions
import ollama
import os
```

## 1-2. 경로 설정 추가

기존:
```python
# 경로 설정
DB_DIR = r"C:\Obsidian\Dooly\05_RAG\db"
MODEL  = "qwen2.5:7b"
```

변경:
```python
# 경로 설정
DB_DIR      = r"C:\Obsidian\Dooly\05_RAG\db"
RUNTIME_DIR = r"C:\Obsidian\Dooly\04_Runtime"
MODEL       = "qwen2.5:7b"
```

## 1-3. CORS 설정 아래에 정적 파일 마운트 추가

기존:
```python
# CORS 설정 (HTML 파일에서 API 호출 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

변경:
```python
# CORS 설정 (HTML 파일에서 API 호출 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙 (HTML/CSS/JS)
app.mount("/static", StaticFiles(directory=RUNTIME_DIR), name="static")
```

## 1-4. 루트 경로에 index.html 반환 추가

기존:
```python
@app.get("/")
def root():
    return {"status": "Dooly RAG 서버 실행 중"}
```

변경:
```python
@app.get("/")
def root():
    return {"status": "Dooly RAG 서버 실행 중"}

@app.get("/app")
def serve_app():
    return FileResponse(os.path.join(RUNTIME_DIR, "index.html"))

@app.get("/app/{filename}")
def serve_file(filename: str):
    filepath = os.path.join(RUNTIME_DIR, filename)
    if os.path.exists(filepath):
        return FileResponse(filepath)
    return {"error": "File not found"}
```

---

# [수정 2] 06_Dooly_v1.html — RAG_SERVER 주소를 동적으로 변경

현재 RAG_SERVER가 localhost:8001로 고정되어 있어
스마트폰에서 접속 시 서버를 찾지 못함.
접속한 호스트 주소를 자동으로 사용하도록 변경.

기존:
```javascript
  var RAG_SERVER = 'http://localhost:8001';
```

변경:
```javascript
  // 현재 접속한 호스트 기준으로 RAG 서버 주소 자동 설정
  // 로컬 파일(file://)로 열면 localhost:8001 사용
  // 서버를 통해 열면 같은 호스트의 8001 포트 사용
  var RAG_SERVER = (location.protocol === 'file:')
    ? 'http://localhost:8001'
    : location.protocol + '//' + location.hostname + ':8001';
```

---

# [수정 3] run_server.bat — 접속 주소 안내 추가

기존 마지막 echo 부분:
```bat
echo [Starting] uvicorn server...
echo.

python -m uvicorn server:app --host 0.0.0.0 --port 8001
```

변경:
```bat
echo [Starting] uvicorn server...
echo.
echo Access URLs:
echo   PC browser  : http://localhost:8001/app
echo   Smartphone  : http://192.168.219.100:8001/app
echo   API status  : http://localhost:8001
echo.

python -m uvicorn server:app --host 0.0.0.0 --port 8001
```

---

# 작업 완료 후

서버 재시작:
1. 현재 서버 창 Ctrl+C 종료
2. run_server.bat 다시 더블클릭

접속 테스트:
```
PC 브라우저:
http://localhost:8001/app

스마트폰 브라우저 (같은 와이파이):
http://192.168.219.100:8001/app
```

```
git add . && git commit -m "feat: FastAPI static HTML serving for mobile access" && git push
```
