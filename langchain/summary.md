

参考链接：[docs.langchain.com官网](https://docs.langchain.com/oss/python/langchain/overview)
参考链接：[langchain-doc.cn](https://langchain-doc.cn/)
参考链接：[www.langchain.com.cn](https://www.langchain.com.cn/docs/introduction/)

## 模型

## 模型调用
必须调用聊天模型才能生成输出。有三种主要的调用方法，每种方法都适用于不同的使用场景。
- invoke: 最简单的调用方法，直接返回结果。
- stream: 通过逐步显示输出，流式传输显著提升了用户体验，尤其是在处理较长的响应时
- batch:  将一系列独立的模型请求批量处理，可以显著提高性能并降低成本，因为可以并行处理这些请求.
默认情况下，batch()只会返回整个批次的最终输出。如果您希望在每个输入生成完成后立即接收其输出，可以使用以下方式流式传输结果batch_as_completed()：


