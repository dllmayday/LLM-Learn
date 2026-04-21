## 01_model.py 

这是一段 连接火山引擎方舟 API 并调用大模型 的完整示例。

核心流程
code
环境变量 → 模型配置 → API 调用 → 响应解析
关键点解析
部分	说明
ARK_API_KEY	从环境变量读取 API 密钥，避免硬编码泄露
base_url	火山引擎方舟 API 端点（北京区域）
ChatOpenAI	LangChain 封装的 OpenAI 兼容接口，可直连第三方 API
model="glm-4-7-251222"	智谱 GLM-4 模型的具体版本
响应对象结构
python
response.usage_metadata        # Token 用量统计
response.content              # 模型生成的文本回复
response.response_metadata    # 元数据字典
设计亮点
OpenAI 兼容接口：通过 langchain_openai + 自定义 base_url，无缝对接非 OpenAI 的 API 提供商
环境变量配置：密钥不硬编码，符合安全最佳实践
完整元信息输出：打印 finish_reason 可用于监控模型停止原因（正常完成/截断/过长等）
**注意事项**
```python
# 实际使用时需确保环境变量已设置
# export ARK_API_KEY="your-api-key-here"
```
这段代码展示了 LangChain 的 Provider 无关设计——同一套代码可轻松切换不同的 LLM 后端。





