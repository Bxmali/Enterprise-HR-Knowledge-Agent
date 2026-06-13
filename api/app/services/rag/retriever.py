from typing import Optional, Dict, List
from langchain_core.documents import Document

from api.app.services.rag.vector_store import VectorStoreService
from api.app.services.rag.knowledge_base import KnowledgeBaseService


class RetrieverService:
    """
    检索服务。

    当前实现：
    - 向量检索 child chunk
    - 根据 parent_id 找 parent chunk
    - 返回更完整的大块上下文

    这就是 Small-to-Big 的查询阶段。
    """

    def __init__(self):
        self.vector_store = VectorStoreService()
        self.kb_service = KnowledgeBaseService()

    def retrieve(
        self,
        query: str,
        employee_id: Optional[int] = None,
        department_id: Optional[int] = None,
        k: int = 5,
    ) -> str:
        metadata_filter: Dict = {}

        if employee_id is not None:
            metadata_filter["employee_id"] = employee_id

        if department_id is not None:
            metadata_filter["department_id"] = department_id

        docs: List[Document] = self.vector_store.similarity_search(
            query=query,
            k=k,
            filter=metadata_filter if metadata_filter else None,
        )

        if not docs:
            return "无相关知识库内容。"

        parent_contents = []
        seen_parent_ids = set()

        for doc in docs:
            parent_id = doc.metadata.get("parent_id")

            if not parent_id or parent_id in seen_parent_ids:
                continue

            seen_parent_ids.add(parent_id)
            parent_text = self.kb_service.get_parent_by_id(parent_id)

            if parent_text:
                parent_contents.append(parent_text)
            else:
                parent_contents.append(doc.page_content)

        return "\n\n---\n\n".join(parent_contents)
