
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