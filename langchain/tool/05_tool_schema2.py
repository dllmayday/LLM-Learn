import os
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from openai import OpenAI

# ==================== 配置 ====================
# 阿里云百炼配置
api_key = os.getenv("DASHSCOPE_API_KEY")
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
model_name = "qwen-plus"  # 或 "qwen-max"

# ==================== 方式1：通用联网搜索工具 ====================

@tool
def web_search(query: str) -> str:
    """联网搜索实时信息：天气、新闻、数据等"""
    try:
        client = OpenAI(base_url=base_url, api_key=api_key)
        response = client.responses.create(
            model=model_name,
            input=[{"role": "user", "content": query}],
            tools=[{"type": "web_search", "max_keyword": 3}],  # 启用联网搜索
        )
        return response.output_text
    except Exception as e:
        return f"搜索失败：{str(e)}"


# ==================== 方式2：专门的天气查询工具（推荐）====================

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


# ==================== 方式3：增强版天气查询（带结果优化）====================

@tool
def get_weather_enhanced(location: str) -> str:
    """获取指定城市的详细天气信息，包括温度、湿度、风力等"""
    
    # 构建更精确的查询
    query = f"""请提供{location}的以下天气信息：
1. 当前温度（摄氏度）
2. 天气状况（晴、雨、多云等）
3. 湿度
4. 风力风向
5. 体感温度
6. 空气质量

请用简洁清晰的格式返回。"""
    
    try:
        client = OpenAI(base_url=base_url, api_key=api_key)
        response = client.responses.create(
            model=model_name,
            input=[{"role": "user", "content": query}],
            tools=[{"type": "web_search", "max_keyword": 5}],  # 增加搜索关键词
        )
        
        return response.output_text
        
    except Exception as e:
        return f"获取{location}天气信息失败：{str(e)}"


# ==================== 方式4：多城市天气对比 ====================

@tool
def compare_weather(cities: str) -> str:
    """对比多个城市的天气，参数为逗号分隔的城市名，如：北京,上海,深圳"""
    
    query = f"请对比以下城市的天气情况：{cities}，包括温度、天气状况"
    
    try:
        client = OpenAI(base_url=base_url, api_key=api_key)
        response = client.responses.create(
            model=model_name,
            input=[{"role": "user", "content": query}],
            tools=[{"type": "web_search", "max_keyword": 5}],
        )
        
        return response.output_text
        
    except Exception as e:
        return f"天气对比失败：{str(e)}"


# ==================== 创建 Agent ====================

def create_weather_agent():
    """创建天气查询助手"""
    
    agent = create_agent(
        model=ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=0.3,  # 较低温度保证准确性
        ),
        tools=[
            get_weather,           # 标准天气查询
            get_weather_enhanced,  # 增强版天气查询
            compare_weather,       # 多城市对比
            web_search,           # 通用搜索
        ],
        system_prompt="""你是一个专业的天气助手，可以帮助用户查询天气信息。

重要规则：
1. 当用户询问天气时，优先使用 get_weather 工具
2. 如果用户需要详细的天气信息（如湿度、风力等），使用 get_weather_enhanced
3. 如果用户想对比多个城市天气，使用 compare_weather
4. 对于其他联网查询需求，使用 web_search
5. 回答时要清晰、准确，温度使用摄氏度（除非用户要求华氏度）
6. 如果工具返回错误，友好地告知用户并建议稍后重试"""
    )
    
    return agent


# ==================== 测试函数 ====================

def test_basic_weather():
    """测试基本天气查询"""
    print("\n" + "="*60)
    print("测试1：基本天气查询")
    print("="*60)
    
    agent = create_weather_agent()
    
    test_cases = [
        "北京今天天气怎么样？",
        "上海明天会下雨吗？",
        "深圳现在多少度？",
    ]
    
    for query in test_cases:
        print(f"\n👤 用户: {query}")
        try:
            result = agent.invoke({
                "messages": [{"role": "user", "content": query}]
            })
            print(f"🤖 助手: {result['messages'][-1].content}")
            print("-"*60)
        except Exception as e:
            print(f"❌ 错误: {e}")


def test_weather_with_forecast():
    """测试包含天气预报的查询"""
    print("\n" + "="*60)
    print("测试2：天气预报查询")
    print("="*60)
    
    agent = create_weather_agent()
    
    test_cases = [
        "查询北京未来3天天气",
        "上海一周天气预报",
        "深圳周末天气怎么样？",
    ]
    
    for query in test_cases:
        print(f"\n👤 用户: {query}")
        try:
            result = agent.invoke({
                "messages": [{"role": "user", "content": query}]
            })
            print(f"🤖 助手: {result['messages'][-1].content}")
            print("-"*60)
        except Exception as e:
            print(f"❌ 错误: {e}")


