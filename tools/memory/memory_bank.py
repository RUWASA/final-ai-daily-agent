# memory/memory_bank.py
import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DATA_FILE = os.path.join(DATA_DIR, "tasks.json")

def _ensure_datafile():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

class MemoryBank:
    def __init__(self, path: Optional[str] = None):
        self.path = path or DATA_FILE
        _ensure_datafile()

    def _read(self) -> List[Dict]:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, items: List[Dict]):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, default=str)

    def save_task(self, task: Dict) -> Dict:
        items = self._read()
        if not task.get("id"):
            task["id"] = str(uuid.uuid4())
        task.setdefault("created_at", datetime.utcnow().isoformat())
        task.setdefault("status", "todo")
        items.append(task)
        self._write(items)
        return task

    def get_tasks(self, filters: Dict = None) -> List[Dict]:
        items = self._read()
        if not filters:
            return items
        out = items
        if "status" in filters:
            out = [t for t in out if t.get("status") == filters["status"]]
        if "tag" in filters:
            out = [t for t in out if filters["tag"] in (t.get("tags") or [])]
        return out

    def update_task(self, task_id: str, updates: Dict) -> Optional[Dict]:
        items = self._read()
        changed = False
        for t in items:
            if t.get("id") == task_id:
                t.update(updates)
                changed = True
                break
        if changed:
            self._write(items)
            return t
        return None

    def delete_task(self, task_id: str) -> bool:
        items = self._read()
        new = [t for t in items if t.get("id") != task_id]
        if len(new) == len(items):
            return False
        self._write(new)
        return True
