# ui/pages/_1_Dashboard.py
import streamlit as st
from tools.task_storage_tool import TaskStorageTool

def app():
    st.title("Daily Study Plan Agent")
    st.markdown("AI-powered task management and study planning system")
    storage = TaskStorageTool()
    tasks = storage.list_tasks()
    st.subheader("Quick stats")
    total = len(tasks)
    todo = sum(1 for t in tasks if t.get("status") != "done")
    done = total - todo
    col1, col2, col3 = st.columns(3)
    col1.metric("Total tasks", total)
    col2.metric("Pending", todo)
    col3.metric("Completed", done)
    st.write("---")
    st.subheader("Upcoming")
    for t in tasks[:6]:
        st.write(f"- **{t.get('task')}** — due: {t.get('due') or 'N/A'} — {t.get('duration') or '30'} min")
