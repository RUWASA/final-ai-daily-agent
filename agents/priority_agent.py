# priority_agent.py

# agents/priority_agent.py
from datetime import datetime
from typing import List, Dict

def _days_left(due):
    if not due:
        return 9999
    s = str(due).lower()
    if "today" in s:
        return 0
    if "tomorrow" in s:
        return 1
    try:
        dt = datetime.fromisoformat(due)
        delta = dt - datetime.utcnow()
        return max(0, delta.days)
    except Exception:
        return 9999

class PriorityAgent:
    """
    Scores tasks by urgency, importance, and duration penalty.
    """

    def score_task(self, task: Dict) -> float:
        days = _days_left(task.get("due"))
        urgency_score = 1.0 / (days + 0.5)
        importance_map = {"high": 1.0, "medium": 0.6, "low": 0.2}
        importance = importance_map.get(task.get("urgency"), 0.5)
        duration = int(task.get("duration") or 30)
        duration_penalty = min(duration / 120.0, 1.0)
        score = 0.6 * urgency_score + 0.4 * importance - 0.1 * duration_penalty
        return float(score)

    def prioritize(self, tasks: List[Dict]) -> List[Dict]:
        for t in tasks:
            t["_score"] = self.score_task(t)
        return sorted(tasks, key=lambda x: x["_score"], reverse=True)
