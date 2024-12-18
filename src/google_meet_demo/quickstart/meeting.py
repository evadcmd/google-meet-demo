# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START meet_quickstart]
from __future__ import print_function

import os.path

from google.apps import meet_v2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/meetings.space.created"]


def main():
    """Shows basic usage of the Google Meet API."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        # creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        pass
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        # https://stackoverflow.com/questions/10827920/not-receiving-google-oauth-refresh-token
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials-quickstart.json", SCOPES
            )
            creds = flow.run_local_server(port=8010)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        client = meet_v2.SpacesServiceClient(credentials=creds)
        request = meet_v2.CreateSpaceRequest()
        response = client.create_space(request=request)
        print(f"Space created: {response.meeting_uri}")
    except Exception as error:
        # TODO(developer) - Handle errors from Meet API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
# [END meet_quickstart]
