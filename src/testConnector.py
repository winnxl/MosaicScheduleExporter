import connector

# The following tests are to be administered manually.
# Run this program, and proceed by pressing "enter" following
# the prompt after each step or test.

input("'Enter' to initialize the Connector object")
bodies = [{'end': {'dateTime': '2018-9-10T14:20:00', 'timeZone': 'America/Toronto'},
  'location': 'ABB B118',
  'recurrence': ['RRULE:FREQ=WEEKLY;UNTIL=20181205T045959Z;BYDAY=MO'],
  'start': {'dateTime': '2018-9-10T13:30:00', 'timeZone': 'America/Toronto'},
  'summary': '3MX3 Tutorial'}, {'end': {'dateTime': '2018-9-6T14:20:00', 'timeZone': 'America/Toronto'},
  'location': 'HSC 1A1',
  'recurrence': ['RRULE:FREQ=WEEKLY;UNTIL=20181205T045959Z;BYDAY=TH'],
  'start': {'dateTime': '2018-9-6T13:30:00', 'timeZone': 'America/Toronto'},
  'summary': '3XA3 Lecture'},{'end': {'dateTime': '2018-9-5T14:20:00', 'timeZone': 'America/Toronto'},
  'location': 'ITB 236',
  'recurrence': ['RRULE:FREQ=WEEKLY;UNTIL=20181205T045959Z;BYDAY=WE'],
  'start': {'dateTime': '2018-9-5T12:30:00', 'timeZone': 'America/Toronto'},
  'summary': '3XA3 Laboratory'}]
con = connector.Connector(bodies)
print("Connector object initialized")

print("\nTest: test_check_perms_1")
input("'Enter' to start this test: ")
print("Result: " + str(con.check_perms()))

print("\nTest: test_login_1")
print("A window will open in your default browser. Login.")
input("'Enter' to start this test: ")
print("Result: " + str(con.login()))

print("\nTest: test_check_perms_2")
input("'Enter' to start this test: ")
print("Result: " + str(con.check_perms()))

print("\nTest: test_create_cal_1")
input("'Enter' to start this test: ")
print("Result: " + str(con.create_cal()))
print("Also log into google calendars to check that a calendar named")
print("Mac Schedule has been created")

print("\nTest: test_insert_events_1")
input("'Enter' to start this test: ")
print("Result: " + str(con.insert_events()))
print("Also log into google calendars to check that events have been inserted")
print("into the Mac Schedule had been created in the step above")

print("\nTest: test_get_num_events_1")
input("'Enter' to start this test: ")
print("Result: " + str(con.get_num_events()))

print("\nTest: test_check_insertion_1")
input("'Enter' to start this test: ")
print("Result: " + str(con.check_insertion()))

print("\nTest: test_remove_new_cal_1")
input("'Enter' to start this test: ")
print("Result: " + str(con.remove_new_cal()))
print("Check Google Calendars to make sure that Mac Schedule has been removed.")

print("\nTest: test_push_to_schedule_1")
input("'Enter' to start this test: ")
print("Result: " + str(con.push_to_schedule()))
print("Check Google Calendars for a new Mac Schedule with events.")
print("Check that the details of the events match those given in the bodies variable below:")
print(bodies)

print("\nTest: test_logout_1")
input("'Enter' to start this test: ")
print("Result: " + str(con.logout()))

print("\nManual testing for connector complete.")
