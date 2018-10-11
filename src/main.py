import sys
from oauth2client import client
from googleapiclient import sample_tools

# Oauth and login stuff
def main(argv):
    global service
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        # scope='https://www.googleapis.com/auth/calendar.readonly')
        scope='https://www.googleapis.com/auth/calendar')


# Functions used after access is authorized by main:

# Get list of calendars
def list_cals():
    try:
        page_token = None
        while True:
            calendar_list = service.calendarList().list(
                pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                # print(calendar_list_entry)              # All fields for each calendar
                print(calendar_list_entry['summary'])   # Cal title
                print(calendar_list_entry['id'])        # ID Of Cal - Used to get the Cal
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')


# Pass in a calendar ID
# Prints all the events in that calendar.
# TODO Instead of printing, save entries with event id and other useful params like title, time, etc.
def events_in_cal(cal_id):
    global service
    try:
        page_token = None
        while True:
            calendar_list = service.events().list(calendarId=cal_id, pageToken=page_token).execute()
            for event_list_entry in calendar_list['items']:
                # print(event_list_entry)              # All fields for each calendar
                print(event_list_entry['summary'])   # Cal title
                print(event_list_entry['id'])        # ID Of Cal - Used to get the Cal
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')


# Pass in a calendar id and event id
# Deletes an event
def delete_event(cal_id, event_id):
    global service
    try:
        service.events().delete(calendarId=cal_id, eventId=event_id).execute()

    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')


# Pass in a calendar id and event id
# Inserts (Creates) an event
def insert_event(cal_id, params):
    global service
    p_body = {
      'summary': params["title"],
      'start': {
        'dateTime': params["start"],
      },
      'end': {
        'dateTime': params["end"],
      },
    }
    try:
        service.events().insert(calendarId=cal_id, body=p_body).execute()

    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')

service = None
if __name__ == '__main__':
    main(sys.argv)


# Variables for testing
a = 'mcmaster.ca_m9ek5aj14r2r7pg4tei8cl361c@group.calendar.google.com'  # MSE Sample Calendar Id
b = '0v5soplmf3ps7eqbp1d06eqg6o'    # Event 1 Id
ins_params = {
    "title": "Event X",
    "start": "2018-10-10T15:00:00-04:00",
    "end": "2018-10-10T16:00:00-04:00"
}

# list_cals()
events_in_cal(a)
# delete_event(a, x)
# events_in_cal(a)

# insert_event(a, ins_params)


