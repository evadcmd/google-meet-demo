from google_auth_oauthlib.flow import Flow

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_google_oauth_flow(redirect_uri: str):
    return Flow.from_client_secrets_file(
        CLIENT_CREDENTIALS_FILE, scopes=SCOPES, redirect_uri=redirect_uri
    )
