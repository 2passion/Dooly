# server.py — FastAPI + Chroma + Ollama RAG 서버

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions
import ollama
import os

# 경로 설정
DB_DIR      = r"C:\Obsidian\Dooly\05_RAG\db"
RUNTIME_DIR = r"C:\Obsidian\Dooly\04_Runtime"
MODEL       = "qwen2.5:7b"

# FastAPI 앱 초기화
app = FastAPI()

# CORS 설정 (HTML 파일에서 API 호출 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙 (HTML/CSS/JS)
app.mount("/static", StaticFiles(directory=RUNTIME_DIR), name="static")

# Chroma 초기화
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)
chroma_client = chromadb.PersistentClient(path=DB_DIR)
collection = chroma_client.get_collection(
    name="dooly_docs",
    embedding_function=emb_fn
)

# 요청 모델
class ChatRequest(BaseModel):
    message: str
    model: str = "qwen2.5:7b"

# 시스템 프롬프트
SYSTEM_PROMPT = """당신은 킹수학 학원의 AI 업무 도우미 둘리(Dooly)입니다.
조교들의 업무를 도와주는 역할을 합니다.

규칙:
1. 반드시 한국어로 답변합니다.
2. 제공된 SOP/FAQ 내용을 기반으로 답변합니다.
3. 모르는 내용은 추측하지 말고 "확인이 필요합니다. 원장에게 문의하세요."라고 답변합니다.
4. 답변은 간결하고 명확하게 합니다.
5. 학생이나 학부모에게 직접 약속하지 않습니다.

반드시 한국어로만 답변하라.
중국어, 영어, 일본어 등 한국어 이외의 언어는 절대 사용하지 마라.
답변 마지막에 다른 언어로 된 문장을 추가하지 마라."""

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

@app.get("/{filename}.html")
async def redirect_html(filename: str):
    return RedirectResponse(url=f"/app/{filename}.html")

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        # 1. 벡터DB에서 관련 문서 검색 (상위 3개)
        results = collection.query(
            query_texts=[req.message],
            n_results=3
        )

        # 2. 검색된 문서 컨텍스트 생성
        context_docs = results["documents"][0] if results["documents"] else []
        context = "\n\n---\n\n".join(context_docs)

        # 3. Ollama에 질문 + 컨텍스트 전달
        prompt = f"""다음은 킹수학 학원의 SOP/FAQ 내용입니다:

{context}

위 내용을 참고하여 아래 질문에 답변하세요:
질문: {req.message}"""

        selected_model = req.model if req.model else MODEL
        response = ollama.chat(
            model=selected_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt}
            ]
        )

        answer = response["message"]["content"]

        # 출처 상세 파싱
        sources = []
        if results["metadatas"] and results["metadatas"][0]:
            for meta in results["metadatas"][0]:
                source_file = meta.get("source", "")
                chunk_index = meta.get("chunk", 0)

                if "faq_data" in source_file:
                    sources.append({
                        "type": "FAQ",
                        "label": "Q" + str(chunk_index + 1),
                        "file": source_file
                    })
                elif "sop_data" in source_file:
                    sources.append({
                        "type": "SOP",
                        "label": str(chunk_index + 1),
                        "file": source_file
                    })
                else:
                    sources.append({
                        "type": "DOC",
                        "label": source_file.replace(".txt", ""),
                        "file": source_file
                    })

        return {"answer": answer, "sources": sources}

    except Exception as e:
        return {"answer": f"오류가 발생했습니다: {str(e)}", "sources": []}
