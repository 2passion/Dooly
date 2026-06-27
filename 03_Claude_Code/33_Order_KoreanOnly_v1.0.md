# 33_Order_KoreanOnly_v1.0.md

## 작업 개요
server.py 시스템 프롬프트에 한국어 전용 지시 추가
qwen 모델이 답변 마지막에 중국어를 붙이는 문제 수정

## 수정 대상 파일
C:\Obsidian\Dooly\05_RAG\server.py

## 작업 내용
server.py 내 시스템 프롬프트 문자열에 아래 내용 추가:

기존:
system_prompt = """당신은 킹수학 학원의 AI 비서 둘리입니다.
...existing content...
"""

변경:
system_prompt = """당신은 킹수학 학원의 AI 비서 둘리입니다.
...existing content...

반드시 한국어로만 답변하라.
중국어, 영어, 일본어 등 한국어 이외의 언어는 절대 사용하지 마라.
답변 마지막에 다른 언어로 된 문장을 추가하지 마라.
"""

## 작업 완료 후 git 명령어
git add .
git commit -m "fix: enforce Korean-only response in Dooly system prompt"
git push
