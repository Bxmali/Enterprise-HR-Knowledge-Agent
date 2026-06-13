import re
from typing import List
from langchain_core.documents import Document


class DocumentPreprocessor:
    """
    文档清洗与标准化模块。

    企业级 RAG 通常不会直接把 loader 结果存进向量库，
    而是先进行清洗，降低脏数据对检索效果的影响。

    当前实现：
    - 删除多余空白行
    - 删除连续空格
    - 删除简单页码
    - 统一换行
    - 转换为较干净的 Markdown 风格文本
    """

    def clean_text(self, text: str) -> str:
        # 统一换行符
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # 删除纯页码行，例如：1、2、- 3 -
        text = re.sub(r"(?m)^\s*-?\s*\d+\s*-?\s*$", "", text)

        # 多个空格合并
        text = re.sub(r"[ \t]+", " ", text)

        # 多个空行合并为两个换行
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def to_markdown_document(self, docs: List[Document]) -> List[Document]:
        """
        将 Document 列表清洗后返回新的 Document 列表。

        注意：
        真实企业中会进一步做：
        - 标题识别
        - 表格结构保留
        - 页眉页脚识别
        - 文档章节树构建
        """
        cleaned_docs = []

        for doc in docs:
            cleaned_text = self.clean_text(doc.page_content)

            if not cleaned_text:
                continue

            cleaned_docs.append(
                Document(
                    page_content=cleaned_text,
                    metadata=doc.metadata,
                )
            )

        return cleaned_docs
