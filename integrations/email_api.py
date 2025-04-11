from typing import Dict, List

class EmailAPI:
    def __init__(self, api_key: str = None, api_url: str = None):
        self.inbox = []  # Simulate an inbox
        self.sent_emails = []  # Simulate a sent folder
        self.api_key = api_key  # Store API key for real service
        self.api_url = api_url or "https://api.email-service.example.com"
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if api_key else {}
        
    async def get_inbox(self, filters: Dict = None) -> List[Dict]:
        """
        Fetch emails from the inbox
        """
        if not filters:
            return self.inbox

        filtered_emails = []
        for email in self.inbox:
            match = all(email.get(key) == value for key, value in filters.items())
            if match:
                filtered_emails.append(email)
        return filtered_emails

    async def send_email(self, email_data: Dict) -> Dict:
        """
        Send an email
        """
        email_id = f"email_{len(self.sent_emails) + 1}"
        email_data["id"] = email_id
        self.sent_emails.append(email_data)
        return email_data

    async def delete_email(self, email_id: str) -> bool:
        """
        Delete an email from the inbox
        """
        for email in self.inbox:
            if email.get("id") == email_id:
                self.inbox.remove(email)
                return True
        return False

    async def categorize_email(self, email_id: str, category: str) -> bool:
        """
        Categorize an email
        """
        for email in self.inbox:
            if email.get("id") == email_id:
                email["category"] = category
                return True
        return False

# from typing import Dict, List

# class EmailAPI:
#     def __init__(self):
#         self.inbox = []  # Simulate an inbox
#         self.sent_emails = []  # Simulate a sent folder

#     async def get_inbox(self, filters: Dict = None) -> List[Dict]:
#         """
#         Fetch emails from the inbox
#         """
#         if not filters:
#             return self.inbox

#         filtered_emails = []
#         for email in self.inbox:
#             match = all(email.get(key) == value for key, value in filters.items())
#             if match:
#                 filtered_emails.append(email)
#         return filtered_emails

#     async def send_email(self, email_data: Dict) -> Dict:
#         """
#         Send an email
#         """
#         email_id = f"email_{len(self.sent_emails) + 1}"
#         email_data["id"] = email_id
#         self.sent_emails.append(email_data)
#         return email_data

#     async def delete_email(self, email_id: str) -> bool:
#         """
#         Delete an email from the inbox
#         """
#         for email in self.inbox:
#             if email.get("id") == email_id:
#                 self.inbox.remove(email)
#                 return True
#         return False

#     async def categorize_email(self, email_id: str, category: str) -> bool:
#         """
#         Categorize an email
#         """
#         for email in self.inbox:
#             if email.get("id") == email_id:
#                 email["category"] = category
#                 return True
#         return False