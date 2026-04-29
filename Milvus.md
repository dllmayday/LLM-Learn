下面介绍在 LangChain 框架中安装和使用 Milvus 向量数据库的方法，分为本地轻量体验和生产环境部署两种情况。

---

## 一、Milvus 简介

Milvus 是一个开源向量数据库，专门用于存储、索引和管理深度神经网络生成的向量嵌入，核心能力包括**高效的相似性搜索**、**可扩展的索引**以及**混合检索（稀疏向量 + 密集向量）**。通过官方提供的 **`langchain-milvus`** 集成包，可以与 LangChain 无缝衔接，构建 RAG（检索增强生成）应用。


## 二、方式一：Milvus Lite（本地快速体验）

如果你在本机（Ubuntu 20.04+ 或 macOS 11.0+）进行开发测试，推荐使用 Milvus Lite。它是一个轻量级版本，直接以 `.db` 文件形式存储，无需启动任何后台服务。Milvus Lite 与 Milvus Standalone 共享相同的 API，一套代码可以在不同环境迁移。

**安装步骤：**

1. **安装 PyMilvus（内含 Milvus Lite）**
   ```bash
   pip install -U pymilvus
   ```
   Milvus Lite 已包含在 `pymilvus >= 2.4.2` 中，无需单独安装。

2. **安装 langchain-milvus 集成包**
   ```bash
   pip install -U langchain-milvus
   ```
   如果还需加载网页或使用 OpenAI embeddings，建议一次性安装：
   ```bash
   pip install langchain-milvus langchain-openai tiktoken bs4
   ```

3. **在代码中连接 Milvus Lite**
   只需将 `uri` 参数指定为一个本地文件路径即可。如果文件不存在，程序会自动创建。
   ```python
   from langchain_milvus import Milvus
   from langchain_openai import OpenAIEmbeddings

   embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

   vector_store = Milvus(
       embedding_function=embeddings,
       connection_args={"uri": "./milvus_demo.db"},
       index_params={"index_type": "FLAT", "metric_type": "L2"},
   )
   ```
> ⚠️ **数据规模提醒**：Milvus Lite 适合小规模原型开发（通常少于 100 万条向量），一旦超过该规模，建议切换到 Milvus Standalone。


## 三、方式二：Milvus Standalone（Docker 部署，适合开发/生产测试）

若数据量较大（超过百万级向量），使用 Docker 部署的 Milvus Standalone 性能更优，支持 IVF、HNSW 等多种高效索引。

### 方案 A：一键脚本启动（最简单）

Milvus 官方提供了一个脚本，通过 `curl` 和 `bash` 一键启动 Standalone 容器：

```bash
# 下载安装脚本
curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh

# 启动 Milvus 容器
bash standalone_embed.sh start

# 可选：停止 Milvus
bash standalone_embed.sh stop
```

成功启动后：
- Milvus 服务在 **19530** 端口监听
- Milvus WebUI 可通过 `http://127.0.0.1:9091/webui/` 访问，查看实例详情

### 方案 B：Docker Compose 配置（更具可控性）

通过 `docker-compose.yml` 管理多个组件（Milvus、etcd、MinIO），适合生产环境的长期部署：

```bash
# 下载配置文件
wget https://github.com/milvus-io/milvus/releases/download/v2.6.14/milvus-standalone-docker-compose.yml -O docker-compose.yml

# 启动服务（后台运行）
sudo docker compose up -d
```

启动完成后，查看容器状态：
```bash
sudo docker compose ps
```

输出应包含 `milvus-standalone`、`milvus-etcd`、`milvus-minio` 三个容器，均处于活动状态。

### 在 LangChain 中连接 Docker Milvus

连接参数只需将 `uri` 改为 Milvus 服务的地址和端口：

```python
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = Milvus(
    embedding_function=embeddings,
    connection_args={"uri": "http://localhost:19530"},
    collection_name="my_collection",
)
```


## 四、方式三：Milvus 分布式集群（生产级部署）

若需处理**十亿级**向量、支撑大规模 RAG 系统，推荐使用 Milvus 分布式集群。日常采用 Kubernetes + Milvus Operator 部署，但涉及专用的存储和运维团队。开发阶段建议使用托管云方案（如 Zilliz Cloud），无需自行运维。

### 如何在 LangChain 中连接分布式 Milvus

与 Standalone 完全相同，只需修改 `uri` 和 `token`：

```python
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
vector_store = Milvus(
    embedding_function=embeddings,
    connection_args={
        "uri": "https://xxx.api.gcp-us-west1.zillizcloud.com",  # 集群公网访问端点
        "token": "your_api_key_or_username:password",
    },
    collection_name="production_collection",
)
```


## 五、LangChain 中的完整代码示例

以下是一个完整的 RAG 流程：加载网页文档 → 文本分块 → 生成向量 → 存储至 Milvus → 执行相似性检索。

```python
import os
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

# 1. 设置 OpenAI API Key
os.environ["OPENAI_API_KEY"] = "your-api-key"

# 2. 加载文档
loader = WebBaseLoader("https://milvus.io/docs/overview.md")
docs = loader.load()

# 3. 文本分块
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
documents = text_splitter.split_documents(docs)

# 4. 生成向量并存入 Milvus（使用 Lite 本地模式）
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = Milvus.from_documents(
    documents=documents,
    embedding=embeddings,
    connection_args={"uri": "./milvus_demo.db"},   # Lite 模式
    collection_name="doc_qa_db",
)

# 5. 构建检索器并执行语义查询
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
query = "What is Milvus?"
results = retriever.invoke(query)

for doc in results:
    print(f"Content: {doc.page_content[:200]}...\n---\n")
```

### 几点说明：
- 若需持久化数据，可将 `uri` 修改为 Milvus Server 的远程地址（如 `http://localhost:19530`）。
- Milvus 还支持**混合检索**，即结合语义搜索（密集向量）与 BM25 全文检索（稀疏向量），适合精确术语类查询。更多细节可参考 [LangChain + Milvus 混合检索官方示例](https://milvus.io/docs/milvus_hybrid_search_retriever.md)。


## 总结：如何选择部署方式

| 部署方式 | 适用场景 | 推荐索引类型 | 数据量上限 |
|---|---|---|---|
| **Milvus Lite** | 本地开发、Jupyter Notebook | FLAT | < 100 万条 |
| **Milvus Standalone (Docker)** | 开发/测试、中型应用 | IVF、HNSW | 数百万～千万级 |
| **Milvus 集群 / 全托管云** | 高并发、亿万级 RAG 服务 | DiskANN、HNSW 等任意索引 | 十亿级以上 |

综合来看，日常开发先用 **Milvus Lite** 跑通流程，需要更优性能时再切换到 **Docker Standalone**，生产环境则可以直接使用分布式或全托管方案。这种渐进模式可以最大程度降低前期投入成本。