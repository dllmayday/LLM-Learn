import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


# =========================
# LLM 配置（阿里云百炼 Qwen）
# =========================
api_key = os.getenv("DASHSCOPE_API_KEY")
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
model_name = "qwen-plus"

llm = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url
)


# =========================
# Prompt
# =========================
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with memory."),
    
    # 历史对话
    MessagesPlaceholder(variable_name="chat_history"),
    
    # 当前用户输入
    ("user", "{question}")
])


# =========================
# Session Memory Store
# =========================
store = {}


def get_session_history(session_id: str):
    """根据 session_id 获取会话历史"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# =========================
# Chain
# =========================
base_chain = prompt | llm


agent_runnable = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history"
)


# =========================
# Chat API
# =========================
def chat(question: str, session_id: str = "default_session"):
    result = agent_runnable.invoke(
        {
            "question": question
        },
        config={
            "configurable": {
                "session_id": session_id
            }
        }
    )
    return result.content


# =========================
# Test
# =========================
if __name__ == "__main__":
    print(chat("我喜欢吃火锅"))
    print(chat("记住我口味是辣"))
    print(chat("我喜欢什么口味？"))

    print("------ 新会话 ------")

    print(chat("我喜欢什么口味？", "session_1"))