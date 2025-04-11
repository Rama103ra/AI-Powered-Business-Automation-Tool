from datetime import datetime, timedelta
from typing import Dict, List
from integrations.calendar_api import CalendarAPI

class MeetingScheduler:
    def __init__(self):
        self.calendar_api = CalendarAPI()

    async def schedule(self, meeting_data: Dict) -> Dict:
        """
        Schedule meetings based on availability and preferences
        """
        participants = meeting_data.get("participants", [])
        duration = meeting_data.get("duration", 60)  # minutes
        preferred_time_range = meeting_data.get("preferred_time_range", {})

        # Find available slots
        available_slots = await self._find_available_slots(
            participants,
            duration,
            preferred_time_range
        )

        if not available_slots:
            return {
                "success": False,
                "message": "No available slots found",
                "suggested_alternatives": await self._suggest_alternatives(participants)
            }

        # Schedule the meeting
        scheduled_meeting = await self._create_meeting(
            participants,
            available_slots[0],
            duration,
            meeting_data.get("title", ""),
            meeting_data.get("description", "")
        )

        return {
            "success": True,
            "meeting_details": scheduled_meeting,
            "scheduled_time": available_slots[0].isoformat()
        }

    async def _find_available_slots(
        self,
        participants: List[str],
        duration: int,
        preferred_time_range: Dict
    ) -> List[datetime]:
        """
        Find available time slots for all participants
        """
        # Get each participant's calendar
        calendars = {}
        for participant in participants:
            calendars[participant] = await self.calendar_api.get_calendar(participant)

        # Find common free time slots
        common_slots = self._find_common_free_time(
            calendars,
            duration,
            preferred_time_range
        )

        return common_slots

    def _find_common_free_time(
        self,
        calendars: Dict,
        duration: int,
        preferred_time_range: Dict
    ) -> List[datetime]:
        """
        Find common free time slots among all participants
        """
        # Implementation for finding common free time slots
        # This is a simplified version
        available_slots = []
        start_time = datetime.now()
        end_time = start_time + timedelta(days=7)

        current_slot = start_time
        while current_slot < end_time:
            if self._is_slot_available(current_slot, duration, calendars):
                available_slots.append(current_slot)
            current_slot += timedelta(minutes=30)

        return available_slots

    def _is_slot_available(
        self,
        slot: datetime,
        duration: int,
        calendars: Dict
    ) -> bool:
        """
        Check if a time slot is available for all participants
        """
        # Check working hours (9 AM to 5 PM)
        if slot.hour < 9 or slot.hour >= 17:
            return False

        # Check weekends
        if slot.weekday() >= 5:  # Saturday or Sunday
            return False

        # Check each participant's calendar
        for calendar in calendars.values():
            if not self._is_participant_available(slot, duration, calendar):
                return False

        return True

    def _is_participant_available(
        self,
        slot: datetime,
        duration: int,
        calendar: List[Dict]
    ) -> bool:
        """
        Check if a participant is available during a specific time slot
        """
        slot_end = slot + timedelta(minutes=duration)
        
        for event in calendar:
            event_start = event['start']
            event_end = event['end']
            
            if (slot < event_end and slot_end > event_start):
                return False
        
        return True

    async def _create_meeting(
        self,
        participants: List[str],
        time_slot: datetime,
        duration: int,
        title: str,
        description: str
    ) -> Dict:
        """
        Create a meeting and send invitations
        """
        meeting_details = {
            "title": title,
            "description": description,
            "start_time": time_slot,
            "end_time": time_slot + timedelta(minutes=duration),
            "participants": participants
        }

        # Create calendar event
        event = await self.calendar_api.create_event(meeting_details)

        # Send meeting invitations
        await self._send_invitations(meeting_details)

        return event

    async def _send_invitations(self, meeting_details: Dict):
        """
        Send meeting invitations to all participants
        """
        for participant in meeting_details["participants"]:
            await self.calendar_api.send_invitation(
                participant,
                meeting_details
            )