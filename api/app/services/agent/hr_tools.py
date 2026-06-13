from sqlalchemy.orm import Session

from api.app.models.hr import Employee, Department, PerformanceRecord


class HRTools:
    """
    HR Agent 工具类。

    Agent 可以调用这些工具查询 MySQL 中的结构化数据。
    """

    def get_employee_by_name(self, db: Session, name: str) -> str:
        emp = db.query(Employee).filter(Employee.name == name).first()

        if not emp:
            return f"没有找到姓名为 {name} 的员工。"

        return (
            f"员工ID: {emp.id}\n"
            f"员工编号: {emp.employee_no}\n"
            f"姓名: {emp.name}\n"
            f"岗位: {emp.position}\n"
            f"薪资: {emp.salary}\n"
            f"入职时间: {emp.hire_date}\n"
            f"绩效评分: {emp.performance_score}\n"
        )

    def list_department_employees(self, db: Session, department_id: int) -> str:
        employees = db.query(Employee).filter(Employee.department_id == department_id).all()

        if not employees:
            return "该部门暂无员工。"

        return "\n".join(
            [
                f"{emp.id}. {emp.name} - {emp.position} - 绩效: {emp.performance_score}"
                for emp in employees
            ]
        )

    def get_top_performers(self, db: Session, limit: int = 5) -> str:
        employees = (
            db.query(Employee)
            .order_by(Employee.performance_score.desc())
            .limit(limit)
            .all()
        )

        if not employees:
            return "暂无员工绩效数据。"

        return "\n".join(
            [
                f"{i+1}. {emp.name} - {emp.position} - 绩效: {emp.performance_score}"
                for i, emp in enumerate(employees)
            ]
        )
