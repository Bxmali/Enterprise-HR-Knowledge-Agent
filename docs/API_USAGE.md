# API 使用说明

## 上传知识文件

POST /knowledge/upload

form-data:

- file: 文件
- employee_id: 可选
- department_id: 可选

## AI 问答

POST /chat/

```json
{
  "question": "张三的绩效怎么样？",
  "session_id": "user01",
  "employee_id": 1,
  "department_id": null
}
```

## 创建员工

POST /employees/

```json
{
  "employee_no": "E001",
  "name": "张三",
  "position": "AI工程师",
  "salary": 15000,
  "performance_score": 90
}
```
