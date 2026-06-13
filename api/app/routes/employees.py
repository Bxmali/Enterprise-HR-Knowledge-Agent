from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.app.db.session import get_db
from api.app.models.hr import Employee
from api.app.schemas.hr import EmployeeCreate, EmployeeOut

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("/", response_model=EmployeeOut)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    """
    创建员工。

    结构化员工数据写入 MySQL。
    """
    emp = Employee(**payload.model_dump())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


@router.get("/", response_model=list[EmployeeOut])
def list_employees(db: Session = Depends(get_db)):
    """
    查询员工列表。

    前端可以用这个接口展示员工下拉框。
    """
    return db.query(Employee).order_by(Employee.id.desc()).all()
