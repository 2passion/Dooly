
# 32_Order_ServerRedirect_v1.0.md

## 작업 개요
server.py에 리다이렉트 라우트 추가
/02_Task_v1.html → /app/02_Task_v1.html 형태로 자동 리다이렉트

## 수정 대상 파일
C:\Obsidian\Dooly\05_RAG\server.py

## 작업 내용
기존 라우트 아래에 아래 코드 추가:

from fastapi.responses import RedirectResponse

@app.get("/{filename}.html")
async def redirect_html(filename: str):
    return RedirectResponse(url=f"/app/{filename}.html")

## 작업 완료 후 git 명령어
git add .
git commit -m "fix: redirect /{filename}.html to /app/{filename}.html"
git push
