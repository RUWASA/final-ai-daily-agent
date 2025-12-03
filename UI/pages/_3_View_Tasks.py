# ui/pages/_3_View_Tasks.py
import streamlit as st
from tools.task_storage_tool import TaskStorageTool

def app():
    st.title("View Tasks")
    storage = TaskStorageTool()
    tasks = storage.list_tasks()
    if not tasks:
        st.info("No tasks found.")
        return
    for t in tasks:
        with st.expander(f"{t.get('task')}  —  {t.get('due') or 'no due'}"):
            st.write(f"ID: {t.get('id')}")
            st.write(f"Duration: {t.get('duration')}")
            st.write(f"Urgency: {t.get('urgency')}")
            st.write(f"Status: {t.get('status')}")
            col1, col2, col3 = st.columns(3)
            if col1.button("Mark Done", key=f"done_{t.get('id')}"):
                storage.update_task(t.get("id"), {"status": "done"})
                st.experimental_rerun()
            if col2.button("Delete", key=f"del_{t.get('id')}"):
                storage.delete_task(t.get("id"))
                st.experimental_rerun()
            if col3.button("Reschedule (set tomorrow)", key=f"res_{t.get('id')}"):
                storage.update_task(t.get("id"), {"due": "tomorrow"})
                st.experimental_rerun()
