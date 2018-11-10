## @file converter.py
#  @author Cassandra Nicolak, Winnie Liang, Michelle Leung
#  @brief Converts parseMosaic input to Google Api inputs.
## @date 11/8/2018

## @brief Converts dates and times from parseMosaic output to Rfc formats.
class Rfc:
    ## @brief Converts date from 'YYYY/MM/DD - YYYY/MM/DD' to 'YYYY-MM-DD'
    # @param Takes input in the form of 'YYYY/MM/DD - YYYY/MM/DD'
    # @return Returns 2 outputs, start, in the form of 'YYYY-MM-DD'
    # @return and end, in the form of 'YYYYMMDD'
    # Because start is for Rfc 2232 and end needs to be in Rfc 5545
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

    ## @brief Converts 12-hour to 24-hour time
    # @param Takes a 12-hour time input in the form of for example, '2:30PM'
    # @return Returns military time
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

    ## @brief Converts a string like "MoTuWeThFr" to "MO,TU,WE,TH,FR"
    # @param Takes a string containing weekdays ex. "MoTuWeThFr"
    # @return Returns capitalized string with commas between the weekdays: "MO,TU,WE,TH,FR"
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

    ## @brief Converts date and time strings to Rfc 2232 and 5545 format
    # @param Takes 2 inputs, a date string '2019/01/07 - 2019/04/09' and a time string 'We 2:30PM - 3:20PM'
    # @return Returns a start and end dateTime in RFC 2232 format, and a rrule in Rfc 5545 format
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


## @brief Convert parseMosaic output to Google Api inputs.
class Converter:
    ## @brief Convert parseMosaic output to Google Api inputs.
    # @param Input from parseMosaic module
    # @return Outputs a list of event body dictionary objects
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
