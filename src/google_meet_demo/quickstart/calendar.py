from datetime import datetime, timedelta

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleMeetCreator:
    def __init__(self, credentials_path):
        SCOPES = [
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/calendar.events",
        ]

        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        credentials = flow.run_local_server(port=8010)

        self.calendar_service = build("calendar", "v3", credentials=credentials)
        self.meet_service = build("calendar", "v3", credentials=credentials)

    def create_meet_event(self, summary, description=None, duration=60):
        """
        Create a Google Meet meeting

        :param summary: Meeting title
        :param description: Meeting description (optional)
        :param duration: Meeting duration (in minutes)
        :return: Meeting details
        """
        start_time = datetime.utcnow() + timedelta(hours=1)
        end_time = start_time + timedelta(minutes=duration)

        event = {
            "summary": summary,
            "description": description or "",
            "start": {
                "dateTime": start_time.isoformat() + "Z",
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end_time.isoformat() + "Z",
                "timeZone": "UTC",
            },
            "conferenceData": {
                "createRequest": {
                    "requestId": f"meet_create_{start_time.isoformat()}",
                    "conferenceSolutionKey": {"type": "hangoutsMeet"},
                }
            },
        }

        event = (
            self.calendar_service.events()
            .insert(calendarId="primary", body=event, conferenceDataVersion=1)
            .execute()
        )

        return {"meeting_link": event.get("hangoutLink"), "event_id": event["id"]}


def main():
    try:
        google_meet_creator = GoogleMeetCreator("./credentials.json")

        meeting = google_meet_creator.create_meet_event(
            summary="google meet demo test",
            description="google meet demo test",
            duration=45,
        )

        print(f"Google Meet URL: {meeting['meeting_link']}")
        print(f"Event ID: {meeting['event_id']}")

    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    main()
