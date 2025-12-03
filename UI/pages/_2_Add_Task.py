# ui/pages/_2_Add_Task.py
import streamlit as st
from tools.task_storage_tool import TaskStorageTool

def app():
    st.title("Add Task")
    st.write("Enter your task in natural language or fill the fields below.")
    text = st.text_input("Task description (e.g., Finish assignment tomorrow 3 hours)")
    with st.form("task_form"):
        title = st.text_input("Title")
        duration = st.number_input("Duration (minutes)", min_value=5, value=30)
        due = st.text_input("Due (e.g., today, tomorrow, 2025-12-01)")
        urgency = st.selectbox("Urgency", ["medium", "high", "low"])
        tags = st.text_input("Tags (comma-separated)")
        submitted = st.form_submit_button("Add Task")
    storage = TaskStorageTool()
    if submitted:
        task_obj = {
            "task": title or text or "Untitled task",
            "duration": int(duration),
            "due": due or None,
            "urgency": urgency,
            "tags": [t.strip() for t in (tags.split(",") if tags else [])]
        }
        saved = storage.add_task(task_obj)
        st.success("Task saved")
        st.json(saved)
