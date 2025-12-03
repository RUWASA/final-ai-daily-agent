# tools/task_storage_tool.py
from typing import Dict, List, Optional
from memory.memory_bank import MemoryBank

class TaskStorageTool:
    def __init__(self, memory: Optional[MemoryBank] = None):
        self.memory = memory or MemoryBank()

    def add_task(self, task: Dict) -> Dict:
        # normalize fields
        if "title" in task and "task" not in task:
            task["task"] = task.pop("title")
        if not task.get("task"):
            raise ValueError("Task must contain 'task' or 'title' field.")
        return self.memory.save_task(task)

    def list_tasks(self, filters: Dict = None) -> List[Dict]:
        return self.memory.get_tasks(filters)

    def update_task(self, task_id: str, updates: Dict) -> Dict:
        return self.memory.update_task(task_id, updates)

    def delete_task(self, task_id: str) -> bool:
        return self.memory.delete_task(task_id)
