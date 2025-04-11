from typing import Dict, List

class TaskAPI:
    def __init__(self, api_key: str = None, api_url: str = None):
        self.tasks = {}  # In-memory storage for tasks
        self.reminders = {}  # In-memory storage for reminders
        self.api_key = api_key
        self.api_url = api_url or "https://api.task-service.example.com"
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if api_key else {}
        
        # Flag to determine if we're using simulation or real API
        self.use_real_api = bool(api_key)

    async def create_task(self, task_data: Dict) -> Dict:
        """
        Create a new task
        """
        task_id = f"task_{len(self.tasks) + 1}"
        task_data["id"] = task_id
        self.tasks[task_id] = task_data
        return self.tasks[task_id]

    async def get_tasks(self, filters: Dict = None) -> List[Dict]:
        """
        Get tasks based on optional filters
        """
        if not filters:
            return list(self.tasks.values())

        filtered_tasks = []
        for task in self.tasks.values():
            match = all(task.get(key) == value for key, value in filters.items())
            if match:
                filtered_tasks.append(task)
        return filtered_tasks

    async def update_task(self, task_id: str, updates: Dict) -> Dict:
        """
        Update an existing task
        """
        if task_id in self.tasks:
            self.tasks[task_id].update(updates)
            return self.tasks[task_id]
        raise ValueError("Task not found")

    async def delete_task(self, task_id: str) -> bool:
        """
        Delete a task
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    async def create_reminder(self, task_id: str, reminder: Dict):
        """
        Create a reminder for a task
        """
        if task_id not in self.reminders:
            self.reminders[task_id] = []
        self.reminders[task_id].append(reminder)

# from typing import Dict, List

# class TaskAPI:
#     def __init__(self):
#         self.tasks = {}  # In-memory storage for tasks
#         self.reminders = {}  # In-memory storage for reminders

#     async def create_task(self, task_data: Dict) -> Dict:
#         """
#         Create a new task
#         """
#         task_id = f"task_{len(self.tasks) + 1}"
#         task_data["id"] = task_id
#         self.tasks[task_id] = task_data
#         return self.tasks[task_id]

#     async def get_tasks(self, filters: Dict = None) -> List[Dict]:
#         """
#         Get tasks based on optional filters
#         """
#         if not filters:
#             return list(self.tasks.values())

#         filtered_tasks = []
#         for task in self.tasks.values():
#             match = all(task.get(key) == value for key, value in filters.items())
#             if match:
#                 filtered_tasks.append(task)
#         return filtered_tasks

#     async def update_task(self, task_id: str, updates: Dict) -> Dict:
#         """
#         Update an existing task
#         """
#         if task_id in self.tasks:
#             self.tasks[task_id].update(updates)
#             return self.tasks[task_id]
#         raise ValueError("Task not found")

#     async def delete_task(self, task_id: str) -> bool:
#         """
#         Delete a task
#         """
#         if task_id in self.tasks:
#             del self.tasks[task_id]
#             return True
#         return False

#     async def create_reminder(self, task_id: str, reminder: Dict):
#         """
#         Create a reminder for a task
#         """
#         if task_id not in self.reminders:
#             self.reminders[task_id] = []
#         self.reminders[task_id].append(reminder)