import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form

from api.app.core.config import settings
from api.app.services.rag.knowledge_base import KnowledgeBaseService

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.post("/upload")
async def upload_knowledge_file(
    file: UploadFile = File(...),
    employee_id: int | None = Form(default=None),
    department_id: int | None = Form(default=None),
):
    """
    上传知识文件并写入向量数据库。

    支持员工资料、简历、绩效评语、制度文档等。

    employee_id:
    - 如果文件属于某个员工，填写员工ID

    department_id:
    - 如果文件属于某个部门，填写部门ID
    """
    os.makedirs(settings.upload_dir, exist_ok=True)

    save_path = os.path.join(settings.upload_dir, file.filename)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    kb = KnowledgeBaseService()
    result = kb.create_knowledge(
        file_path=save_path,
        employee_id=employee_id,
        department_id=department_id,
    )

    return result
