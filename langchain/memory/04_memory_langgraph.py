from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import List, Dict, Any
from pydantic import BaseModel

import os

# ========== 配置模型 ==========
model = ChatOpenAI(
    model="deepseek-v3-2-251201",
    api_key=os.getenv("ARK_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    temperature=0.7
)

# ========== 定义状态结构 ==========
class ChatState(MessagesState):
    """对话状态，继承自 MessagesState 自动包含 messages 字段"""
    role: str  # 用户角色（技术专家、DevOps等）
    
# ========== 定义节点函数 ==========
def chat_node(state: ChatState) -> Dict[str, Any]:
    """
    对话节点：处理用户输入并生成回复
    """
    # 获取当前状态中的角色和所有消息
    role = state.get("role", "技术")
    messages = state["messages"]
    
    # 构建 prompt 模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一位 {role} 专家。回答简洁、专业、有帮助。"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])
    
    # 分离最后一条用户消息和历史消息
    # messages 格式：[HumanMessage, AIMessage, HumanMessage, AIMessage, ...]
    if messages and isinstance(messages[-1], HumanMessage):
        question = messages[-1].content
        chat_history = messages[:-1]  # 除了最后一条都是历史
    else:
        question = ""
        chat_history = messages
    
    # 格式化 prompt
    formatted_prompt = prompt.format_messages(
        role=role,
        chat_history=chat_history,
        question=question
    )
    
    # 调用模型
    response = model.invoke(formatted_prompt)
    
    # 返回 AI 回复（会自动添加到 messages 中）
    return {"messages": [response]}

# ========== 构建 LangGraph 工作流 ==========
def build_chat_graph():
    """构建对话图"""
    # 创建状态图
    graph_builder = StateGraph(ChatState)
    
    # 添加节点
    graph_builder.add_node("chat", chat_node)
    
    # 添加边：START -> chat -> END
    graph_builder.add_edge(START, "chat")
    graph_builder.add_edge("chat", END)
    
    # 设置入口点
    graph_builder.set_entry_point("chat")
    
    return graph_builder

# ========== 创建带检查点的对话应用 ==========
# MemorySaver 自动保存所有消息历史（替代 RunnableWithMessageHistory）
memory = MemorySaver()

# 编译图并注入记忆
graph_builder = build_chat_graph()
app = graph_builder.compile(checkpointer=memory)

# ========== 使用示例 ==========
def chat(question: str, role: str = "技术", thread_id: str = "default_thread"):
    """
    发送消息并获取回复
    thread_id: 线程标识，不同 thread_id 的对话历史相互隔离
    """
    # 配置线程 ID（用于记忆隔离）
    config = {"configurable": {"thread_id": thread_id}}
    
    # 准备输入：添加用户消息到状态中
    input_state = {
        "messages": [HumanMessage(content=question)],
        "role": role
    }
    
    # 调用图（会自动保存所有消息到 memory）
    result = app.invoke(input_state, config=config)
    
    # 提取最后一条 AI 消息作为回复
    last_message = result["messages"][-1]
    return last_message.content

def print_memory(thread_id: str = "default_thread"):
    """打印指定线程的对话历史"""
    config = {"configurable": {"thread_id": thread_id}}
    
    # 从检查点获取状态快照
    snapshot = app.get_state(config)
    
    print("\n当前记忆内容：")
    print("=" * 40)
    for msg in snapshot.values["messages"]:
        if isinstance(msg, HumanMessage):
            print(f"用户: {msg.content}")
        elif isinstance(msg, AIMessage):
            print(f"AI: {msg.content}")
    print("=" * 40)

# ========== 运行示例 ==========
if __name__ == "__main__":
    thread = "user_001"  # 使用 thread_id 隔离会话
    
    print("=" * 40)
    print("对话1：什么是 Docker？")
    print("=" * 40)
    print(chat("什么是 Docker？", role="DevOps", thread_id=thread))
    
    print("=" * 40)
    print("对话2：它和虚拟机有什么区别？")
    print("=" * 40)
    print(chat("它和虚拟机有什么区别？", thread_id=thread))
    
    print("=" * 40)
    print("对话3：给我一个最简单的示例")
    print("=" * 40)
    print(chat("给我一个最简单的 Dockerfile 示例", thread_id=thread))
    
    print_memory(thread)