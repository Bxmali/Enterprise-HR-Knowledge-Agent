from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from api.app.core.config import settings
from api.app.services.rag.retriever import RetrieverService
from api.app.services.memory.memory_service import MemoryService
from api.app.services.agent.hr_tools import HRTools


class HRAgentService:
    """
    HR 智能体核心服务。

    当前版本采用“规则路由 + RAG + MySQL 查询”的方式，
    比完全让 LLM 自己判断更稳定。

    后续可以升级成 LangGraph Tool Calling：
    - MySQL Tool
    - Retriever Tool
    - Memory Tool
    """

    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.deepseek_model,
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
            temperature=0.3,
        )

        self.retriever = RetrieverService()
        self.memory = MemoryService()
        self.hr_tools = HRTools()

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
你是一个企业 HR 智能体助手。

你可以根据以下信息回答用户问题：

【用户画像】
{profile}

【短期聊天历史】
{history}

【MySQL结构化数据查询结果】
{sql_context}

【RAG知识库上下文】
{rag_context}

回答规则：
1. 如果问题涉及员工薪资、部门、绩效评分，优先参考 MySQL 结构化数据。
2. 如果问题涉及简历、绩效评语、培训记录、员工手册，优先参考 RAG 知识库。
3. 如果信息不足，请直接说当前数据不足，不要编造。
4. 回答要清晰、专业、适合 HR 场景。
5. 涉及敏感薪资信息时，提醒需要权限控制。
"""
                ),
                ("human", "{question}"),
            ]
        )

        self.chain = self.prompt | self.llm | StrOutputParser()

    def _simple_sql_router(self, db: Session, question: str) -> str:
        """
        简单规则路由。

        用关键词判断是否需要查询 MySQL。
        企业级可以替换为 Tool Calling 或 LangGraph Router。
        """
        if "绩效最高" in question or "表现最好" in question:
            return self.hr_tools.get_top_performers(db)

        # 这里只是示例：真实项目可做员工姓名识别
        return ""

    def ask(
        self,
        db: Session,
        question: str,
        session_id: str,
        employee_id: int | None = None,
        department_id: int | None = None,
    ) -> str:
        # 1. 保存用户消息
        self.memory.save_message(db, session_id, "user", question)

        # 2. 获取短期记忆和用户画像
        history = self.memory.get_recent_history(db, session_id)
        profile = self.memory.get_user_profile(db, session_id)

        # 3. 查询结构化数据
        sql_context = self._simple_sql_router(db, question)

        # 4. 查询向量知识库
        rag_context = self.retriever.retrieve(
            query=question,
            employee_id=employee_id,
            department_id=department_id,
            k=5,
        )

        # 5. 调用 DeepSeek 生成回答
        answer = self.chain.invoke(
            {
                "profile": profile or "暂无用户画像。",
                "history": history or "暂无历史对话。",
                "sql_context": sql_context or "无结构化查询结果。",
                "rag_context": rag_context or "无知识库上下文。",
                "question": question,
            }
        )

        # 6. 保存 AI 回复
        self.memory.save_message(db, session_id, "assistant", answer)

        # 7. 判断是否写入长期记忆
        if self.memory.should_save_long_memory(question):
            self.memory.save_long_memory(
                db=db,
                session_id=session_id,
                memory_text=f"用户提到：{question}",
                memory_type="user_intent",
                importance=0.7,
            )

        return answer
