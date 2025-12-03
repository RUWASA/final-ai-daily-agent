# ui/pages/_4_Schedule.py
import streamlit as st
from datetime import datetime
from tools.task_storage_tool import TaskStorageTool
from agents.priority_agent import PriorityAgent
from agents.scheduler_agent import SchedulerAgent

def app():
    st.title("Daily Schedule")
    storage = TaskStorageTool()
    tasks = storage.list_tasks()
    # date selector
    target_date = st.date_input("Select Date", value=datetime.today().date())
    # Prioritize
    pr = PriorityAgent()
    ordered = pr.prioritize(tasks)
    sched = SchedulerAgent()
    plan = sched.create_daily_schedule(datetime.combine(target_date, datetime.min.time()), ordered)
    st.subheader(f"Schedule for {target_date.strftime('%B %d, %Y')}")
    st.write(f"{len(plan['scheduled'])} items scheduled")
    for s in plan["scheduled"]:
        start = s["start"][11:16] if "T" in s["start"] else s["start"]
        end = s["end"][11:16] if "T" in s["end"] else s["end"]
        st.write(f"{start} - {end} | {s['title']} ")
    if plan["unscheduled"]:
        st.write("### Unscheduled")
        for u in plan["unscheduled"]:
            st.write(f"- {u.get('task')}")
