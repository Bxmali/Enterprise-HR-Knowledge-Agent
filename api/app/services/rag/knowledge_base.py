import os
import json
from typing import Dict, List

from langchain_core.documents import Document

from api.app.core.config import settings
from api.app.services.rag.document_loader import DocumentLoaderService
from api.app.services.rag.preprocessor import DocumentPreprocessor
from api.app.services.rag.splitter import SmallToBigSplitter
from api.app.services.rag.vector_store import VectorStoreService


class KnowledgeBaseService:
    """
    知识库构建服务。

    负责完整的入库流程：
    文件路径
    → 文件解析
    → 数据清洗
    → Small-to-Big 切片
    → Child Chunk 入向量库
    → Parent Chunk 保存到本地 docstore

    说明：
    为了让项目简单可跑，parent docstore 暂时使用 JSON 文件。
    企业级可以替换成 MySQL / PostgreSQL / MongoDB。
    """

    def __init__(self):
        self.loader = DocumentLoaderService()
        self.preprocessor = DocumentPreprocessor()
        self.splitter = SmallToBigSplitter()
        self.vector_store = VectorStoreService()

        self.parent_store_path = os.path.join(settings.upload_dir, "parent_docstore.json")
        os.makedirs(settings.upload_dir, exist_ok=True)

        if not os.path.exists(self.parent_store_path):
            with open(self.parent_store_path, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

    def _load_parent_store(self) -> Dict:
        with open(self.parent_store_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_parent_store(self, data: Dict) -> None:
        with open(self.parent_store_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def create_knowledge(
        self,
        file_path: str,
        employee_id: int | None = None,
        department_id: int | None = None,
    ) -> Dict:
        """
        创建知识库。

        employee_id / department_id 会写入 metadata，
        这样后续可以实现：
        - 只查某个员工的资料
        - 只查某个部门的知识库
        """

        raw_docs = self.loader.load(file_path)
        cleaned_docs = self.preprocessor.to_markdown_document(raw_docs)

        for doc in cleaned_docs:
            doc.metadata["employee_id"] = str(employee_id) if employee_id is not None else "0"
            doc.metadata["department_id"] = str(department_id) if department_id is not None else "0"

        parent_docs, child_docs = self.splitter.split(cleaned_docs)

        # 保存 parent chunk
        parent_store = self._load_parent_store()
        for parent in parent_docs:
            parent_id = parent.metadata["parent_id"]
            parent_store[parent_id] = {
                "content": parent.page_content,
                "metadata": parent.metadata,
            }
        self._save_parent_store(parent_store)

        # child chunk 入向量库
        self.vector_store.add_documents(child_docs)

        return {
            "file_path": file_path,
            "parent_chunks": len(parent_docs),
            "child_chunks": len(child_docs),
            "message": "知识库创建成功",
        }

    def get_parent_by_id(self, parent_id: str) -> str:
        parent_store = self._load_parent_store()
        item = parent_store.get(parent_id)
        if not item:
            return ""
        return item["content"]
