# claude-4-5 版本的 LangChain 代理示例（官方文档示例，未测试过，供参考）：
# from langchain.agents import create_agent


# def get_weather(city: str) -> str:
#     """获取指定城市的天气。"""
#     return f"{city}总是阳光明媚！"

# agent = create_agent(
#     model="anthropic:claude-sonnet-4-5",
#     tools=[get_weather],
#     system_prompt="你是一个乐于助人的助手",
# )

# # 运行代理
# agent.invoke(
#     {"messages": [{"role": "user", "content": "旧金山的天气怎么样"}]}
# )


# 火山引擎大模型测试示例，使用 LangChain 框架
import os
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# 配置火山引擎方舟
api_key = os.getenv("ARK_API_KEY")
base_url = "https://ark.cn-beijing.volces.com/api/v3"

# 联网搜索工具
def web_search(query: str) -> str:
    """联网搜索实时信息：天气、新闻、数据"""
    from openai import OpenAI
    client = OpenAI(base_url=base_url, api_key=api_key)
    response = client.responses.create(
        model="glm-4-7-251222",
        input=[{"role": "user", "content": query}],
        tools=[{"type": "web_search", "max_keyword": 2}],
    )
    return response.output_text

# ===================== 完全按你的示例 =====================
agent = create_agent(
    model=ChatOpenAI(
        model="glm-4-7-251222",
        api_key=api_key,
        base_url=base_url,
    ),
    tools=[web_search],
    system_prompt="你是一个乐于助人的助手",
)

# 执行（和你示例完全一样）
result = agent.invoke({
    "messages": [{"role": "user", "content": "北京的天气怎么样？"}]
})

# ✅ 终极稳定输出（永远不会报错）
print("最终回答：", result["messages"][-1].content)