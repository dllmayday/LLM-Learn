
## 目录结构
rag-demo/
├── app.py              # Web入口
├── rag/
│   ├── ingest.py      # 文档入库
│   ├── retrieve.py    # 检索
│   ├── generate.py    # 生成回答
│   └── vector_store.py
├── data/              # 原始文档
├── index/             # 向量索引
└── requirements.txt

## 环境准备

```
pip install fastapi uvicorn faiss-cpu requests

sudo snap install ollama
```

安装 Ollama（并启动）：
```
//拉去embedding模型 用于数据向量化
ollama pull nomic-embed-text

//拉去生成模型（LLM） 
ollama pull phi3

ollama run phi3
```

## 数据准备

    Gutenberg: 这是一个包含 3,036 本英文书籍的合集，作者共 142 位。该合集是古腾堡计划语料库的一小部分。所有书籍均经过人工清理，尽可能地去除了元数据、许可信息和转录者注
    [Gutenberg Dataset](https://shibamoulilahiri.github.io/gutenberg_dataset.html)

## 运行

### 文档入库:
```
python3 rag/ingest.py
```
注意： Gutenberg数据集太大可能入库耗时很长，可通过建设文件数量减少耗时

### 启动：

uvicorn app:app --reload

### 测试

#### 浏览器访问：

http://localhost:8000/ask?q=你的问题

#### python脚本测试

python3 ask.py