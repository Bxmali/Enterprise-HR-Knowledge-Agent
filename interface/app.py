import requests
import streamlit as st


API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="企业级 HR 智能体系统",
    layout="wide",
)

st.title("企业级 HR 智能体系统")
st.caption("FastAPI + Streamlit + LangChain + DeepSeek + MySQL + Chroma/Qdrant")


with st.sidebar:
    st.header("会话配置")

    session_id = st.text_input("Session ID", value="user01")

    st.divider()

    st.header("文档上传")

    uploaded_file = st.file_uploader(
        "上传员工资料 / 简历 / 绩效文档 / 公司制度",
        type=["txt", "md", "pdf", "docx", "csv"],
    )

    employee_id = st.number_input("员工ID，可选", min_value=0, value=0)
    department_id = st.number_input("部门ID，可选", min_value=0, value=0)

    if st.button("上传并构建知识库"):
        if uploaded_file is None:
            st.warning("请先选择文件")
        else:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type,
                )
            }

            data = {
                "employee_id": employee_id if employee_id > 0 else None,
                "department_id": department_id if department_id > 0 else None,
            }

            resp = requests.post(
                f"{API_BASE}/knowledge/upload",
                files=files,
                data=data,
                timeout=120,
            )

            if resp.status_code == 200:
                st.success("知识库创建成功")
                st.json(resp.json())
            else:
                st.error(resp.text)


st.header("HR 智能问答")

question = st.text_area(
    "请输入你的问题",
    placeholder="例如：张三的绩效表现怎么样？研发部绩效最高的是谁？员工手册里病假制度是什么？",
)

col1, col2 = st.columns(2)
with col1:
    selected_employee_id = st.number_input("限定员工ID，可选", min_value=0, value=0, key="query_emp")
with col2:
    selected_department_id = st.number_input("限定部门ID，可选", min_value=0, value=0, key="query_dept")

if st.button("发送问题"):
    if not question.strip():
        st.warning("请输入问题")
    else:
        payload = {
            "question": question,
            "session_id": session_id,
            "employee_id": selected_employee_id if selected_employee_id > 0 else None,
            "department_id": selected_department_id if selected_department_id > 0 else None,
        }

        resp = requests.post(
            f"{API_BASE}/chat/",
            json=payload,
            timeout=120,
        )

        if resp.status_code == 200:
            st.subheader("AI 回答")
            st.write(resp.json()["answer"])
        else:
            st.error(resp.text)


st.divider()

st.header("员工管理测试")

with st.expander("新增员工"):
    employee_no = st.text_input("员工编号", value="E001")
    name = st.text_input("姓名", value="张三")
    position = st.text_input("岗位", value="AI工程师")
    salary = st.number_input("薪资", min_value=0.0, value=15000.0)
    performance_score = st.number_input("绩效评分", min_value=0.0, max_value=100.0, value=90.0)

    if st.button("创建员工"):
        payload = {
            "employee_no": employee_no,
            "name": name,
            "position": position,
            "salary": salary,
            "performance_score": performance_score,
        }

        resp = requests.post(f"{API_BASE}/employees/", json=payload)

        if resp.status_code == 200:
            st.success("员工创建成功")
            st.json(resp.json())
        else:
            st.error(resp.text)
