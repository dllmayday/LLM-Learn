
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

## Linux 环境准备

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
##  Windows 环境准备
### python安装 
    [Python Download](https://www.python.org/downloads/)
    pip及python程序 安装在 C:\Users\[用户名]\AppData\Local\Python\bin目录下
    查看是否添加环境变量 PATH C:\Users\[用户名]\AppData\Local\Python\bin

### 安装faiss-cpu uvicorn fastapi requests
    ```powershell
    pip install fastapi uvicorn faiss-cpu requests
    ```
### 安装ollama
```powershell
irm https://ollama.com/install.ps1 | iex
```
### ollama 拉去模型及启动命令与Linux相同


## 数据准备

    Gutenberg: 这是一个包含 3,036 本英文书籍的合集，作者共 142 位。该合集是古腾堡计划语料库的一小部分。所有书籍均经过人工清理，尽可能地去除了元数据、许可信息和转录者注
    [Gutenberg Dataset](https://shibamoulilahiri.github.io/gutenberg_dataset.html)

## 运行

### 文档入库:
```
python3 rag/ingest.py
```
注意： Gutenberg数据集太大可能入库耗时很长，可通过建设文件数量减少耗时

### Linux 环境启动：

uvicorn app:app --reload

### Windows 环境启动
py -m uvicorn app:app --reload

### 测试

#### 浏览器访问：

http://localhost:8000/ask?q=你的问题

#### python脚本测试

python3 ask.py

**注意：** 在设备性能较差的情况下可以拉取轻量模型qwen2.5:0.5b，phi3:mini等模型提高速度。

## 模型选择
### Phi-3-mini
#### Phi-3-mini 最小硬件配置（INT4 量化 / Ollama）
✅ 绝对最低（纯 CPU，能跑但慢）
CPU：4 核（支持 AVX2）
内存：8GB RAM（系统 + 模型共占 5–6GB）
存储：≥5GB 可用空间（模型约 2.3GB）
系统：Windows 10/11 64 位
显卡：无（纯 CPU 推理）
速度：1–3 tokens / 秒（很慢，仅测试用）
✅ 推荐最小（流畅可用）
CPU：6 核 / 8 核（i5-12400P / R5 5600U 以上）
内存：16GB RAM（推荐）
显卡：NVIDIA（GTX 1660 Ti / RTX 3050 6GB+）
显存：≥6GB（INT4 约 4.5GB）
存储：SSD（加载更快）
速度：15–30 tokens / 秒（正常对话）
#### 不同量化的显存占用（Phi-3-mini-4k）
FP16：约 10.6GB（4k 上下文）
INT8：约 6GB
INT4（Ollama）：约 4.5GB（最小）
### Qwen2.5:0.5B
#### Qwen2.5-0.5B 最小硬件配置（INT4 量化 / Ollama）
✅ 绝对最低（纯 CPU，能跑、仅测试）
CPU：2 核（支持 AVX2）
内存：4GB RAM（系统 + 模型共占 2–3GB）
存储：≥1GB 可用空间（INT4 模型约 0.4GB）
系统：Windows 10/11 64 位、macOS、Linux
显卡：无（纯 CPU 推理）
速度：5–10 tokens / 秒（轻量对话可用）
✅ 推荐最小（流畅日常）
CPU：4 核 / 6 核（i3-12100 / R5 5500U 以上）
内存：8GB RAM（推荐）
显卡：NVIDIA（GTX 1050 Ti / MX570 2GB+）
显存：≥1GB（INT4 约 0.5GB）
存储：SSD（加载更快）
速度：30–60 tokens / 秒（流畅对话、轻量代码）
#### 不同量化的显存 / 内存占用（Qwen2.5-0.5B-32k）
FP16：约 1.1GB（32k 上下文，含基础开销）
INT8：约 0.6GB
INT4（Ollama Q4_K_M）：约 0.5GB（最小，最省资源）
### 优化建议（低配必开）
用 Ollama 默认 INT4（最小显存）
限制上下文：ollama run phi3:mini --context-window 2048
关闭后台软件，释放内存
纯 CPU 时：设置线程 set OLLAMA_CPU_THREADS=8
启用 GPU 加速：ollama run qwen2.5:0.5b --gpu-layers 20（NVIDIA 显卡）