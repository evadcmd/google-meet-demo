from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from googleapiclient.discovery import build

from google_meet_demo import google_meet

router = APIRouter(prefix="", tags=["google OAuth endpoint"])


@router.get(path="/")
async def google_oauth(req: Request):
    flow = await google_meet.get_google_oauth_flow(req.base_url)
    if not req.query_params:
        authorization_url, _state = flow.authorization_url(
            access_type="offline", prompt="consent"
        )
        return RedirectResponse(authorization_url)
    else:
        flow.fetch_token(authorization_response=str(req.url))
        # TODO: cache flow.credentials as token
        calendar = build("calendar", "v3", credentials=flow.credentials)

        event = (
            calendar.events()
            .insert(
                calendarId="primary",
                body=await google_meet.create_meet_event(
                    "google meet demo", "google meet demo"
                ),
                conferenceDataVersion=1,
            )
            .execute()
        )

        return {"meeting_link": event.get("hangoutLink"), "event_id": event["id"]}
