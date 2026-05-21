import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from mcp.server import Server, InitializationOptions
from mcp.server.sse import SseServerTransport
import mcp.types as types

# ---------- 工具实现 ----------
def get_user_location(user_id: str) -> str:
    return "Florida" if user_id == "1" else "SF"

def get_weather_for_location(city: str) -> str:
    return f"{city}总是阳光明媚！"

# ---------- MCP 服务器 ----------
mcp_server = Server("weather-assistant")

@mcp_server.list_tools()
async def list_tools() -> list[types.Tool]:
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

@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
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

# ---------- SSE 传输 ----------
# 创建全局 SSE 传输对象，指定消息端点路径（用于 POST 请求）
sse_transport = SseServerTransport("/messages")

async def handle_sse(request: Request):
    """处理 SSE 连接（GET /sse）"""
    # 使用 request._send 获取底层的 ASGI send 函数
    async with sse_transport.connect_sse(
        request.scope, request.receive, request._send
    ) as (read_stream, write_stream):
        options = InitializationOptions(
            server_name="weather-assistant",
            server_version="1.0.0",
            capabilities=types.ServerCapabilities(tools={})
        )
        await mcp_server.run(read_stream, write_stream, options)
    # 连接关闭后返回（不会执行到这里，因为连接会一直保持直到客户端断开）
    return None

async def handle_messages(request: Request):
    """处理 POST 消息（POST /messages）"""
    await sse_transport.handle_post_message(
        request.scope, request.receive, request._send
    )
    return None

# 创建 Starlette 应用
app = Starlette(
    routes=[
        Route("/sse", handle_sse, methods=["GET"]),
        Route("/messages", handle_messages, methods=["POST"]),
    ]
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6274)