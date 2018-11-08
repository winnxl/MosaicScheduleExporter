# Converts parser time output to Rfc
class Rfc:
    # Takes input in the form of 'YYYY/MM/DD - YYYY/MM/DD'
    # Returns 2 outputs, start and end, in the form of 'YYYY-MM-DD'
    # Fixme: Offset start date. Start dates from avenue are mondays regardless of whether or not
    # Fixme: class actually starts on monday. So when inputted into google calendars, we get extra
    # Fixme: entries on monday. Need to find a way to make find the actual date of say, the first
    # Fixme: wednesday after Jan. 6th.
    @staticmethod
    def extract_date(input):
        start, _, end = input.split()
        start = '-'.join(start.split('/'))
        end = ''.join(end.split('/'))
        return start, end

    # Takes a 12-hour time input in the form of for example, '2:30PM'
    # Returns military time
    @staticmethod
    def to_military(input):
        mil = None
        if "AM" in input:
            mil = input.split("AM")[0]
            hr, min = mil.split(":")
            hr = int(hr)
            if hr == 12:
                hr = "00"
            mil = str(hr) + ":" + min
        elif "PM" in input:
            mil = input.split("PM")[0]
            hr, min = mil.split(":")
            hr = int(hr)
            if hr != 12:
                hr += 12
            hr = str(hr)
            mil = hr + ":" + min
        return mil

    # Takes a string containing weekdays ex. "MoTuWeThFr"
    # Returns capitalized string with commas between the weekdays: "MO,TU,WE,TH,FR"
    @staticmethod
    def extract_weekdays(input):
        weekdays = ""
        if "Mo" in input:
            if weekdays != "":
                weekdays += ","
            weekdays += "MO"
        if "Tu" in input:
            if weekdays != "":
                weekdays += ","
            weekdays += "TU"
        if "We" in input:
            if weekdays != "":
                weekdays += ","
            weekdays += "WE"
        if "Th" in input:
            if weekdays != "":
                weekdays += ","
            weekdays += "TH"
        if "Fr" in input:
            if weekdays != "":
                weekdays += ","
            weekdays += "FR"
        return weekdays

    # Takes 2 inputs, a date string '2019/01/07 - 2019/04/09' and a time string 'We 2:30PM - 3:20PM'
    # Returns a start and end dateTime in RFC 2232 format, and a rrule in Rfc 5545 format
    # Todo deal with daylight savings
    @staticmethod
    def rfc_output(date_str, time_str):
        # Extract and Process Strings
        date_start, date_end = Rfc.extract_date(date_str)
        weekdays, time_start, _, time_end = time_str.split()

        # Merge Strings
        # Fixme: -4:00 is fine after ~mar.10, when DST starts.
        # Fixme: -5:00 is fine before, when there is no DST.
        start_date_time = date_start + "T" + Rfc.to_military(time_start) + ":00-04:00"    # RFC 2232 dateTime
        end_date_time = date_start + "T" + Rfc.to_military(time_end) + ":00-04:00"         # RFC 2232 dateTime
        rrule = "RRULE:FREQ=WEEKLY;UNTIL=" + date_end + "T045959Z;BYDAY=" + Rfc.extract_weekdays(weekdays)  # RFC 5545 recurrence RRULE

        return start_date_time, end_date_time, rrule


class Converter:

    # Todo: Add comments and description.
    @staticmethod
    def convert(input):
        output = []
        for item in input:
            start, end, rrule = Rfc.rfc_output(item[4],item[2])

            event = {
                'summary': item[0].split()[1] + " " + item[1],
                'location': item[3],
                'start': {'dateTime': start, 'timeZone': 'America/Toronto'},
                'end': {'dateTime': end, 'timeZone': 'America/Toronto'},
                'recurrence': [rrule]
            }

            print(event)
            output.append(event)
        return output

# Testing Constants/Formats
# Rfc Inputs:
# date_str = '2019/01/07 - 2019/04/09'
# time_str = 'We 2:30PM - 3:20PM'

# Rfc Outputs:
#'dateTime': '2015-05-28T09:00:00-07:00'
#'dateTime': '2015-05-28T17:00:00-07:00'
#'RRULE:FREQ=WEEKLY;UNTIL=20181128T045959Z;BYDAY=TU,TH'
