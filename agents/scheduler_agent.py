# scheduler_agent.py

# agents/scheduler_agent.py
from datetime import datetime, timedelta
from typing import List, Dict

class SchedulerAgent:
    """
    Greedy scheduler that fills a work window from start hour to end hour.
    """

    def __init__(self, work_start_hour: int = 9, work_end_hour: int = 18):
        self.work_start_hour = work_start_hour
        self.work_end_hour = work_end_hour

    def create_daily_schedule(self, date_obj: datetime, tasks: List[Dict]) -> Dict:
        # ensure date_obj is a datetime
        if not isinstance(date_obj, datetime):
            date_obj = datetime.now()

        cursor = date_obj.replace(hour=self.work_start_hour, minute=0, second=0, microsecond=0)
        end_dt = date_obj.replace(hour=self.work_end_hour, minute=0, second=0, microsecond=0)
        scheduled = []
        unscheduled = []

        for t in tasks:
            dur = int(t.get("duration") or 30)
            slot_end = cursor + timedelta(minutes=dur)
            if slot_end <= end_dt:
                scheduled.append({
                    "task_id": t.get("id"),
                    "title": t.get("task"),
                    "start": cursor.isoformat(),
                    "end": slot_end.isoformat(),
                    "score": t.get("_score")
                })
                # move cursor, add small buffer
                cursor = slot_end + timedelta(minutes=5)
            else:
                unscheduled.append(t)

        return {"scheduled": scheduled, "unscheduled": unscheduled}
