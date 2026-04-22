from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

import os

# 配置模型（火山引擎 DeepSeek）
model = ChatOpenAI(
    model="deepseek-v3-2-251201",
    api_key=os.getenv("ARK_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    temperature=0.7
)

# ========== 新接口核心改动 ==========

# 1. 使用 LCEL 构建基础链
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位 {role} 专家。回答简洁、专业、有帮助。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

# 基础链：prompt -> model -> 输出解析
base_chain = prompt | model | StrOutputParser()

# 2. 会话存储（管理不同会话的历史记录）
session_store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """根据 session_id 获取对应的对话历史"""
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]

# 3. 使用 RunnableWithMessageHistory 包装基础链，注入记忆能力
chain_with_memory = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="question",      # 输入消息的字段名
    history_messages_key="chat_history" # 与 MessagesPlaceholder 变量名一致
)

# ========== 使用示例 ==========

def chat(question: str, role: str = "技术", session_id: str = "default_session"):
    """
    发送消息并获取回复
    session_id: 会话标识，不同 session_id 的对话历史相互隔离
    """
    response = chain_with_memory.invoke(
        {
            "question": question,
            "role": role
        },
        config={"configurable": {"session_id": session_id}}
    )
    return response

def print_memory(session_id: str = "default_session"):
    """打印指定会话的对话历史"""
    history = get_session_history(session_id)
    print("\n当前记忆内容：")
    print("=" * 40)
    for msg in history.messages:
        prefix = "用户" if msg.type == "human" else "AI"
        print(f"{prefix}: {msg.content}")
    print("=" * 40)


# ========== 运行示例 ==========
if __name__ == "__main__":
    session = "user_001"  # 使用 session_id 隔离会话
    
    print("=" * 40)
    print("对话1：什么是 Docker？")
    print("=" * 40)
    print(chat("什么是 Docker？", role="DevOps", session_id=session))
    
    print("=" * 40)
    print("对话2：它和虚拟机有什么区别？")
    print("=" * 40)
    print(chat("它和虚拟机有什么区别？", session_id=session))   # 依赖上文记忆
    
    print("=" * 40)
    print("对话3：给我一个最简单的示例")
    print("=" * 40)
    print(chat("给我一个最简单的 Dockerfile 示例", session_id=session))
    
    print_memory(session)