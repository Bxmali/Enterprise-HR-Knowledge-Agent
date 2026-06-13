from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """
    项目全局配置类。

    所有重要 API Key、数据库地址、向量库配置都从 .env 中读取。
    面试时可以说明：
    - 不把密钥写死在代码里
    - 通过环境变量区分开发、测试、生产环境
    """

    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"

    dashscope_api_key: str = ""
    embedding_model: str = "text-embedding-v4"

    mysql_url: str = "mysql+pymysql://root:password@localhost:3306/hr_agent?charset=utf8mb4"

    vector_backend: str = "chroma"

    chroma_persist_dir: str = "./data/chroma_db"
    chroma_collection: str = "hr_rag"

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "hr_rag"

    upload_dir: str = "./data/uploads"

    recent_history_limit: int = 10
    long_memory_top_k: int = 3

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
