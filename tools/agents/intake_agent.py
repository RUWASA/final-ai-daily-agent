# agents/intake_agent.py
# agents/intake_agent.py
from typing import Dict
import re
from tools.task_storage_tool import TaskStorageTool

class IntakeAgent:
    """
    Minimal intake agent: converts a user's free-text into a normalized task dict.
    Replace _parse_with_llm with an actual LLM call for production quality.
    """

    def __init__(self, storage: TaskStorageTool = None):
        self.storage = storage or TaskStorageTool()

    def _parse_with_rules(self, text: str) -> Dict:
        txt = text.strip()
        task = {"task": txt, "duration": None, "due": None, "urgency": "medium", "tags": []}

        # duration: "2 hours", "30 min"
        m = re.search(r"(\d+)\s*(hour|hours|hr)\b", txt, flags=re.I)
        if m:
            task["duration"] = int(m.group(1)) * 60
        else:
            m2 = re.search(r"(\d+)\s*(minute|minutes|min)\b", txt, flags=re.I)
            if m2:
                task["duration"] = int(m2.group(1))

        # due hints
        if re.search(r"\btoday\b", txt, flags=re.I):
            task["due"] = "today"
            task["urgency"] = "high"
        elif re.search(r"\btomorrow\b", txt, flags=re.I):
            task["due"] = "tomorrow"

        # urgency keywords
        if re.search(r"\b(asap|urgent|immediately)\b", txt, flags=re.I):
            task["urgency"] = "high"

        # simple tag detection
        if re.search(r"\b(email|send|mail)\b", txt, flags=re.I):
            task["tags"].append("email")
        if re.search(r"\b(meeting|call)\b", txt, flags=re.I):
            task["tags"].append("meeting")

        return task

    def handle(self, user_text: str) -> Dict:
        parsed = self._parse_with_rules(user_text)
        saved = self.storage.add_task(parsed)
        return saved
