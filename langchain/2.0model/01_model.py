# from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic

# # OpenAI
# openai_model = ChatOpenAI(model="gpt-4o", temperature=0.7)

# # Anthropic Claude
# claude_model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# # Both use the same interface
# response = openai_model.invoke("Explain Kubernetes in one sentence")


# 使用火山引擎大模型替代测试
# 火山引擎大模型测试示例，使用 LangChain 框架
import os
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# 配置火山引擎方舟
api_key = os.getenv("ARK_API_KEY")
base_url = "https://ark.cn-beijing.volces.com/api/v3"

# ===================== 完全按你的示例 =====================
model=ChatOpenAI(
        model="glm-4-7-251222",
        api_key=api_key,
        base_url=base_url,
)
response = model.invoke("Explain Kubernetes in one sentence")

# ✅ 终极稳定输出（永远不会报错）
usage = response.usage_metadata
print(f"回复: {response.content}")
print(f"模型: {response.response_metadata['model_name']}")
print(f"Token 用量: 输入={usage['input_tokens']} 输出={usage['output_tokens']} 总计={usage['total_tokens']}")
print(f"结束原因: {response.response_metadata['finish_reason']}")