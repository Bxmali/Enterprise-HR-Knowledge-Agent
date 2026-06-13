from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from api.app.core.config import settings


"""
数据库连接模块。

MySQL 用来存储企业中的结构化数据：
- 员工信息
- 部门
- 薪资
- 绩效评分
- 聊天历史
- 用户画像
- 长期记忆

注意：
向量数据库不适合存薪资、部门这类强结构化数据。
这些数据应该放在 MySQL 里，便于精确查询、排序、统计。
"""

engine = create_engine(
    settings.mysql_url,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    """
    FastAPI 依赖注入函数。

    每个请求创建一个数据库 Session，
    请求结束后自动关闭。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
