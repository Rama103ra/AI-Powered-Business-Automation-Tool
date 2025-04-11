from typing import Dict, List
import spacy
from transformers import pipeline
from integrations.email_api import EmailAPI

class EmailProcessor:
    def __init__(self):
        # Initialize NLP components
        self.nlp = spacy.load("en_core_web_sm")
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.email_api = EmailAPI()

    async def process(self, email_data: Dict) -> Dict:
        """
        Process incoming emails using NLP for categorization and automated responses
        """
        # Extract email content
        content = email_data.get("content", "")
        sender = email_data.get("sender", "")
        subject = email_data.get("subject", "")

        # Analyze email
        category = self._categorize_email(content)
        priority = self._determine_priority(content, sender)
        response = self._generate_response(content, category)

        return {
            "category": category,
            "priority": priority,
            "suggested_response": response,
            "automated_actions": self._determine_actions(category, priority)
        }

    def _categorize_email(self, content: str) -> str:
        """
        Categorize email using NLP
        """
        doc = self.nlp(content)
        # Implement email categorization logic
        categories = {
            "meeting": ["meet", "schedule", "appointment"],
            "task": ["task", "todo", "deadline"],
            "inquiry": ["question", "help", "support"],
        }
        
        text_lower = content.lower()
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        return "other"

    def _determine_priority(self, content: str, sender: str) -> int:
        """
        Determine email priority (1-5)
        """
        priority = 3  # Default priority
        
        # Check for urgent keywords
        urgent_keywords = ["urgent", "asap", "emergency", "deadline"]
        if any(keyword in content.lower() for keyword in urgent_keywords):
            priority += 1

        # Add sender importance check
        vip_senders = ["boss@company.com", "client@important.com"]  # Example
        if sender in vip_senders:
            priority += 1

        return min(max(priority, 1), 5)  # Ensure priority is between 1-5

    def _generate_response(self, content: str, category: str) -> str:
        """
        Generate automated response based on email content and category
        """
        templates = {
            "meeting": "Thank you for your meeting request. I'll check the calendar and get back to you shortly.",
            "task": "I've received your task request and will process it right away.",
            "inquiry": "Thank you for your inquiry. I'm looking into this and will respond soon.",
            "other": "Thank you for your email. I'll review and respond shortly."
        }
        return templates.get(category, templates["other"])

    def _determine_actions(self, category: str, priority: int) -> List[str]:
        """
        Determine automated actions based on email category and priority
        """
        actions = []
        if category == "meeting":
            actions.append("schedule_calendar_check")
        if priority >= 4:
            actions.append("send_urgent_notification")
        if category == "task":
            actions.append("create_task_entry")
        return actions