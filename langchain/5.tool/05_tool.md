tool扩展了Agent的功能——使它们能够获取实时数据、执行代码、查询外部数据库并在现实世界中采取行动。
在底层，工具是具有明确定义输入和输出的可调用函数，这些函数会被传递给聊天模型。模型会根据对话上下文决定何时调用工具以及需要提供哪些输入参数。
## 创建工具
创建工具最简单的方法是使用@tool装饰器。默认情况下，函数的文档字符串会成为工具的描述，帮助模型理解何时使用该工具：
```
from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"
```
### 自定义工具属性
默认情况下，工具名称来源于函数名称。如果需要更具描述性的名称，可以对其进行覆盖：
创建工具时，您也可以指定工具名称和描述。如果您不指定名称，则将使用函数的名称作为工具名称。如果您不指定描述，则将使用函数的文档字符串作为工具描述：
```
@tool(name="Search Database", description="Search the customer database for records matching the query.")
def search_database(query: str, limit: int = 10) -> str:
    return f"Found {limit} results for '{query}'"
```
### 高级模式定义
使用 Pydantic 模型或 JSON 模式定义复杂输入：

```
weather_schema = {
    "type": "object",
    "properties": {
        "location": {"type": "string"},
        "units": {"type": "string"},
        "include_forecast": {"type": "boolean"}
    },
    "required": ["location", "units", "include_forecast"]
}

@tool(args_schema=weather_schema)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get current weather and optional forecast."""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    if include_forecast:
        result += "\nNext 5 days: Sunny"
    return result
```


#### 保留参数名称
以下参数名称为保留名称，不能用作工具参数。使用这些名称会导致运行时错误。
参数名称	目的
config	保留供RunnableConfig内部工具使用
runtime	保留用于ToolRuntime参数（访问状态、上下文、存储）
要访问运行时信息，请使用ToolRuntime参数而不是命名您自己的参数config或runtime。

## 访问上下文

tool在能够访问运行时信息（例如对话历史记录、用户数据和持久内存）时，其功能最为强大。本节将介绍如何从tool内部访问和更新这些信息。

Tools can access runtime information through the ToolRuntime parameter, which provides:

| 组件 | 描述 | 使用场景 |
|------|------|----------|
| State（状态） | 短期记忆 - 当前对话期间存在的可变数据（消息、计数器、自定义字段） | 访问对话历史、追踪工具调用次数 |
| Context（上下文） | 调用时传递的不可变配置（用户ID、会话信息） | 基于用户身份个性化响应 |
| Store（存储） | 长期记忆 - 跨对话持久化保存的数据 | 保存用户偏好、维护知识库 |
| Stream Writer（流写入器） | 在工具执行期间发送实时更新 | 显示长时间运行操作的进度 |
| Execution Info（执行信息） | 当前执行的标识和重试信息（线程ID、运行ID、尝试次数） | 访问线程/运行ID、根据重试状态调整行为 |
| Server Info（服务器信息） | 在 LangGraph Server 上运行时的服务器特定元数据（助手ID、图ID、认证用户） | 访问助手ID、图ID或认证用户信息 |
| Config（配置） | 执行的 RunnableConfig | 访问回调、标签和元数据 |
| Tool Call ID（工具调用ID） | 当前工具调用的唯一标识符 | 关联日志和模型调用的工具调用 |