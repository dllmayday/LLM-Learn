import os
from langchain_openai import ChatOpenAI

# 千问模型
def get_qwen():
    return ChatOpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="qwen-plus",
        temperature=0.7,
        max_tokens=1000,
        timeout=30
    )

# 火山模型
def get_ark():
    return ChatOpenAI(
        api_key=os.getenv("ARK_API_KEY"),
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        model="glm-4-7-251222",
        temperature=0.7,
        max_tokens=1000,
        timeout=30
    )

# deepseek模型:
#    deepseek-chat 对应 DeepSeek-V3.2-Exp 的非思考模式，
#    deepseek-reasoner 对应 DeepSeek-V3.2-Exp 的思考模式.
def get_deepseek():
    return ChatOpenAI(
        api_key=os.getenv('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com",
        model="deepseek-chat",
        max_tokens=1000,
        timeout=30
    )
