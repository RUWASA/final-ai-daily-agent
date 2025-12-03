# tests/test_integration.py
import os
from datetime import datetime
from memory.memory_bank import MemoryBank
from tools.task_storage_tool import TaskStorageTool
from agents.intake_agent import IntakeAgent
from agents.priority_agent import PriorityAgent
from agents.scheduler_agent import SchedulerAgent
from agents.summary_agent import SummaryAgent

def test_full_flow(tmp_path):
    # point memory to tmp path
    db_path = tmp_path / "tasks.json"
    mb = MemoryBank(path=str(db_path))
    storage = TaskStorageTool(memory=mb)
    intake = IntakeAgent(storage)
    saved = intake.handle("Unit test task today 20 min")
    assert saved.get("id")
    tasks = storage.list_tasks()
    assert len(tasks) == 1
    pr = PriorityAgent()
    ordered = pr.prioritize(tasks)
    sched = SchedulerAgent()
    plan = sched.create_daily_schedule(datetime.now(), ordered)
    assert "scheduled" in plan
    summary = SummaryAgent().end_of_day_summary(tasks)
    assert "text" in summary
