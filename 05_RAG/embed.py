# embed.py — SOP/FAQ 문서를 Chroma 벡터DB에 임베딩

import os
import chromadb
from chromadb.utils import embedding_functions

# 경로 설정
DOCS_DIR = r"C:\Obsidian\Dooly\05_RAG\docs"
DB_DIR   = r"C:\Obsidian\Dooly\05_RAG\db"

# 임베딩 함수 (로컬 모델, 인터넷 불필요)
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)

# Chroma 클라이언트 초기화
client = chromadb.PersistentClient(path=DB_DIR)

# 기존 컬렉션 삭제 후 재생성 (재임베딩 시)
try:
    client.delete_collection("dooly_docs")
    print("기존 컬렉션 삭제 완료")
except:
    pass

collection = client.create_collection(
    name="dooly_docs",
    embedding_function=emb_fn
)

# docs 폴더의 모든 txt 파일 읽기
docs = []
ids  = []
metas = []

for filename in os.listdir(DOCS_DIR):
    if not filename.endswith(".txt"):
        continue

    filepath = os.path.join(DOCS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 빈 줄 기준으로 청크 분할
    chunks = [c.strip() for c in content.split("\n\n") if c.strip()]

    for i, chunk in enumerate(chunks):
        doc_id = f"{filename}_{i}"
        docs.append(chunk)
        ids.append(doc_id)
        metas.append({"source": filename, "chunk": i})

# 벡터DB에 저장
if docs:
    collection.add(
        documents=docs,
        ids=ids,
        metadatas=metas
    )
    print(f"임베딩 완료: {len(docs)}개 청크 저장됨")
else:
    print("docs 폴더에 txt 파일이 없습니다.")
