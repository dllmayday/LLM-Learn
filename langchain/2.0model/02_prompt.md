## 02_prompt.py
这是一个 LangChain 提示词模板 的基础示例，展示了如何构建可动态替换变量的对话式提示。
核心组件
组件	说明
ChatPromptTemplate	LangChain 的提示模板类，用于结构化对话消息
from_messages()	静态工厂方法，从消息列表创建模板
("system", ...)	系统消息：定义 AI 助手的角色/行为
("human", ...)	用户消息：包含占位符 {question}
关键设计
角色化提示：通过 {role} 变量实现动态角色定义，使同一个模板可复用于不同场景（Kubernetes、Python、Docker 等）

消息元组格式：("type", "content") - 元组第一个元素标识消息来源，第二个元素是实际内容

延迟绑定：变量替换发生在 invoke() 调用时，而非模板创建时

代码流程
code
创建模板 → 定义角色=Kubernetes，问题=What is a Pod? → invoke() 触发替换
调用 invoke() 后，formatted 对象会包含最终渲染的消息内容，可直接传给大模型。