def test_enhanced_weather():
    """测试详细天气查询"""
    print("\n" + "="*60)
    print("测试3：详细天气查询（湿度、风力等）")
    print("="*60)
    
    agent = create_weather_agent()
    
    query = "杭州天气怎么样？要包括湿度、风力、空气质量"
    
    print(f"\n👤 用户: {query}")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
        print(f"🤖 助手: {result['messages'][-1].content}")
        print("-"*60)
    except Exception as e:
        print(f"❌ 错误: {e}")


def test_city_comparison():
    """测试多城市对比"""
    print("\n" + "="*60)
    print("测试4：多城市天气对比")
    print("="*60)
    
    agent = create_weather_agent()
    
    query = "对比一下北京、上海、广州的天气"
    
    print(f"\n👤 用户: {query}")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
        print(f"🤖 助手: {result['messages'][-1].content}")
        print("-"*60)
    except Exception as e:
        print(f"❌ 错误: {e}")


def test_temperature_unit():
    """测试温度单位转换"""
    print("\n" + "="*60)
    print("测试5：华氏度查询")
    print("="*60)
    
    agent = create_weather_agent()
    
    test_cases = [
        "纽约现在多少度？用华氏度",
        "伦敦天气怎么样？我要华氏度",
    ]
    
    for query in test_cases:
        print(f"\n👤 用户: {query}")
        try:
            result = agent.invoke({
                "messages": [{"role": "user", "content": query}]
            })
            print(f"🤖 助手: {result['messages'][-1].content}")
            print("-"*60)
        except Exception as e:
            print(f"❌ 错误: {e}")


# ==================== 交互式模式 ====================

def interactive_mode():
    """交互式天气查询模式"""
    
    print("\n" + "="*60)
    print("🌤️ 联网天气查询助手")
    print("="*60)
    print("支持查询：")
    print("  • 实时天气")
    print("  • 天气预报")
    print("  • 详细天气信息（湿度、风力等）")
    print("  • 多城市天气对比")
    print("  • 支持摄氏度/华氏度")
    print("\n输入 'exit' 退出程序")
    print("-"*60)
    
    agent = create_weather_agent()
    
    while True:
        try:
            user_input = input("\n👤 你: ").strip()
            
            if user_input.lower() in ['exit', 'quit', '退出', 'q']:
                print("👋 再见！")
                break
            
            if not user_input:
                continue
            
            print("🤖 思考中...")
            result = agent.invoke({
                "messages": [{"role": "user", "content": user_input}]
            })
            
            print(f"🤖 助手: {result['messages'][-1].content}")
            
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 出错: {e}")
            print("请稍后重试或换个问法")


# ==================== 直接使用工具的方式（不通过Agent）====================

def direct_tool_usage():
    """直接使用工具，不通过Agent"""
    print("\n" + "="*60)
    print("直接调用工具示例")
    print("="*60)
    
    # 直接调用天气工具
    result = get_weather.invoke({
        "location": "北京",
        "units": "celsius",
        "include_forecast": True
    })
    print(f"天气查询结果：\n{result}")


# ==================== 主函数 ====================

def main():
    """主函数"""
    
    # 检查API密钥
    if not api_key:
        print("❌ 错误：未设置 DASHSCOPE_API_KEY 环境变量")
        print("请运行：export DASHSCOPE_API_KEY='your-api-key'")
        return
    
    print("\n请选择运行模式：")
    print("1. 测试基本天气查询")
    print("2. 测试天气预报")
    print("3. 测试详细天气查询")
    print("4. 测试多城市对比")
    print("5. 测试温度单位转换")
    print("6. 运行所有测试")
    print("7. 交互式模式")
    print("8. 直接调用工具示例")
    
    choice = input("\n请输入选择 (1-8): ").strip()
    
    if choice == "1":
        test_basic_weather()
    elif choice == "2":
        test_weather_with_forecast()
    elif choice == "3":
        test_enhanced_weather()
    elif choice == "4":
        test_city_comparison()
    elif choice == "5":
        test_temperature_unit()
    elif choice == "6":
        test_basic_weather()
        test_weather_with_forecast()
        test_enhanced_weather()
        test_city_comparison()
        test_temperature_unit()
    elif choice == "7":
        interactive_mode()
    elif choice == "8":
        direct_tool_usage()
    else:
        print("无效选择，运行交互式模式")
        interactive_mode()


if __name__ == "__main__":
    main()