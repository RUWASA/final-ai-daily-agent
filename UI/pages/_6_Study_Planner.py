# ui/pages/_6_Study_Planner.py
import streamlit as st
from tools.task_storage_tool import TaskStorageTool

def app():
    st.title("Study Planner")
    st.write("Simple study session planner built on top of scheduled tasks.")
    storage = TaskStorageTool()
    tasks = storage.list_tasks()
    study_tasks = [t for t in tasks if "study" in (t.get("tags") or []) or "study" in t.get("task", "").lower()]
    if not study_tasks:
        st.info("No study tasks found. Add tasks with 'study' tag or word.")
        return
    for t in study_tasks:
        st.write(f"- {t.get('task')} ({t.get('duration')} min)")
