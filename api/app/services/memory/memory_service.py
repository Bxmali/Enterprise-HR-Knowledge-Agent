from typing import List
from sqlalchemy.orm import Session

from api.app.models.hr import ChatMessage, UserProfile, LongTermMemory
from api.app.core.config import settings


class MemoryService:
    """
    记忆系统。

    分三层：
    1. 短期记忆：最近 N 条聊天记录
    2. 长期记忆：重要信息，存 MySQL，也可以向量化
    3. 用户画像：稳定偏好和长期状态

    注意：
    不要把所有历史记录都塞进 Prompt，
    否则 token 会爆炸。
    """

    def save_message(self, db: Session, session_id: str, role: str, content: str) -> None:
        msg = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
        )
        db.add(msg)
        db.commit()

    def get_recent_history(self, db: Session, session_id: str) -> str:
        messages: List[ChatMessage] = (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.id.desc())
            .limit(settings.recent_history_limit)
            .all()
        )

        messages = list(reversed(messages))

        history_text = ""
        for msg in messages:
            history_text += f"{msg.role}: {msg.content}\n"

        return history_text.strip()

    def get_user_profile(self, db: Session, session_id: str) -> str:
        profile = (
            db.query(UserProfile)
            .filter(UserProfile.session_id == session_id)
            .first()
        )

        return profile.profile_text if profile else ""

    def save_long_memory(
        self,
        db: Session,
        session_id: str,
        memory_text: str,
        memory_type: str = "general",
        importance: float = 0.5,
    ) -> None:
        memory = LongTermMemory(
            session_id=session_id,
            memory_text=memory_text,
            memory_type=memory_type,
            importance=importance,
        )
        db.add(memory)
        db.commit()

    def should_save_long_memory(self, text: str) -> bool:
        """
        简单规则版长期记忆判断。

        企业级可以改成 LLM 判断：
        - 是否包含长期稳定信息
        - 是否需要更新用户画像
        - 是否值得向量化
        """
        keywords = [
            "以后",
            "记住",
            "我的项目",
            "我正在",
            "偏好",
            "目标",
            "已经完成",
            "下一步",
        ]
        return any(k in text for k in keywords)
