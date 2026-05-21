from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.config import get_stream_writer 

import os

# 从环境变量中获取您的API KEY，配置方法见：https://www.volcengine.com/docs/82379/1399008
api_key = os.getenv('ARK_API_KEY')

# 定义系统提示
SYSTEM_PROMPT = """你是一位擅长用双关语表达的专家天气预报员。

你可以使用两个工具：

- get_weather_for_location：用于获取特定地点的天气
- get_user_location：用于获取用户的位置

如果用户询问天气，请确保你知道具体位置。如果从问题中可以判断他们指的是自己所在的位置，请使用 get_user_location 工具来查找他们的位置。"""

# 定义上下文模式
@dataclass
class Context:
    """自定义运行时上下文模式。"""
    user_id: str

# 定义工具
@tool
def get_weather_for_location(city: str) -> str:
    """获取指定城市的天气。"""
    return f"{city}总是阳光明媚！"

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """根据用户 ID 获取用户信息。"""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"

# 配置模型
MODEL_NAME = "deepseek-v3-2-251201"
model = ChatOpenAI(
    model=MODEL_NAME,
    api_key=api_key,
    base_url="https://ark.cn-beijing.volces.com/api/v3",  # 火山引擎 API 地址
    temperature=0
)
# 定义响应格式
@dataclass
class ResponseFormat:
    """代理的响应模式。"""
    # 带双关语的回应（始终必需）
    punny_response: str
    # 天气的任何有趣信息（如果有）
    weather_conditions: str | None = None

# 设置记忆
checkpointer = InMemorySaver()

# 创建代理
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

def print_agent_response(response):
    if not isinstance(response, dict):
        print(response)
        return

    # ✅ 优先用结构化响应
    sr = response.get("structured_response")
    if sr and hasattr(sr, "punny_response") and sr.punny_response:
        print(f"punny_response: '{sr.punny_response}'")
        if sr.weather_conditions:
            print(f"weather_conditions: '{sr.weather_conditions}'")
        return

    # ✅ 没有结构化响应时，取最后一条非空 AI 消息
    messages = response.get("messages", [])
    for msg in reversed(messages):
        role = getattr(msg, "type", getattr(msg, "role", ""))
        content = getattr(msg, "content", "")
        # 跳过工具消息和空消息
        if role in ("ai", "assistant") and isinstance(content, str) and content.strip():
            print(f"punny_response: '{content.strip()}'")
            return

    print("（无有效回复）")

            
def debug_messages(response):
    """临时调试：打印所有消息，看清完整流程"""
    for i, msg in enumerate(response.get("messages", [])):
        role = getattr(msg, "type", getattr(msg, "role", "?"))
        content = getattr(msg, "content", "")
        if isinstance(content, list):
            content = str(content)[:60]
        else:
            content = str(content)[:60]
        print(f"  [{i}] {role:12s} | {content}")

# 运行代理
# `thread_id` 是给定对话的唯一标识符。
config = {"configurable": {"thread_id": "1"}}


#demo1 普通stream
# for chunk in agent.stream(  # [!code highlight]
#     {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
#     stream_mode="updates",
#     config=config,
#     context=Context(user_id="1")
# ):
#     for step, data in chunk.items():
#         print(f"step: {step}")
#         print(f"content: {data['messages'][-1].content_blocks}")

#demo2  LLM 生成令牌时流式传输它们
# for token, metadata in agent.stream(  # [!code highlight]
#     {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
#     stream_mode="messages",
#     config=config,
#     context=Context(user_id="1")
# ):
#     print(f"node: {metadata['langgraph_node']}")
#     print(f"content: {token.content_blocks}")
#     print("\n")


#demo3 自定义更新 (Custom updates)
# def get_weather(city: str) -> str:
#     """获取给定城市的天气。"""
#     writer = get_stream_writer()  # [!code highlight]
#     # 流式传输任何任意数据
#     writer(f"Looking up data for city: {city}")
#     writer(f"Acquired data for city: {city}")
#     return f"It's always sunny in {city}!"

# agent_demo3 = create_agent(
#     model=model,
#     system_prompt=SYSTEM_PROMPT,
#     tools=[get_weather],
#     context_schema=Context,
#     response_format=ResponseFormat,
#     checkpointer=checkpointer
# )
# for chunk in agent_demo3.stream(
#     {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
#     stream_mode="custom",
#     config=config,
#     context=Context(user_id="1")
# ):
#     print(chunk)

#demo4 流式传输多种模式 (Stream multiple modes)
def get_weather(city: str) -> str:
    """获取给定城市的天气。"""
    writer = get_stream_writer()
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")
    return f"It's always sunny in {city}!"

agent_demo4 = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_weather],
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

for stream_mode, chunk in agent_demo4.stream(  # [!code highlight]
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode=["updates", "custom"],
    config=config,
    context=Context(user_id="1")
):
    print(f"stream_mode: {stream_mode}")
    print(f"content: {chunk}")
    print("\n")