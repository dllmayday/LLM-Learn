from rag.vector_store import VectorStore
from rag.ingest import get_embedding

vs = VectorStore()
vs.load("index")

def retrieve(query, k=3):
    q_emb = get_embedding(query)
    return vs.search(q_emb, k)