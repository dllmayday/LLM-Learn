import requests
import os
import json
from rag.vector_store import VectorStore
from concurrent.futures import ThreadPoolExecutor

OLLAMA_URL = "http://localhost:11434/api/embeddings"



def get_embeddings_parallel(chunks, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(get_embedding, chunks))

def get_embedding(text):
    res = requests.post(OLLAMA_URL, json={
        "model": "nomic-embed-text",
        "prompt": text
    })

    data = res.json()

    if "embedding" not in data:
        raise ValueError(f"embedding接口异常: {data}")

    emb = data["embedding"]

    if not isinstance(emb, list):
        raise ValueError(f"embedding格式错误: {emb}")

    return emb

def load_docs(folder):
    docs = []
    for root, _, filenames in os.walk(folder):
        for file in filenames:
            if not file.lower().endswith(".txt"):
                continue

            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    docs.append(f.read())
            except UnicodeDecodeError:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    docs.append(f.read())

    return docs


def chunk_text(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def ingest():
    vs = VectorStore()

    docs = load_docs("data")
    chunks = []
    for doc in docs:
        chunks.extend(chunk_text(doc))

    embeddings = [get_embedding(c) for c in chunks]
    vs.add(embeddings, chunks)

    vs.save("index")

# 使用Quora数据集测试

def load_corpus(path):
    docs = []
    ids = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            docs.append(data["text"])
            ids.append(data["_id"])

    return docs, ids

def ingest_quora():
    vs = VectorStore()

    docs, ids = load_corpus("corpus.jsonl")

    chunks = docs  # Quora比较短，不用chunk

    # embeddings = [get_embedding(d) for d in docs]
    # 多线程
    embeddings = get_embeddings_parallel(chunks)


    vs.add(embeddings, docs)
    vs.save("index")

if __name__ == "__main__":
    ingest()