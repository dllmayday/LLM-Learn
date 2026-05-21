from langchain_core.prompts import ChatPromptTemplate
import os
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from models import *

def print_response(response):
    print(f"回复: {response.content}")
    print(f"模型: {response.response_metadata['model_name']}")
    print(f"Token 用量: 输入={response.usage_metadata['input_tokens']} 输出={response.usage_metadata['output_tokens']} 总计={response.usage_metadata['total_tokens']}")
    print(f"结束原因: {response.response_metadata['finish_reason']}")

# print("invoke 调用")
# response = get_qwen().invoke("Why do parrots have colorful feathers? Answer Use Chinese.")
# print_response(response)
# print("="*50)

# print("stream 调用")
# for chunk in get_qwen().stream("Why do parrots have colorful feathers? Answer Use Chinese."):
#     print(chunk.text, end="|", flush=True)
# print("="*50)


# full = None  # None | AIMessageChunk
# for chunk in get_qwen().stream("What color is the sky? Answer Use Chinese."):
#     full = chunk if full is None else full + chunk
#     print(full.text)

# print("="*50)

# print(full.content_blocks)


responses = get_qwen().batch([
    "Why do parrots have colorful feathers?",
    "How do airplanes fly?",
    "What is quantum computing?"
])
for response in responses:
    print_response(response)