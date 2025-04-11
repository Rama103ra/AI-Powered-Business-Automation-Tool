from typing import Dict, List
import datetime
from integrations.task_api import TaskAPI

class TaskManager:
    def __init__(self):
        self.task_api = TaskAPI()
        self.priority_levels = {
            "high": 3,
            "medium": 2,
            "low": 1
        }

    async def process_task(self, task_data: Dict) -> Dict:
        """
        Process and manage tasks
        """
        # Validate and enhance task data
        enhanced_task = self._enhance_task_data(task_data)
        
        # Determine priority and deadline
        priority = self._calculate_priority(enhanced_task)
        enhanced_task["priority"] = priority

        # Store task
        stored_task = await self.task_api.create_task(enhanced_task)

        # Set up automated reminders
        reminders = await self._setup_reminders(stored_task)

        return {
            "task_id": stored_task["id"],
            "status": "created",
            "priority": priority,
            "reminders": reminders
        }

    def _enhance_task_data(self, task_data: Dict) -> Dict:
        """
        Enhance task data with additional information and validations
        """
        enhanced_task = task_data.copy()

        # Add default deadline if not provided
        if "deadline" not in enhanced_task:
            enhanced_task["deadline"] = (
                datetime.datetime.now() + datetime.timedelta(days=7)
            ).isoformat()

        # Add default status if not provided
        enhanced_task["status"] = enhanced_task.get("status", "pending")

        # Add creation timestamp
        enhanced_task["created_at"] = datetime.datetime.now().isoformat()

        return enhanced_task

    def _calculate_priority(self, task_data: Dict) -> int:
        """
        Calculate task priority based on various factors
        """
        priority_score = 0

        # Consider deadline
        deadline = datetime.datetime.fromisoformat(task_data["deadline"])
        days_until_deadline = (deadline - datetime.datetime.now()).days

        if days_until_deadline <= 1:
            priority_score += 3
        elif days_until_deadline <= 3:
            priority_score += 2
        elif days_until_deadline <= 7:
            priority_score += 1

        # Consider explicit priority if provided
        if "priority" in task_data:
            priority_score += self.priority_levels.get(
                task_data["priority"].lower(),
                0
            )

        # Consider task complexity
        if "complexity" in task_data:
            complexity_score = {
                "high": 3,
                "medium": 2,
                "low": 1
            }.get(task_data["complexity"].lower(), 0)
            priority_score += complexity_score

        # Normalize priority score to 1-5 range
        return min(max(priority_score, 1), 5)

    async def _setup_reminders(self, task: Dict) -> List[Dict]:
        """
        Set up automated reminders for the task
        """
        deadline = datetime.datetime.fromisoformat(task["deadline"])
        reminders = []

        # Create reminders based on deadline and priority
        if task["priority"] >= 4:  # High priority
            reminders.extend([
                {"time": deadline - datetime.timedelta(days=1), "type": "24h_reminder"},
                {"time": deadline - datetime.timedelta(hours=4), "type": "4h_reminder"},
                {"time": deadline - datetime.timedelta(hours=1), "type": "1h_reminder"}
            ])
        elif task["priority"] >= 2:  # Medium priority
            reminders.extend([
                {"time": deadline - datetime.timedelta(days=2), "type": "48h_reminder"},
                {"time": deadline - datetime.timedelta(days=1), "type": "24h_reminder"}
            ])
        else:  # Low priority
            reminders.append(
                {"time": deadline - datetime.timedelta(days=1), "type": "24h_reminder"}
            )

        # Store reminders in the system
        for reminder in reminders:
            await self.task_api.create_reminder(task["id"], reminder)

        return reminders

    async def get_tasks(self, filters: Dict = None) -> List[Dict]:
        """
        Get tasks based on filters
        """
        return await self.task_api.get_tasks(filters)

    async def update_task(self, task_id: str, updates: Dict) -> Dict:
        """
        Update task details
        """
        return await self.task_api.update_task(task_id, updates)

    async def delete_task(self, task_id: str) -> bool:
        """
        Delete a task
        """
        return await self.task_api.delete_task(task_id)