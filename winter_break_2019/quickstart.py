from __future__ import print_function
import httplib2
import os
import googleapiclient.discovery as discovery
from oauth2client import client
from oauth2client.file import Storage
import datetime
import pytz


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        # credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def schedule_matcher(year, month, date, hour, year_1, month_1, date_1, hour_1):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # This code is to fetch the calendar ids shared with me
    # Src: https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list
    page_token = None
    calendar_ids = []
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            calendar_ids.append(calendar_list_entry['id'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    # This code is to look for all-day events in each calendar for the month of September
    # Src: https://developers.google.com/google-apps/calendar/v3/reference/events/list
    # You need to get this from command line
    # Bother about it later!
    utc = pytz.utc
    eastern = pytz.timezone('US/Eastern')
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    start_text = '{}/{}/{}   {}:0:0'.format(month, date, year, hour)
    end_text = '{}/{}/{}   {}:0:0'.format(month_1, date_1, year_1, hour_1)

    start_end = []
    for datestring in [start_text, end_text]:
        datee = datetime.datetime.strptime(datestring, "%m/%d/%Y %H:%M:%S")
        date_eastern = eastern.localize(datee, is_dst=None)
        date_utc = date_eastern.astimezone(utc)
        start_end.append(date_utc.strftime(fmt))

    start_hour = int(start_end[0].split()[1].split(':')[0])
    start_date = int(start_end[0].split()[0].split('-')[2])
    start_month = int(start_end[0].split()[0].split('-')[1])
    start_year = int(start_end[0].split()[0].split('-')[0])
    end_hour = int(start_end[1].split()[1].split(':')[0])
    end_date = int(start_end[1].split()[0].split('-')[2])
    end_month = int(start_end[1].split()[0].split('-')[1])
    end_year = int(start_end[1].split()[0].split('-')[0])

    start_date = datetime.datetime(start_year, start_month, start_date, start_hour, 00, 00).isoformat() + 'Z'
    end_date = datetime.datetime(end_year, end_month, end_date, end_hour, 59, 00).isoformat() + 'Z'

    return_list = []
    for calendar_id in calendar_ids:
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start_date,
            timeMax=end_date,
            singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            continue
        for event in events:
            if event['creator']['email'] == 'en.usa#holiday@group.v.calendar.google.com':
                continue
            return_list.append(event['summary'])

    return return_list


if __name__ == '__main__':
    schedule_matcher(2020, 1, 8, 20, 2020, 1, 8, 23)
