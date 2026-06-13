# Enterprise HR Knowledge Agent

## 企业级 HR 知识智能体系统

Enterprise HR Knowledge Agent 是一个基于 FastAPI、LangChain、DeepSeek、MySQL 和 Chroma/Qdrant 构建的企业知识管理与智能问答平台。

Enterprise HR Knowledge Agent is an AI-powered enterprise HR knowledge assistant built with FastAPI, LangChain, DeepSeek, MySQL and Chroma/Qdrant.

系统将结构化员工数据（MySQL）与非结构化企业文档（向量数据库）结合，通过 RAG（Retrieval-Augmented Generation）技术实现企业制度查询、员工档案分析、绩效信息检索、知识库问答等场景。

The system combines structured employee records with unstructured enterprise documents through Retrieval-Augmented Generation (RAG) to provide intelligent HR knowledge retrieval and analysis.

---

# 项目亮点 | Project Highlights

## 1. 混合数据架构 | Hybrid Data Architecture

### 结构化数据（MySQL）

存储：

- 员工档案
- 部门信息
- 薪资信息
- 绩效数据
- 组织架构

### Structured Data (MySQL)

Stores:

- Employee Records
- Department Information
- Salary Information
- Performance Data
- Organizational Structure

### 非结构化数据（Chroma / Qdrant）

存储：

- 公司制度
- 员工简历
- 培训资料
- 项目文档
- 绩效评语
- 招聘资料

### Unstructured Data (Chroma / Qdrant)

Stores:

- Company Policies
- Employee Resumes
- Training Materials
- Project Documents
- Performance Reviews
- Recruitment Documents

---

# 核心功能 | Core Features

## 员工管理 | Employee Management

- 员工档案管理
- 员工绩效管理
- 部门管理
- 员工查询

Employee records, performance management, department management and employee search.

## 企业知识库 | Enterprise Knowledge Base

支持：

- PDF
- DOCX
- TXT
- CSV
- Markdown

Supports PDF, DOCX, TXT, CSV and Markdown ingestion.

## RAG 检索增强 | Retrieval-Augmented Generation

- 文档解析
- 数据清洗
- Markdown标准化
- Small-to-Big Chunking
- Embedding
- Vector Search

## AI Agent

支持：

- 企业制度问答
- 员工信息分析
- 绩效分析
- 企业知识问答
- 多轮对话

Supports company policy QA, employee analysis, performance review and conversational AI.

## 记忆系统 | Memory System

- 短期会话记忆
- 长期记忆设计
- 用户画像设计

Short-term memory, long-term memory architecture and user profile memory.

---

# 企业级 RAG 流程 | Enterprise RAG Pipeline

```text
文件上传 Upload

        ↓

文档解析 Document Parsing

        ↓

数据清洗 Data Cleaning

        ↓

Markdown标准化

        ↓

Small-to-Big Chunking

        ↓

Embedding

        ↓

Chroma / Qdrant

        ↓

Retriever

        ↓

DeepSeek LLM

        ↓

Answer Generation
```

---

# 技术栈 | Technology Stack

| Layer | Technology |
|---------|------------|
| Frontend | Streamlit |
| Backend | FastAPI |
| LLM | DeepSeek |
| Framework | LangChain |
| Database | MySQL |
| Vector Database | Chroma / Qdrant |
| ORM | SQLAlchemy |
| Embedding | DashScope Embeddings |
| File Parsing | PyPDFLoader / Docx2txtLoader |
| Config | python-dotenv |

---

# 项目结构 | Project Structure

```text
hr_agent_rag_project/

├── api/
│   ├── routes/
│   ├── services/
│   ├── db/
│   └── models/
│
├── interface/
│   └── app.py
│
├── scripts/
│   └── init_db.py
│
├── data/
│   ├── uploads/
│   ├── chroma_db/
│   └── parent_store/
│
├── requirements.txt
├── .env.example
└── README.md
```

---

# 快速启动 | Quick Start

## 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置环境变量

```env
DEEPSEEK_API_KEY=your_key
DASHSCOPE_API_KEY=your_key
MYSQL_URL=mysql+pymysql://root:password@localhost:3306/hr_agent
```

## 初始化数据库

```bash
PYTHONPATH=. python scripts/init_db.py
```

## 启动 FastAPI

```bash
PYTHONPATH=. python -m uvicorn api.app.main:app --reload --port 8000
```

## 启动 Streamlit

```bash
PYTHONPATH=. python -m streamlit run interface/app.py
```

---

# Roadmap

- [ ] LangGraph Memory
- [ ] Hybrid Search
- [ ] Rerank Pipeline
- [ ] Qdrant Deployment
- [ ] RBAC Permission System
- [ ] Docker Deployment
- [ ] Kubernetes Deployment

---

# License

MIT License
