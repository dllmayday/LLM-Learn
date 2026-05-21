from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict

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

# from langchain_core.messages import HumanMessage, SystemMessage

# test_response = model.invoke([
#     SystemMessage(content=SYSTEM_PROMPT),
#     HumanMessage(content="外面的天气怎么样？")
# ])

# print("原始响应类型:", type(test_response))
# print("content:", test_response.content)
# print("tool_calls:", test_response.tool_calls)          # ← 关键：是否为空
# print("additional_kwargs:", test_response.additional_kwargs)

print("=" * 40)
print("第一次提问：外面的天气怎么样？")
print("=" * 40)
response = agent.invoke(
    {"messages": [{"role": "user", "content": "外面的天气怎么样？"}]},
    config=config,
    context=Context(user_id="1")
)
debug_messages(response)   # 先看结构
print_agent_response(response)

# 注意，我们可以使用相同的 `thread_id` 继续对话。
print("=" * 40)
print("第二次提问：谢谢！")
print("=" * 40)
response = agent.invoke(
    {"messages": [{"role": "user", "content": "谢谢！"}]},
    config=config,
    context=Context(user_id="1")
)
debug_messages(response)   # 先看结构
print_agent_response(response)
# ResponseFormat(
#     punny_response="你真是'雷'厉风行地欢迎！帮助你保持'当前'天气总是'轻而易举'。我只是'云'游四方，等待随时'淋浴'你更多预报。祝你在佛罗里达的阳光下度过'sun-sational'的一天！",
#     weather_conditions=None
# )