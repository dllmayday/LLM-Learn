from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime
import os
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from models import *


#  构建一个真实世界的智能体
#  1. 定义系统提示词
SYSTEM_PROMPT = """
你是一位天气预报专家，说话总是双关语。 
 
您可以访问两个工具： 

- get_weather_for_location：使用它来获取给定城市的天气 
- get_user_location：使用它来获取用户的城市地址 
 
如果用户向你询问天气，确保你知道它的位置。如果您可以从问题中知道它们的意思，那么可以使用get_user_location工具找到它们的位置。
"""

# 2. 创建工具
@tool
def get_weather_for_location(city: str) -> str:
    """获取给定城市的天气."""
    return f"在这个 {city} 总是阳光明媚!"


# LangChain的@tool装饰器添加元数据，并通过ToolRuntime参数启用运行时注入。
@dataclass
class Context:
    """自定义运行时上下文模式."""
    user_id: str

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """根据user_id检索用户城市地址."""
    user_id = runtime.context.user_id
    return "北京" if user_id == "1" else "长沙"

# 3. 配置模型
# 千问模型
model = qwen

# 4. 定义返回格式 (可选)
# 如果需要agent响应匹配特定模式，还可以选择定义结构化响应格式。如：dataclass
@dataclass
class ResponseFormat:
    """agent的响应模式."""
    # 双关语的响应
    punny_response: str
    # 天气信息
    weather_conditions: str | None = None

# 5. 添加记忆
checkpointer = InMemorySaver()

# 6. 创建一个智能体
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer,
    # debug=True  # 开启调试
)

# thread_id 是给定会话的唯一标识符。
config = {"configurable": {"thread_id": "1"}}

# 第一轮会话
response = agent.invoke(
    {"messages": [{"role": "user", "content": "外面天气怎么样?"}]},
    config=config,
    context=Context(user_id="1")
)
print(response['structured_response'])

# 第二轮会话
# 使用同一个thread_id，继续提问，多轮会话
response = agent.invoke(
    {"messages": [{"role": "user", "content": "谢谢!"}]},
    config=config,
    context=Context(user_id="1")
)
print(response['structured_response'])