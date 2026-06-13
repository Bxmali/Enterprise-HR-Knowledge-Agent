import os
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    CSVLoader,
)


class DocumentLoaderService:
    """
    文件解析服务。

    作用：
    把不同格式文件解析成 LangChain Document。

    支持：
    - txt
    - md
    - pdf
    - docx
    - csv

    企业级项目中，这一层还会继续扩展：
    - Excel
    - HTML
    - Word 表格
    - OCR 图片
    - 飞书 / Notion / Confluence 文档
    """

    def load(self, file_path: str) -> List[Document]:
        ext = os.path.splitext(file_path)[1].lower().replace(".", "")

        if ext in ["txt", "md"]:
            loader = TextLoader(file_path, encoding="utf-8")
        elif ext == "pdf":
            loader = PyPDFLoader(file_path)
        elif ext == "docx":
            loader = Docx2txtLoader(file_path)
        elif ext == "csv":
            loader = CSVLoader(file_path)
        else:
            raise ValueError(f"暂不支持的文件类型: {ext}")

        docs = loader.load()

        # 给每个 Document 补充基础元数据
        for doc in docs:
            doc.metadata["source"] = os.path.basename(file_path)
            doc.metadata["file_path"] = file_path
            doc.metadata["file_type"] = ext

        return docs
