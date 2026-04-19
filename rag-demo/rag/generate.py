import requests
from rag.retrieve import retrieve

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_answer(query):
    docs = retrieve(query)

    context = "\n".join(docs)

    prompt = f"""
你是一个专业助手，请基于以下资料回答问题：

资料：
{context}

问题：
{query}

要求：
- 只基于资料回答
- 不要编造
"""

    try:
        res = requests.post(OLLAMA_URL, json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        })

        data = res.json()

        # ⭐调试用（建议保留一段时间）
        print("Ollama返回:", data)

        # ✅ 正常情况
        if "response" in data:
            return data["response"]

        # ✅ 兼容 chat 接口格式（防止你后面换接口）
        elif "message" in data:
            return data["message"]["content"]

        # ❌ Ollama错误
        elif "error" in data:
            return f"[Ollama错误] {data['error']}"

        # ❌ 未知格式
        else:
            return f"[未知返回格式] {data}"

    except Exception as e:
        return f"[请求失败] {str(e)}"