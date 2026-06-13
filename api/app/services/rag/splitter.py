import hashlib
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class SmallToBigSplitter:
    """
    Small-to-Big 智能切片策略。

    核心思想：
    - Parent Chunk：较大文本块，用于最终回答，保证上下文完整
    - Child Chunk：较小文本块，用于向量检索，保证召回精准

    检索流程：
    用户问题 → 检索 child chunk → 根据 parent_id 找 parent chunk → 返回 parent 给 LLM
    """

    def __init__(
        self,
        parent_chunk_size: int = 1500,
        parent_overlap: int = 150,
        child_chunk_size: int = 500,
        child_overlap: int = 80,
    ):
        self.parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=parent_chunk_size,
            chunk_overlap=parent_overlap,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""],
        )

        self.child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=child_chunk_size,
            chunk_overlap=child_overlap,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""],
        )

    def _hash(self, text: str) -> str:
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    def split(self, docs: List[Document]) -> Tuple[List[Document], List[Document]]:
        """
        返回：
        - parent_docs：大块文档，保存完整上下文
        - child_docs：小块文档，进入向量库检索
        """

        parent_docs = self.parent_splitter.split_documents(docs)
        all_child_docs = []

        for parent_index, parent in enumerate(parent_docs):
            parent_id = self._hash(parent.page_content + str(parent_index))

            parent.metadata["parent_id"] = parent_id
            parent.metadata["chunk_type"] = "parent"

            children = self.child_splitter.split_documents([parent])

            for child_index, child in enumerate(children):
                child.metadata["parent_id"] = parent_id
                child.metadata["chunk_type"] = "child"
                child.metadata["child_index"] = child_index
                child.metadata["parent_preview"] = parent.page_content[:200]

                all_child_docs.append(child)

        return parent_docs, all_child_docs
