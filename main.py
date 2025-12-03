# main.py
import sys
from datetime import datetime
from tools.task_storage_tool import TaskStorageTool
from agents.intake_agent import IntakeAgent
from agents.priority_agent import PriorityAgent
from agents.scheduler_agent import SchedulerAgent
from agents.summary_agent import SummaryAgent

def add_flow(text):
    storage = TaskStorageTool()
    intake = IntakeAgent(storage)
    saved = intake.handle(text)
    print("Saved task:")
    print(saved)

def list_flow():
    storage = TaskStorageTool()
    tasks = storage.list_tasks()
    if not tasks:
        print("No tasks found.")
    for t in tasks:
        print(f"- {t.get('id','')[:8]} | {t.get('task')} | due:{t.get('due')} | dur:{t.get('duration')} | status:{t.get('status')}")

def schedule_flow(target_date: str = None):
    storage = TaskStorageTool()
    tasks = storage.list_tasks()
    pr = PriorityAgent()
    prioritized = pr.prioritize(tasks)
    sched = SchedulerAgent()
    dt = datetime.now()
    plan = sched.create_daily_schedule(dt, prioritized)
    print("Scheduled slots:")
    for s in plan["scheduled"]:
        print(f"- {s['start']} -> {s['end']} : {s['title']} (score={s.get('score'):.3f})")
    if plan["unscheduled"]:
        print("\nUnscheduled:")
        for u in plan["unscheduled"]:
            print(f"- {u.get('task')}")
    return plan

def summary_flow():
    storage = TaskStorageTool()
    tasks = storage.list_tasks()
    summary_agent = SummaryAgent()
    s = summary_agent.end_of_day_summary(tasks)
    print(s["text"])
    return s

def demo_flow():
    print("Running demo: add two tasks, schedule and summary.")
    add_flow("Finish ML assignment tomorrow 3 hours")
    add_flow("Buy groceries today 30 min")
    print("\nLIST:")
    list_flow()
    print("\nSCHEDULE:")
    schedule_flow()
    print("\nSUMMARY:")
    summary_flow()

def print_help():
    print("Usage:")
    print(" python main.py demo")
    print(" python main.py add \"task text\"")
    print(" python main.py list")
    print(" python main.py schedule [iso-date]")
    print(" python main.py summary")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "add":
        if len(sys.argv) < 3:
            print("Please provide task text in quotes.")
        else:
            add_flow(sys.argv[2])
    elif cmd == "list":
        list_flow()
    elif cmd == "schedule":
        d = sys.argv[2] if len(sys.argv) >= 3 else None
        schedule_flow(d)
    elif cmd == "summary":
        summary_flow()
    elif cmd == "demo":
        demo_flow()
    else:
        print_help()
