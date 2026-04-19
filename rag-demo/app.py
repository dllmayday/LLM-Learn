from fastapi import FastAPI
from rag.generate import generate_answer

app = FastAPI()

@app.get("/ask")
def ask(q: str):
    answer = generate_answer(q)
    return {"answer": answer}