from pydantic import BaseModel
from typing import Optional


class EmployeeCreate(BaseModel):
    employee_no: str
    name: str
    department_id: Optional[int] = None
    position: Optional[str] = None
    salary: Optional[float] = None
    hire_date: Optional[str] = None
    performance_score: Optional[float] = None


class EmployeeOut(BaseModel):
    id: int
    employee_no: str
    name: str
    department_id: Optional[int]
    position: Optional[str]
    salary: Optional[float]
    hire_date: Optional[str]
    performance_score: Optional[float]

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    question: str
    session_id: str = "default"
    employee_id: Optional[int] = None
    department_id: Optional[int] = None


class ChatResponse(BaseModel):
    answer: str
