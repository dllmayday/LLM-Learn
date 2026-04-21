from langchain_core.prompts import ChatPromptTemplate
import os
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} expert. Be concise and helpful."),
    ("human", "{question}")
])



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
#方法一 chain 方式（prompt + model 组合）
chain = prompt | model | StrOutputParser()
response = chain.invoke({
    "role": "DevOps",
    "question": "What is CI/CD? User Chinese answer."
})
# 查看实际消息内容
print(response)