from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey

from api.app.db.session import Base


class Department(Base):
    """
    部门表。

    用来支持前端选择部门，
    以及 Agent 根据部门过滤员工数据。
    """
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)


class Employee(Base):
    """
    员工核心信息表。

    这类数据属于结构化数据，适合存 MySQL：
    - 姓名
    - 部门
    - 岗位
    - 薪资
    - 入职时间
    - 绩效分数
    """
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_no = Column(String(50), unique=True, index=True, nullable=False)

    name = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    position = Column(String(100), nullable=True)

    salary = Column(Float, nullable=True)
    hire_date = Column(String(50), nullable=True)
    performance_score = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class PerformanceRecord(Base):
    """
    员工绩效记录表。

    绩效评分适合 MySQL 查询。
    绩效评语也可以同步进入向量数据库，方便 AI 语义分析。
    """
    __tablename__ = "performance_records"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    period = Column(String(50), nullable=False)
    score = Column(Float, nullable=True)
    comment = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class ChatMessage(Base):
    """
    聊天消息表。

    用来存完整聊天历史。
    注意：不要每次把所有历史都塞进 Prompt。
    正确做法是：只取最近 N 轮作为短期记忆。
    """
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True, nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserProfile(Base):
    """
    用户画像表。

    存储长期稳定信息，例如：
    - 用户常查询哪个部门
    - 用户关注绩效还是薪资
    - 用户偏好中文回答
    """
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    profile_text = Column(Text, default="")
    updated_at = Column(DateTime, default=datetime.utcnow)


class LongTermMemory(Base):
    """
    长期记忆表。

    存储重要历史事实。
    同时建议将 memory_text 向量化存入向量数据库。
    """
    __tablename__ = "long_term_memories"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True, nullable=False)
    memory_type = Column(String(50), default="general")
    memory_text = Column(Text, nullable=False)
    importance = Column(Float, default=0.5)
    created_at = Column(DateTime, default=datetime.utcnow)
