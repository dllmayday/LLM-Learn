from openai import OpenAI
import os
# 从环境变量中获取您的API KEY，配置方法见：https://www.volcengine.com/docs/82379/1399008
api_key = os.getenv('ARK_API_KEY')
client = OpenAI(
    base_url='https://ark.cn-beijing.volces.com/api/v3',
    api_key=api_key
)
tools = [{
    "type": "web_search",
    "max_keyword": 2,
}]
# 创建一个对话请求
response = client.responses.create(
    model="glm-4-7-251222",
    input=[{"role": "user", "content": "北京的天气怎么样？"}],
    tools=tools,
)
print(response)


# import os
# from volcenginesdkarkruntime import Ark

# client = Ark(
#     base_url='https://ark.cn-beijing.volces.com/api/v3',
#     api_key=os.getenv('ARK_API_KEY'),
# )

# response = client.responses.create(
#     model="doubao-seed-2-0-lite-260215",
#     input="请使用C++实现二分查找算法", # Replace with your prompt
#     # thinking={"type": "disabled"}, #  Manually disable deep thinking
# )
# print(response)