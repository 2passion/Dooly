# server.py — FastAPI + Chroma + Ollama RAG 서버

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions
import ollama

# 경로 설정
DB_DIR = r"C:\Obsidian\Dooly\05_RAG\db"
MODEL  = "qwen2.5:7b"

# FastAPI 앱 초기화
app = FastAPI()

# CORS 설정 (HTML 파일에서 API 호출 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# 시스템 프롬프트
SYSTEM_PROMPT = """당신은 킹수학 학원의 AI 업무 도우미 둘리(Dooly)입니다.
조교들의 업무를 도와주는 역할을 합니다.

규칙:
1. 반드시 한국어로 답변합니다.
2. 제공된 SOP/FAQ 내용을 기반으로 답변합니다.
3. 모르는 내용은 추측하지 말고 "확인이 필요합니다. 원장에게 문의하세요."라고 답변합니다.
4. 답변은 간결하고 명확하게 합니다.
5. 학생이나 학부모에게 직접 약속하지 않습니다."""

@app.get("/")
def root():
    return {"status": "Dooly RAG 서버 실행 중"}

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

        response = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt}
            ]
        )

        answer = response["message"]["content"]
        return {"answer": answer, "sources": results["metadatas"][0] if results["metadatas"] else []}

    except Exception as e:
        return {"answer": f"오류가 발생했습니다: {str(e)}", "sources": []}
