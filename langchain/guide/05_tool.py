# import os
# from langchain.agents import create_agent
# from langchain_openai import ChatOpenAI
# from langchain.tools import tool

# # 修改智能体信息
# # 方法1：强制要求模型使用工具（推荐）
# # 配置阿里云百炼
# api_key = os.getenv("DASHSCOPE_API_KEY")
# base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
# model_name = "qwen-plus"

# # 定义个人信息工具
# @tool
# def get_bot_info(query: str = "") -> str:
#     """获取智能助手的基本信息，包括名称、功能、特点等"""
#     return "我是你的智能助手，小爱同学，随时为你服务。我可以回答问题、提供建议、进行对话等。"

# # 创建 Agent - 添加强制使用工具的提示
# agent = create_agent(
#     model=ChatOpenAI(
#         model=model_name,
#         api_key=api_key,
#         base_url=base_url,
#         temperature=0.7,
#     ),
#     tools=[get_bot_info],
#     system_prompt="""你是一个乐于助人的助手。
    
# 重要指令：
# 1. 当用户询问"你是谁"、"你叫什么"、"介绍一下你自己"等问题时，必须使用 get_bot_info 工具来回答
# 2. 不要直接编造关于你自己的信息
# 3. 始终优先使用工具获取准确信息""",
# )

# # 执行查询
# result = agent.invoke({
#     "messages": [{"role": "user", "content": "你是谁？"}]
# })

# print("最终回答：", result["messages"][-1].content)

#--------------------------------------------------------------------------------------------------------------------------------------------

# 修改智能体信息
# 方法2：修改工具名称和描述，使其更明确
# import os
# from langchain.agents import create_agent
# from langchain_openai import ChatOpenAI
# from langchain.tools import tool
# 配置阿里云百炼
# api_key = os.getenv("DASHSCOPE_API_KEY")
# base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
# model_name = "qwen-plus"
# @tool
# def get_assistant_identity() -> str:
#     """当用户询问助手的身份、名称或基本信息时，必须调用此工具。
    
#     适用问题：
#     - 你是谁？
#     - 你叫什么名字？
#     - 介绍一下你自己
#     - 你能做什么？
#     """
#     return "我是你的智能助手，小爱同学，随时为你服务。我可以回答问题、提供建议、进行对话等。"

# # 创建 Agent
# agent = create_agent(
#     model=ChatOpenAI(
#         model=model_name,
#         api_key=api_key,
#         base_url=base_url,
#     ),
#     tools=[get_assistant_identity],
#     system_prompt="""你是小爱同学助手。

# 规则：
# - 任何关于你身份的问题，都必须调用 get_assistant_identity 工具
# - 禁止使用你自己的知识回答关于身份的问题
# - 只使用工具返回的信息回答""",
# )

# # 执行查询
# result = agent.invoke({
#     "messages": [{"role": "user", "content": "你是谁？"}]
# })

# print("最终回答：", result["messages"][-1].content)

#--------------------------------------------------------------------------------------------------------------------------------------------

# # 方法三 直接使用工具 + 模型（不通过 Agent）
# import os
# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain.agents import create_agent
# from langchain_openai import ChatOpenAI
# from langchain.tools import tool

# api_key = os.getenv("DASHSCOPE_API_KEY")
# base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
# model_name = "qwen-plus"
# # 定义个人信息工具
# @tool
# def get_bot_info(query: str = "") -> str:
#     """获取智能助手的基本信息，包括名称、功能、特点等"""
#     return "我是你的智能助手，小爱同学，随时为你服务。我可以回答问题、提供建议、进行对话等。"

# # 直接使用工具获取信息
# bot_info = get_bot_info.invoke({"query": "身份信息"})

# # 创建模型
# model = ChatOpenAI(
#     model=model_name,
#     api_key=api_key,
#     base_url=base_url,
# )

# # 构造提示
# response = model.invoke([
#     SystemMessage(content=f"你的身份信息是：{bot_info}。请基于这个信息回答用户问题。"),
#     HumanMessage(content="你是谁？")
# ])

# print("最终回答：", response.content)

# response = model.invoke([
#     SystemMessage(content=f"你的身份信息是：{bot_info}。请基于这个信息回答用户问题。"),
#     HumanMessage(content="你是通义千问吗？")
# ])

# print("最终回答：", response.content)


#--------------------------------------------------------------------------------------------------------------------------------------------
#方法5：自定义工具执行逻辑（最灵活）
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field

api_key = os.getenv("DASHSCOPE_API_KEY")
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
model_name = "qwen-plus"

# 定义个人信息工具
@tool
def get_bot_info(query: str = "") -> str:
    """获取智能助手的基本信息，包括名称、功能、特点等"""
    return "我是你的智能助手，小爱同学，随时为你服务。我可以回答问题、提供建议、进行对话等。"

class BotInfoInput(BaseModel):
    question: str = Field(description="用户关于助手身份的问题")

class BotInfoTool(BaseTool):
    name: str = "get_bot_info"
    description: str = """当用户询问关于助手身份、名称、功能的问题时使用。
    包括但不限于：你是谁、你叫什么、你能做什么、介绍一下你自己"""
    args_schema: Type[BaseModel] = BotInfoInput
    
    def _run(self, question: str) -> str:
        """返回助手信息"""
        # 可以根据具体问题返回不同信息
        if "名字" in question or "名称" in question:
            return "我叫小爱同学"
        elif "功能" in question or "做什么" in question:
            return "我可以回答问题、提供建议、进行日常对话"
        else:
            return "我是你的智能助手，小爱同学，随时为你服务"
    
    async def _arun(self, question: str) -> str:
        return self._run(question)

# 使用自定义工具
bot_tool = BotInfoTool()
agent = create_agent(
    model=ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url=base_url,
    ),
    tools=[bot_tool],
    system_prompt="""你是小爱同学助手。
    
重要：对于任何关于你身份的问题，必须使用 get_bot_info 工具。
永远不要自己编造身份信息。""",
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "你是谁？"}]
})
print("最终回答：", result["messages"][-1].content)