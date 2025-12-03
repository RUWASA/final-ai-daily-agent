# summary_agent.py

# agents/summary_agent.py
from typing import List, Dict

class SummaryAgent:
    """
    Produces an end-of-day summary (text + programmatic JSON).
    """

    def end_of_day_summary(self, tasks: List[Dict]) -> Dict:
        completed = [t for t in tasks if t.get("status") == "done"]
        pending = [t for t in tasks if t.get("status") != "done"]
        suggestions = [p.get("task") for p in pending[:3]]
        text = (
            f"Today you completed {len(completed)} task(s). "
            f"{len(pending)} task(s) remain. Suggested focus for tomorrow: {', '.join(suggestions)}."
        )
        return {"completed": completed, "pending": pending, "suggestions": suggestions, "text": text}
