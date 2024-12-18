import asyncio

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