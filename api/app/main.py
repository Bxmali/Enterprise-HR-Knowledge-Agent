from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.app.routes import employees, knowledge, chat


app = FastAPI(
    title="企业级 HR 智能体系统",
    description="FastAPI + Streamlit + LangChain + DeepSeek + MySQL + Chroma/Qdrant",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router)
app.include_router(knowledge.router)
app.include_router(chat.router)


@app.get("/")
def root():
    return {
        "message": "HR Agent RAG API is running",
        "docs": "/docs",
    }
