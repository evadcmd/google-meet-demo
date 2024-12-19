import asyncio
from datetime import datetime, timedelta
from typing import Any

from google_auth_oauthlib.flow import Flow

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
]

CLIENT_CREDENTIALS_FILE = "credentials.json"


def _get_google_oauth_flow_async(redirect_uri: str) -> Flow:
    return Flow.from_client_secrets_file(
        CLIENT_CREDENTIALS_FILE, scopes=SCOPES, redirect_uri=redirect_uri
    )


async def get_google_oauth_flow(redirect_uri: str) -> Flow:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _get_google_oauth_flow_async, redirect_uri)


async def create_meet_event(
    summary: str = "",
    description: str = "",
    start_time: datetime | None = None,
    duration: int = 60,
) -> dict[str, Any]:
    """
    Create a Google Meet meeting

    :param summary: Meeting title
    :param description: Meeting description (optional)
    :param duration: Meeting duration (in minutes)
    :return: Meeting details
    """
    if not start_time:
        start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(minutes=duration)

    return {
        "summary": summary,
        "description": description,
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
