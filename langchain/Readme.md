
参考链接：[langchain-doc](https://langchain-doc.cn/)
参考链接：[langchain-doc](https://langchain-doc.cn/)
## 目录结构


## Linux 环境准备
安装 LangChain 包：
```
pip install -U langchain

```
LangChain 提供对数百种 LLM 和数千种其他集成的支持。这些集成存在于独立的提供者包中。例如：

```
# 安装 Anthropic 集成
pip install -U langchain-anthropic

# 安装 OpenAI 集成
pip install -U langchain-openai

# 安装 DashScope 集成 阿里云百炼
python3 -m pip install -U dashscope
```

## 实现说明

### 创建代理
```
agent = create_agent(
    model="anthropic:claude-sonnet-4-5",   # 使用的语言模型
    tools=[get_weather],                    # 可调用的工具列表
    system_prompt="你是一个乐于助人的助手", # 系统提示词
)
```
| 参数           |  作用        |
| ---------     | ----------- |
| model         | 指定LLM，格式为提供商:模型名          |
| tools         | 形成工具列表，代理可以决定是否调用      |
| system_prompt |设定AI的角色和行为基调                 |

####  定义系统提示
系统提示定义了代理的角色和行为。保持其具体且可操作。示例：
```python
SYSTEM_PROMPT = """你是一位擅长用双关语表达的专家天气预报员。

你可以使用两个工具：

- get_weather_for_location：用于获取特定地点的天气
- get_user_location：用于获取用户的位置

如果用户询问天气，请确保你知道具体位置。如果从问题中可以判断他们指的是自己所在的位置，请使用 get_user_location 工具来查找他们的位置。"""
```
#### 创建工具
工具 允许模型通过调用您定义的函数与外部系统交互。
工具可以依赖于运行时上下文，也可以与代理记忆交互。

```
# 天气查询工具测试用：接收城市名city，返回一个字符串
def get_weather(city: str) -> str:
     """获取指定城市的天气。"""
     return f"{city}总是阳光明媚！"

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

```
**提示**
工具应有良好的文档说明：其名称、描述和参数名称将成为模型提示的一部分。
LangChain 的 @tool 装饰器 会添加元数据，并通过 ToolRuntime 参数启用运行时注入。
#### 模型配置
```
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "anthropic:claude-sonnet-4-5",
    temperature=0.5,
    timeout=10,
    max_tokens=1000
)

```

### 运行代理
```
agent.invoke(
    {"messages": [{"role": "user", "content": "旧金山的天气怎么样"}]}
)
```
invoke()触发代理运行
输入是标准的消息列表格式，role: user表示用户所说的话

#### 整体执行流程

  用户提问："旧金山的天气怎么样？"
        ↓
    Claude 模型分析问题
        ↓
  判断需要调用 get_weather 工具
        ↓
  调用 get_weather("旧金山")
        ↓
  获得返回值："旧金山总是阳光明媚！"
        ↓
  Claude 整合结果，生成最终回答

这就是ReAct代理的核心模式：模型自主决策→调用工具→观察结果→生成回答。