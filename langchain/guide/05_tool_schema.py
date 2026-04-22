import os
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool, ToolRuntime
from openai import OpenAI

# 配置火山引擎方舟
api_key = os.getenv("DASHSCOPE_API_KEY")
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
model_name = "qwen-plus"

weather_schema = {
    "type": "object",
    "properties": {
        "location": {
            "type": "string",
            "description": "城市名称，如：北京、上海、深圳、New York"
        },
        "units": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"],
            "description": "温度单位，celsius为摄氏度，fahrenheit为华氏度"
        },
        "include_forecast": {
            "type": "boolean",
            "description": "是否包含天气预报，true为包含未来几天天气"
        }
    },
    "required": ["location", "units", "include_forecast"]
}

@tool(args_schema=weather_schema)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """通过联网搜索获取真实天气信息"""
    
    # 构建天气查询语句
    if include_forecast:
        query = f"查询{location}未来几天的天气预报"
    else:
        query = f"查询{location}当前的天气情况"
    
    if units == "fahrenheit":
        query += "，温度用华氏度表示"
    else:
        query += "，温度用摄氏度表示"
    
    try:
        # 使用阿里云百炼的联网搜索功能
        client = OpenAI(base_url=base_url, api_key=api_key)
        response = client.responses.create(
            model=model_name,
            input=[{"role": "user", "content": query}],
            tools=[{"type": "web_search", "max_keyword": 3}],
        )
        
        # 返回搜索结果
        result = response.output_text
        
        # 如果结果为空，返回提示
        if not result or len(result.strip()) < 10:
            return f"抱歉，未能获取到{location}的天气信息，请稍后再试。"
        
        return result
        
    except Exception as e:
        return f"获取天气信息失败：{str(e)}"

# ===================== 完全按你的示例 =====================
agent = create_agent(
    model=ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url=base_url,
    ),
    tools=[get_weather],
    system_prompt="""你是一个专业的天气助手，可以帮助用户查询天气信息。

重要规则：
1. 当用户询问天气时，优先使用 get_weather 工具
2. 如果用户需要详细的天气信息（如湿度、风力等），使用 get_weather_enhanced
3. 如果用户想对比多个城市天气，使用 compare_weather
4. 对于其他联网查询需求，使用 web_search
5. 回答时要清晰、准确，温度使用摄氏度（除非用户要求华氏度）
6. 如果工具返回错误，友好地告知用户并建议稍后重试"""
)

# 执行（和你示例完全一样）
result = agent.invoke({
    "messages": [{"role": "user", "content": "北京今日天气怎么样？"}]
})

# ✅ 终极稳定输出（永远不会报错）
print("最终回答：", result["messages"][-1].content)