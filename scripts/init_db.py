from api.app.db.session import Base, engine
from api.app.models import hr  # noqa


def init_db():
    """
    初始化 MySQL 表结构。

    执行前请确保：
    1. MySQL 已启动
    2. 已创建数据库 hr_agent
    3. .env 中 MYSQL_URL 正确
    """
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成")


if __name__ == "__main__":
    init_db()
