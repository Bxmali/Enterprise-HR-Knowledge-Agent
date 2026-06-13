import os
from typing import List, Optional, Dict

from langchain_core.documents import Document
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma

from api.app.core.config import settings


class VectorStoreService:
    """
    向量数据库服务。

    默认使用 Chroma：
    - 适合本地开发和学习
    - 类似 SQLite，轻量、简单

    预留 Qdrant：
    - 适合企业部署
    - 类似 MySQL，是独立服务型向量数据库
    """

    def __init__(self):
        self.embedding = DashScopeEmbeddings(
            model=settings.embedding_model,
            dashscope_api_key=settings.dashscope_api_key,
        )

        if settings.vector_backend == "chroma":
            self.vector_store = Chroma(
                collection_name=settings.chroma_collection,
                embedding_function=self.embedding,
                persist_directory=settings.chroma_persist_dir,
            )
        elif settings.vector_backend == "qdrant":
            # 为了让项目默认能跑，Qdrant 写成懒加载示例。
            # 如果需要启用，请先：
            # docker run -p 6333:6333 qdrant/qdrant
            from langchain_qdrant import QdrantVectorStore

            self.vector_store = QdrantVectorStore.from_existing_collection(
                embedding=self.embedding,
                collection_name=settings.qdrant_collection,
                url=settings.qdrant_url,
            )
        else:
            raise ValueError(f"未知向量数据库类型: {settings.vector_backend}")

    def add_documents(self, docs: List[Document]) -> None:
        """
        将文档写入向量数据库。
        通常写入 child chunk。
        """
        if not docs:
            return
        self.vector_store.add_documents(docs)

    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter: Optional[Dict] = None,
    ) -> List[Document]:
        """
        向量相似度检索。

        参数：
        - query：用户问题
        - k：返回多少条
        - filter：metadata 过滤条件，例如按员工、部门、文件类型过滤
        """
        try:
            return self.vector_store.similarity_search(query, k=k, filter=filter)
        except TypeError:
            # 某些向量库 filter 参数格式不同，学习阶段先兼容无 filter。
            return self.vector_store.similarity_search(query, k=k)
