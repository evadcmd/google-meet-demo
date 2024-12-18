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
        # flow.credentials is the token
        calendar = build("calendar", "v3", credentials=flow.credentials)
        events_result = (
            calendar.events().list(calendarId="primary", maxResults=10).execute()
        )
        events = events_result.get("items", [])
        return {"events": events}
