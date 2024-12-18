import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow

CLIENT_CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_access_token():
    token = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        token = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not token or not token.valid:
        # https://stackoverflow.com/questions/10827920/not-receiving-google-oauth-refresh-token
        if token and token.expired and token.refresh_token:
            token.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_CREDENTIALS_FILE, SCOPES)
            token = flow.run_local_server(port=8010)
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(token.to_json())
    return token

def get_google_oauth_flow(redirect_uri :str):
    flow = Flow.from_client_secrets_file(
        CLIENT_CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    return flow