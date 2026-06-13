from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.app.db.session import get_db
from api.app.schemas.hr import ChatRequest, ChatResponse
from api.app.services.agent.hr_agent import HRAgentService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    """
    HR Agent 问答接口。

    用户问题会同时结合：
    - MySQL 员工结构化数据
    - RAG 向量知识库
    - 短期聊天记忆
    - 用户画像
    """
    agent = HRAgentService()

    answer = agent.ask(
        db=db,
        question=payload.question,
        session_id=payload.session_id,
        employee_id=payload.employee_id,
        department_id=payload.department_id,
    )

    return ChatResponse(answer=answer)
