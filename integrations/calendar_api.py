from typing import Dict, List
from datetime import datetime, timedelta

class CalendarAPI:
    def __init__(self, api_key: str = None, client_id: str = None, client_secret: str = None):
        self.calendars = {}  # Simulate in-memory storage for calendars
        self.api_key = api_key
        self.client_id = client_id
        self.client_secret = client_secret
        self.service = None
        
        # Initialize real calendar service if credentials are provided
        if api_key or (client_id and client_secret):
            self._initialize_service()
    
    def _initialize_service(self):
        """
        Initialize connection to a real calendar service.
        This is a placeholder - implementation would depend on the specific service.
        """
        # Example for Google Calendar:
        # from googleapiclient.discovery import build
        # from google.oauth2.credentials import Credentials
        # 
        # credentials = Credentials(self.api_key)
        # self.service = build('calendar', 'v3', credentials=credentials)
        pass
        
    async def get_calendar(self, user_email: str) -> List[Dict]:
        """
        Fetch the calendar events for a specific user.
        """
        # Return the user's calendar; create an empty calendar if it doesn't exist
        if user_email not in self.calendars:
            self.calendars[user_email] = []
        return self.calendars[user_email]

    async def create_event(self, event_data: Dict) -> Dict:
        """
        Create a new event in the calendar.
        """
        participants = event_data.get("participants", [])
        
        # Generate a unique event ID based on total events across all calendars
        total_events = sum(len(calendar) for calendar in self.calendars.values())
        event_id = f"event_{total_events + 1}"
        event_data["id"] = event_id

        # Add the event to each participant's calendar
        for participant in participants:
            if participant not in self.calendars:
                self.calendars[participant] = []
            self.calendars[participant].append({
                "id": event_id,
                "title": event_data["title"],
                "description": event_data.get("description", ""),  # Handle missing description
                "start": event_data["start_time"],
                "end": event_data["end_time"]
            })
        return event_data

    async def send_invitation(self, participant_email: str, event_data: Dict):
        """
        Simulate sending a meeting invitation to a participant.
        """
        # Simulate sending an invitation (print/log for demonstration purposes)
        print(f"Invitation sent to {participant_email} for event '{event_data['title']}' on {event_data['start_time']}.")

    async def delete_event(self, user_email: str, event_id: str) -> bool:
        """
        Delete an event from a user's calendar.
        """
        if user_email not in self.calendars:
            return False

        user_calendar = self.calendars[user_email]
        for event in user_calendar:
            if event["id"] == event_id:
                user_calendar.remove(event)
                return True
        return False

    async def get_available_time_slots(
        self, user_email: str, start_time: datetime, end_time: datetime, duration: int
    ) -> List[datetime]:
        """
        Find available time slots for a user between start_time and end_time.
        """
        if user_email not in self.calendars:
            self.calendars[user_email] = []

        # Get the user's calendar and sort by start time
        user_calendar = sorted(self.calendars[user_email], key=lambda x: x.get("start") or x.get("start_time"))
        available_slots = []
        current_time = start_time

        while current_time + timedelta(minutes=duration) <= end_time:
            # Check if current_time overlaps with any existing event
            overlap = False
            for event in user_calendar:
                event_start = datetime.fromisoformat(event["start"])
                event_end = datetime.fromisoformat(event["end"])
                if current_time < event_end and current_time + timedelta(minutes=duration) > event_start:
                    overlap = True
                    current_time = event_end  # Move to the end of the overlapping event
                    break
            
            if not overlap:
                available_slots.append(current_time)
                current_time += timedelta(minutes=duration)
            else:
                current_time += timedelta(minutes=15)  # Increment to avoid infinite loops

        return available_slots


#class CalendarAPI:
#     def __init__(self):
#         self.calendars = {}  # Simulate in-memory storage for calendars

#     async def get_calendar(self, user_email: str) -> List[Dict]:
#         """
#         Fetch the calendar events for a specific user.
#         """
#         # Return the user's calendar; create an empty calendar if it doesn't exist
#         if user_email not in self.calendars:
#             self.calendars[user_email] = []
#         return self.calendars[user_email]

#     async def create_event(self, event_data: Dict) -> Dict:
#         """
#         Create a new event in the calendar.
#         """
#         participants = event_data.get("participants", [])
#         event_id = f"event_{len(self.calendars) + 1}"
#         event_data["id"] = event_id

#         # Add the event to each participant's calendar
#         for participant in participants:
#             if participant not in self.calendars:
#                 self.calendars[participant] = []
#             self.calendars[participant].append({
#                 "id": event_id,
#                 "title": event_data["title"],
#                 "description": event_data["description"],
#                 "start": event_data["start_time"],
#                 "end": event_data["end_time"]
#             })
#         return event_data

#     async def send_invitation(self, participant_email: str, event_data: Dict):
#         """
#         Simulate sending a meeting invitation to a participant.
#         """
#         # Simulate sending an invitation (print/log for demonstration purposes)
#         print(f"Invitation sent to {participant_email} for event '{event_data['title']}' on {event_data['start_time']}.")

#     async def delete_event(self, user_email: str, event_id: str) -> bool:
#         """
#         Delete an event from a user's calendar.
#         """
#         if user_email not in self.calendars:
#             return False

#         user_calendar = self.calendars[user_email]
#         for event in user_calendar:
#             if event["id"] == event_id:
#                 user_calendar.remove(event)
#                 return True
#         return False

#     async def get_available_time_slots(
#         self, user_email: str, start_time: datetime, end_time: datetime, duration: int
#     ) -> List[datetime]:
#         """
#         Find available time slots for a user between start_time and end_time.
#         """
#         if user_email not in self.calendars:
#             self.calendars[user_email] = []

#         # Get the user's calendar and sort by start time
#         user_calendar = sorted(self.calendars[user_email], key=lambda x: x["start"])
#         available_slots = []
#         current_time = start_time

#         while current_time + timedelta(minutes=duration) <= end_time:
#             # Check if current_time overlaps with any existing event
#             overlap = False
#             for event in user_calendar:
#                 event_start = datetime.fromisoformat(event["start"])
#                 event_end = datetime.fromisoformat(event["end"])
#                 if current_time < event_end and current_time + timedelta(minutes=duration) > event_start:
#                     overlap = True
#                     current_time = event_end  # Move to the end of the overlapping event
#                     break
            
#             if not overlap:
#                 available_slots.append(current_time)
#                 current_time += timedelta(minutes=duration)
#             else:
#                 current_time += timedelta(minutes=15)  # Increment to avoid infinite loops

#         return available_slots