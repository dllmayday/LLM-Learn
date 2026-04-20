# 火山引擎方舟大模型调用示例
基于 OpenAI 兼容 SDK 调用**火山引擎方舟**平台大模型，支持基础对话、联网搜索（Web Search）功能，开箱即用。

## 功能说明
本脚本提供两种调用示例：
1. **GLM-4 模型 + 联网搜索**：可查询实时信息（如天气、新闻等，需开通插件权限）
2. **豆包轻量版模型**：基础文本生成（代码实现、问答等）

## 环境准备
### 1. 安装依赖
```bash
pip install openai
# 如需使用原生Ark SDK可额外安装：pip install volcenginesdkarkruntime
```

### 2. 获取 API Key
1. 登录 [火山引擎方舟平台](https://console.volcengine.com/ark)
2. 创建并复制你的 **API_KEY**
3. **配置环境变量**：
   ```bash
   # Linux/Mac 终端执行
   export ARK_API_KEY="你的API_KEY"
   
   # Windows 终端执行
   set ARK_API_KEY=你的API_KEY
   ```

### 3. 联网搜索权限（可选）
如果需要使用 `web_search` 联网搜索功能：
1. 开通插件：https://console.volcengine.com/common-buy/CC_content_plugin
2. 开通后等待1-2分钟生效，否则会报错 `ToolNotOpen`

## 脚本使用说明
### 方式1：GLM-4 模型 + 联网搜索
适用场景：查询**实时信息**（天气、最新资讯、实时数据等）
```python
# 核心代码（已内置在脚本中）
tools = [{"type": "web_search", "max_keyword": 2}]
response = client.responses.create(
    model="glm-4-7-251222",
    input=[{"role": "user", "content": "北京的天气怎么样？"}],
    tools=tools,
)
```

### 方式2：豆包轻量版模型
适用场景：**通用文本生成**（写代码、问答、文案创作等），无联网需求
> 注释掉上方代码，取消下方代码注释即可运行

## 运行脚本
```bash
# 直接运行
python doubao.py
```

## 常见问题
### 1. 报错 404 ToolNotOpen
**原因**：未开通联网搜索插件
**解决**：访问 https://console.volcengine.com/common-buy/CC_content_plugin 开通

### 2. 认证失败/无权限
**原因**：API_KEY 配置错误
**解决**：检查环境变量 `ARK_API_KEY` 是否正确填写

### 3. 优化输出（推荐）
将 `print(response)` 替换为：
```python
# 直接输出模型回答文本，更简洁
print(response.output_text)
```

## 模型说明
- `glm-4-7-251222`：GLM-4 大模型，支持联网搜索
- `doubao-seed-2-0-lite-260215`：豆包轻量版模型，高效低成本

---

### README 总结
1. 一键安装依赖、配置API密钥即可运行
2. 分**联网搜索**和**基础对话**两种使用场景
3. 内置完整报错解决方案，新手友好
4. 支持火山引擎方舟全系列兼容模型