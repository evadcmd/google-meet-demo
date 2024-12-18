from google_auth_oauthlib.flow import Flow

SCOPES = ["https://www.googleapis.com/auth/calendar"]

CLIENT_CREDENTIALS_FILE = "credentials.json"

def get_google_oauth_flow(redirect_uri: str) -> Flow:
    return Flow.from_client_secrets_file(
        CLIENT_CREDENTIALS_FILE, scopes=SCOPES, redirect_uri=redirect_uri
    )
