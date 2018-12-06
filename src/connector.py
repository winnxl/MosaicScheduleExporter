## @file connector.py
#  @author Cassandra Nicolak, Winnie Liang, Michelle Leung
#  @brief Connects to Google Calendars
## @date 11/8/2018

import sys
import os
from oauth2client import client
from googleapiclient import sample_tools
from socket import gaierror
from httplib2 import ServerNotFoundError

## @brief Connects to Google Calendars
class Connector:
    def __init__(self, bodies):
        self.service = None
        self.cal_id = None
        self.bodies = bodies

    ## @brief Account Login, Authorize and Authenticate
    # @return None if login fails.
    def login(self):
        try:
            self.service, flags = sample_tools.init(sys.argv, 'calendar', 'v3', __doc__,
                                           __file__, scope='https://www.googleapis.com/auth/calendar')
            print(self.service)
            print(flags)
            return True
        except ServerNotFoundError:
            print('Unable to connect. Retry when you have internet access.')
            return None

    ## @brief Account Logout
    # @details Deletes access key file, sets self.service to None
    def logout(self):
        self.service = None
        os.remove("calendar.dat")
        return True

    ## @brief Checks if there is service.
    # @return Returns True if permissions granted, False otherwise
    def check_perms(self):
        if self.service is None:
            return False
        else:
            return True

    ## @brief Create New Calendar
    # @params name = Name of calendar as it is displayed in Google Calendars
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

    ## @brief Insert Event to Calendar
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

    ## @brief Get # of Events in Calendar
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

    ## @brief Checks if events were successfully uploaded to google calendars.
    # @details Compares number of elements in bodies to number of events in new calendar.
    # @return True if successful, False otherwise
    def check_insertion(self):
        return len(self.bodies) == self.get_num_events()

    ## @brief Remove the newly created cal
    # @details For the case where push to schedule was unsuccessful.
    # @return True if removal was successful. False Otherwise.
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

    ## @brief Wrapper for create_cal, insert_events, check_insertion.
    # @return True if all good.
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

    # Pass in a calendar ID
    # Prints all the events in that calendar.
    # def events_in_cal(self, cal_id):
    #     global service
    #     try:
    #         page_token = None
    #         while True:
    #             calendar_list = self.service.events().list(calendarId=cal_id, pageToken=page_token).execute()
    #             for event_list_entry in calendar_list['items']:
    #                 print(event_list_entry)              # All fields for each calendar
    #                 # print(event_list_entry['summary'])   # Cal title
    #                 # print(event_list_entry['id'])        # ID Of Cal - Used to get the Cal
    #             page_token = calendar_list.get('nextPageToken')
    #             if not page_token:
    #                 break
    #
    #     except client.AccessTokenRefreshError:
    #         print('The credentials have been revoked or expired, please re-run'
    #               'the application to re-authorize.')

    #Get Calendars
    # def get_cals(self):
    #     try:
    #         page_token = None
    #         while True:
    #             calendar_list = self.service.calendarList().list(
    #                 pageToken=page_token).execute()
    #             for calendar_list_entry in calendar_list['items']:
    #                 # print(calendar_list_entry)              # All fields for each calendar
    #                 print(calendar_list_entry['summary'])   # Cal title
    #                 print(calendar_list_entry['id'])        # ID Of Cal - Used to get the Cal
    #             page_token = calendar_list.get('nextPageToken')
    #             if not page_token:
    #                 break
    #
    #     except client.AccessTokenRefreshError:
    #         print('The credentials have been revoked or expired, please re-run'
    #               'the application to re-authorize.')