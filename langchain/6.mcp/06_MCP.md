# 创建并使用一个 MCP 服务
## 创建服务 
1. 安装依赖
```
pip install mcp mcp-proxy
```
2. 运行服务

stdio 服务 
```

python mcp_weather_server.py
```
sse 服务
``` 
python mcp_weather_server_sse.py
```

在 MCP（Model Context Protocol）中，**stdio** 和 **SSE** 是两种主要的传输方式，它们的区别如下：

| 维度 | stdio（标准输入/输出） | SSE（Server‑Sent Events） |
|------|----------------------|---------------------------|
| **通信机制** | 通过子进程的标准输入输出流传递 JSON‑RPC 消息（双向同步） | 基于 HTTP：客户端通过 GET 建立长连接接收事件（服务器推送），通过 POST 发送请求 |
| **网络支持** | 只能用于同一台机器上的进程间通信（本地） | 支持跨网络（包括公网），只要 URL 可访问 |
| **配置方式** | 客户端提供可执行命令（如 `python server.py`），由客户端启动子进程 | 客户端只需提供 HTTP/HTTPS 端点 URL（如 `http://localhost:6274/sse`），服务器需独立运行 |
| **典型场景** | 与本地 AI 助手（如 Cline、Claude Desktop）集成，工具与客户端运行在同一设备 | 远程调用、微服务架构、多客户端共享一个 MCP 服务器 |
| **资源消耗** | 每个客户端启动一个独立进程 | 一个服务进程可同时服务多个客户端（需处理并发） |
| **安全与认证** | 依赖操作系统进程隔离，通常无需额外认证 | 需要自行实现认证（如 token、API key）以防止未授权访问 |
| **调试难度** | 较简单：可直接在终端运行查看输出 | 稍复杂：涉及 HTTP 状态码、CORS、长连接保持等 |

---

## 如何选择？

- **仅本地使用**（例如为 Cline 或 Claude Desktop 开发工具）→ 优先用 **stdio**（配置简单，无需网络和认证）。
- **需要供其他人远程调用**（例如团队共享、云端部署）→ 使用 **SSE**（配合公网地址或内网穿透，如 ngrok）。

## 验证服务

```
npx @modelcontextprotocol/inspector python mcp_weather_server.py
```
当您运行 npx @modelcontextprotocol/inspector python mcp_weather_server_fixed.py 并成功看到 Inspector 界面
可在界面内测试验证的 MCP连接及查看工具列表等。

**SSE 服务配置文件示例 (Cline中的配置文件)** 添加后不报错即可使用 
```
{
  "mcpServers": {
    "weather-assistant": {
      "url": "http://localhost:6274/sse",
      "transport": "sse",
      "autoApprove": [
        "get_weather_for_location",
        "get_user_location"
      ]
    }
  }
}
```
## 服务

