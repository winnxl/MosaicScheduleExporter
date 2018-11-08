import sys
import os
from oauth2client import client
from googleapiclient import sample_tools
from socket import gaierror
from httplib2 import ServerNotFoundError

class CalUpload:
    # Testing Constants
    # t_cal_id = "mcmaster.ca_omu726vqd553uub9ebi2mho1ho@group.calendar.google.com"
    t_params1 = {
        "summary": "Event 1",
        "start": "2018-10-10T15:00:00-04:00",
        "end": "2018-10-10T16:00:00-04:00"
    }
    t_params2 = {
        "summary": "Event 2",
        "start": "2018-10-10T15:00:00-04:00",
        "end": "2018-10-10T16:00:00-04:00"
    }
    t_body1 = {
        'summary': t_params1["summary"],
        'start': {
            'dateTime': t_params1["start"],
        },
        'end': {
            'dateTime': t_params1["end"],
        },
    }
    t_body2 = {
        'summary': t_params2["summary"],
        'start': {
            'dateTime': t_params2["start"],
        },
        'end': {
            'dateTime': t_params2["end"],
        },
    }
    t_bodies = [t_body1, t_body2]

    # def __init__(self, bodies):    # Todo: Put me in Final
    def __init__(self, bodies=t_bodies):
        self.service = None
        self.cal_id = None
        self.bodies = bodies

    # Account Login, Authorize and Authenticate
    def login(self):
        try:
            self.service, flags = sample_tools.init(sys.argv, 'calendar', 'v3', __doc__,
                                           __file__, scope='https://www.googleapis.com/auth/calendar')
            return
        except ServerNotFoundError:
            print('Unable to connect. Retry when you have internet access.')
            return None

    # Account Logout
    # Deletes access key file
    def logout(self):
        self.service = None
        os.remove("calendar.dat")
        return

    # Todo: Check Authorization
    def check_perms(self):
        return

    # Create New Calendar
    # Params: name = Name of calendar as it is displayed in Google Calendars
    # Sets: cal_id to new calendar Id
    def create_cal(self, name="Mac Schedule"):
        try:
            cal_res = {"summary": name}
            new_cal = self.service.calendars().insert(body=cal_res).execute()
            self.cal_id = new_cal["id"]
            return True

        except client.AccessTokenRefreshError:
            print('The credentials have been revoked or expired, please re-authorize.')
            return None

        except (gaierror, ConnectionResetError, ServerNotFoundError):
            print('Unable to connect. Retry when you have internet access.')
            return None

    # Insert Event to Calendar
    # Params: cal_id = Calendar Id of newly created calendar, bodies = array of event bodies (dicts)
    def insert_events(self):
        try:
            for body in self.bodies:
                self.service.events().insert(calendarId=self.cal_id, body=body).execute()
            return True

        except client.AccessTokenRefreshError:
            print('The credentials have been revoked or expired, please re-authorize.')
            return None

        except (gaierror, ConnectionResetError, ServerNotFoundError):
            print('Unable to connect. Retry when you have internet access.')
            return None

    # Get # of Events in Calendar
    def get_num_events(self):
        try:
            event_list = self.service.events().list(calendarId=self.cal_id).execute()
            return len(event_list['items'])

        except client.AccessTokenRefreshError:
            print('The credentials have been revoked or expired, please re-authorize.')
            return None

        except (gaierror, ConnectionResetError, ServerNotFoundError):
            print('Unable to connect. Retry when you have internet access.')
            return None

        #return None

    # Checks if events were successfully uploaded to google calendars.
    # Compares number of elements in bodies to number of events in new calendar.
    # Returns: True if successful, False otherwise
    def check_insertion(self):
        return len(self.bodies) == self.get_num_events()

    # For the case where push to schedule was unsuccessful.
    # Remove the newly created cal
    # Returns: True if removal was successful. False Otherwise.
    def remove_new_cal(self):
        try:
            removed = False
            while removed is not '':
                removed = self.service.calendars().delete(calendarId=self.cal_id).execute()     # Returns empty str if successful
            return True

        except client.AccessTokenRefreshError:
            print('The credentials have been revoked or expired. '
                  'You have to remove the newly created calendar manually.')
            return None

        except (gaierror, ConnectionResetError, ServerNotFoundError):
            print('Unable to connect. Retry when you have internet access.')
            return None

    # Wrapper create_cal, insert_events, check_insertion.
    # status var monitors if exceptions have occurred.
    # If so, it stops and tries to remove the calendar if it has been created.
    # Returns true if all good.
    def push_to_schedule(self):
        try:
            status = self.create_cal()
            if status:
                self.insert_events()
            else:
                print("Error creating calendar")
                return False

            # Check if insertion was successful IFF calendar was created
            if self.check_insertion():
                return True
            else:
                self.remove_new_cal()
                return False
        except:
            print("Push to schedule failed")

