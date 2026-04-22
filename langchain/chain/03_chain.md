## 03_chain.py 

这段代码展示了 LangChain 的核心概念 **LCEL（LangChain Expression Language）**，用管道符 `|` 将三个组件串联成一条链。
---

### 第一部分：定义提示模板

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} expert. Be concise and helpful."),
    ("human", "{question}")
])
```

- `ChatPromptTemplate` 是一个模板工厂，`{role}` 和 `{question}` 是占位符
- `system` 消息设定 AI 的角色身份
- `human` 消息是用户的实际问题
- 调用时传入变量值，模板自动填充

---

### 第二部分：配置模型

```python
model = ChatOpenAI(
    model="glm-4-7-251222",
    api_key=api_key,
    base_url=base_url,  # 指向火山引擎，走 OpenAI 兼容接口
    temperature=0       # 0 = 输出确定性最高，不随机
)
```

---

### 第三部分：构建链并调用

```python
chain = prompt | model | StrOutputParser()
```

这是 LCEL 的精髓，数据流向如下：

```
invoke({"role": "DevOps", "question": "..."})
         ↓
      prompt          # 填充变量 → 生成格式化的消息列表
         ↓
      model           # 接收消息 → 调用 GLM API → 返回 AIMessage 对象
         ↓
  StrOutputParser     # 从 AIMessage 中提取纯文本字符串
         ↓
      response        # 最终得到一个普通字符串
```

`StrOutputParser` 的作用是把模型返回的 `AIMessage(content="...")` 对象，拆包成普通字符串，方便直接使用。

---

### 与不用 LCEL 的对比

```python
# 不用 LCEL 的写法（等价但繁琐）
messages = prompt.format_messages(role="DevOps", question="What is CI/CD?")
ai_message = model.invoke(messages)
response = ai_message.content

# LCEL 写法（简洁）
response = chain.invoke({"role": "DevOps", "question": "What is CI/CD?"})
```

LCEL 的优势在于链可以任意扩展，比如在 `model` 后面再接一个翻译链、摘要链等，只需继续用 `|` 串联。