import os.path
import json
import pprint

from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def create_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        return service

    except HttpError as error:
        print(f"An error occurred: {error}")


def main():
    service = create_service()

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        custom_calendars = list(filter(lambda cal: 'group.calendar.google.com' in cal['id'],
                                       calendar_list['items']))
        start_date = datetime(2024, 6, 3)
        end_date = datetime(2024, 6, 10)
        events_map = {}
        for calendar in custom_calendars:
            events = (service.events()
                      .list(calendarId=calendar['id'],
                            timeMin=start_date.astimezone().isoformat(),
                            timeMax=end_date.astimezone().isoformat(),
                            singleEvents=True,
                            orderBy='startTime')
                      .execute())
            events_dict = {}
            for event in events['items']:
                time_taken = (datetime.fromisoformat(event['end']['dateTime'])
                              - datetime.fromisoformat(event['start']['dateTime']))
                if event['summary'] in events_dict.keys():
                    events_dict[event['summary']] += time_taken
                    continue
                events_dict[event['summary']] = time_taken

            events_map[calendar['summary']] = events_dict

        week_time = timedelta()
        for k, v in events_map.items():
            total_time = sum(v.values(), timedelta())
            week_time += total_time
            print('{}: {}'.format(k, str(total_time)))
            for e, t in v.items():
                print('├── {}: {}'.format(e, str(t)))
        print('From {} to {}: {}'.format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), week_time))
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break


if __name__ == "__main__":
    main()
