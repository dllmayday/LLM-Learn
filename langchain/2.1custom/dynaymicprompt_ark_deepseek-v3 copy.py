from typing import TypedDict

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain_openai import ChatOpenAI

import os

# 从环境变量中获取您的API KEY，配置方法见：https://www.volcengine.com/docs/82379/1399008
api_key = os.getenv('ARK_API_KEY')

class Context(TypedDict):
    user_role: str

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """根据用户角色生成系统提示。"""
    user_role = request.runtime.context.get("user_role", "user")
    base_prompt = "你是一个有帮助的助手。"

    if user_role == "expert":
        return f"{base_prompt} 提供详细的技术响应。"
    elif user_role == "beginner":
        return f"{base_prompt} 简单解释概念，避免使用行话。"

    return base_prompt

# 配置模型
MODEL_NAME = "deepseek-v3-2-251201"
model = ChatOpenAI(
    model=MODEL_NAME,
    api_key=api_key,
    base_url="https://ark.cn-beijing.volces.com/api/v3",  # 火山引擎 API 地址
    temperature=0
)

# 创建代理
agent = create_agent(
    model=model,
    middleware=[user_role_prompt],
    context_schema=Context
)

# 系统提示将根据上下文动态设置
result = agent.invoke(
    {"messages": [{"role": "user", "content": "解释机器学习"}]},
    context={"user_role": "expert"}
)   
# 打印结果
messages = result.get("messages", [])
for msg in reversed(messages):
    role = getattr(msg, "type", getattr(msg, "role", ""))
    content = getattr(msg, "content", "")
    if role in ("ai", "assistant") and isinstance(content, str) and content.strip():
        print("=" * 40)
        print(f"用户角色: expert")
        print("=" * 40)
        print(content.strip())
        break

# 再测试 beginner 角色
result2 = agent.invoke(
    {"messages": [{"role": "user", "content": "解释机器学习"}]},
    context={"user_role": "beginner"}
)

messages2 = result2.get("messages", [])
for msg in reversed(messages2):
    role = getattr(msg, "type", getattr(msg, "role", ""))
    content = getattr(msg, "content", "")
    if role in ("ai", "assistant") and isinstance(content, str) and content.strip():
        print("=" * 40)
        print(f"用户角色: beginner")
        print("=" * 40)
        print(content.strip())
        break