# mcp_weather_server_fixed.py
import asyncio
from mcp.server import Server, InitializationOptions
import mcp.server.stdio
import mcp.types as types
from mcp.types import ServerCapabilities  # 新增导入

# ---------- 工具实现 ----------
def get_user_location(user_id: str) -> str:
    return "Florida" if user_id == "1" else "SF"

def get_weather_for_location(city: str) -> str:
    return f"{city}总是阳光明媚！"

# ---------- 创建服务器 ----------
server = Server("weather-assistant")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_user_location",
            description="根据用户 ID 获取用户所在位置",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "用户的唯一标识符"}
                },
                "required": ["user_id"],
            },
        ),
        types.Tool(
            name="get_weather_for_location",
            description="获取指定城市的天气信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["city"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    if not arguments:
        arguments = {}
    if name == "get_user_location":
        user_id = arguments.get("user_id")
        if not user_id:
            return [types.TextContent(type="text", text="错误：缺少 user_id 参数")]
        location = get_user_location(user_id)
        return [types.TextContent(type="text", text=location)]
    elif name == "get_weather_for_location":
        city = arguments.get("city")
        if not city:
            return [types.TextContent(type="text", text="错误：缺少 city 参数")]
        weather = get_weather_for_location(city)
        return [types.TextContent(type="text", text=weather)]
    else:
        raise ValueError(f"未知工具: {name}")

# ---------- 启动服务 ----------
async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        # 直接构造能力声明（支持工具）
        capabilities = ServerCapabilities(tools={})  # 关键修改
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="weather-assistant",
                server_version="1.0.0",
                capabilities=capabilities
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())