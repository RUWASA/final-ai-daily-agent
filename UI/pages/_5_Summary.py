# ui/pages/_5_Summary.py
import streamlit as st
from tools.task_storage_tool import TaskStorageTool
from agents.summary_agent import SummaryAgent

def app():
    st.title("Summary")
    storage = TaskStorageTool()
    tasks = storage.list_tasks()
    summ = SummaryAgent().end_of_day_summary(tasks)
    st.write(summ["text"])
    st.write("### Completed")
    for c in summ["completed"]:
        st.write(f"- {c.get('task')}")
    st.write("### Pending")
    for p in summ["pending"]:
        st.write(f"- {p.get('task')}")

