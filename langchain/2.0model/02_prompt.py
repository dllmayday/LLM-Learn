from langchain_core.prompts import ChatPromptTemplate
import os
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} expert. Be concise and helpful."),
    ("human", "{question}")
])

# Variables are substituted at runtime
formatted = prompt.invoke({
    "role": "Kubernetes",
    "question": "What is a Pod?"
})


# 配置火山引擎方舟
api_key = os.getenv("ARK_API_KEY")
base_url = "https://ark.cn-beijing.volces.com/api/v3"

# ===================== 完全按你的示例 =====================
model=ChatOpenAI(
        model="glm-4-7-251222",
        api_key=api_key,
        base_url=base_url,
        temperature=0
)
# 方法一 chain 方式（prompt + model 组合）
# chain = prompt | model
# response = chain.invoke({
#     "role": "Kubernetes",
#     "question": "What is a Pod?"
# })
# 方法二 先格式化，再调用（等价于方式一）
response = model.invoke(formatted)

# ✅ 终极稳定输出（永远不会报错）
usage = response.usage_metadata
print(f"回复: {response.content}")
print(f"模型: {response.response_metadata['model_name']}")
print(f"Token 用量: 输入={usage['input_tokens']} 输出={usage['output_tokens']} 总计={usage['total_tokens']}")
print(f"结束原因: {response.response_metadata['finish_reason']}")