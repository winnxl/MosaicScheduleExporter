## @file converter.py
#  @author Cassandra Nicolak, Winnie Liang, Michelle Leung
#  @brief Converts parseMosaic input to Google Api inputs.
## @date 11/8/2018

import datetime

## @brief Converts dates and times from parseMosaic output to Rfc formats.
class Rfc:

    ## @brief Offsets a date to the next weekday occurrance
    # @param date is a datetime.date(year, month, day) object.
    # @param target_weekday is a list of the numerical representation of the weekdays,
    # monday = 0, ... , friday = 4
    # @returns list of strings containing [year, month, day]
    @staticmethod
    def offset_date(date, target_weekday):
        min_offset = 7  # Minimum Offset. Actual maximum should be 6. So if you return a result with min offset = 7, somethings wrong.

        for weekday in target_weekday:
            offset = weekday - date.weekday()

            if offset < 0:
                offset += 7

            if offset < min_offset:
                min_offset = offset

        new = date + datetime.timedelta(min_offset)

        return [str(new.year), str(new.month), str(new.day)]

    ## @brief Converts date from 'YYYY/MM/DD - YYYY/MM/DD' to 'YYYY-MM-DD'
    # Also offsets start day to the next occurring weekday ex. "next occuring tuesday"
    # @param Takes input in the form of 'YYYY/MM/DD - YYYY/MM/DD'
    # @param weekday_num is a list of the numerical representation of the weekdays,
    # @return Returns 2 outputs, start, in the form of 'YYYY-MM-DD'
    # @return and end, in the form of 'YYYYMMDD'
    # Because start is for Rfc 2232 and end needs to be in Rfc 5545
    @staticmethod
    def extract_date(input, weekday_num):
        start, _, end = input.split()

        # For 2018/09/04 formats
        if len(start.split('/')[0]) == 4:
            start = start.split('/')
            d = datetime.date(int(start[0]), int(start[1]), int(start[2]))
            start = Rfc.offset_date(d, weekday_num)
            start = '-'.join(start)
            end = ''.join(end.split('/'))
        # For 04/09/2018 formats
        else:
            day, month, year = start.split('/')
            d = datetime.date(int(year), int(month), int(day))
            start = Rfc.offset_date(d, weekday_num)
            start = '-'.join(start)
            day, month, year = end.split('/')
            end = ''.join([year, month, day])
        return start, end

    ## @brief Converts 12-hour to 24-hour time
    # @param Takes a 12-hour time input in the form of for example, '2:30PM'
    # @return Returns military time, for example '14:30'
    # Does not make single digit hours have an extra 0. Except for 12:00AM
    # Does not handle seconds. Only hr:min:am/pm formats
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
            return mil
        elif "PM" in input:
            mil = input.split("PM")[0]
            hr, min = mil.split(":")
            hr = int(hr)
            if hr != 12:
                hr += 12
            hr = str(hr)
            mil = hr + ":" + min
            return mil
        else:
            return input


    ## @brief Converts a string like "MoTuWeThFr" to "MO,TU,WE,TH,FR"
    # @param Takes a string containing weekdays ex. "MoTuWeThFr"
    # @return Returns capitalized string with commas between the weekdays: "MO,TU,WE,TH,FR"
    # @return A list of the numerical representation of the weekdays,
    # where monday = 0, ... , friday = 4
    # Does not handle saturdays and sundays
    @staticmethod
    def extract_weekdays(input):
        weekdays = ""
        num = []
        if "Mo" in input:
            if weekdays != "":
                weekdays += ","
            weekdays += "MO"
            num.append(0)
        if "Tu" in input:
            if weekdays != "":
                weekdays += ","
            weekdays += "TU"
            num.append(1)
        if "We" in input:
            if weekdays != "":
                weekdays += ","
            weekdays += "WE"
            num.append(2)
        if "Th" in input:
            if weekdays != "":
                weekdays += ","
            weekdays += "TH"
            num.append(3)
        if "Fr" in input:
            if weekdays != "":
                weekdays += ","
            weekdays += "FR"
            num.append(4)
        return weekdays, num

    ## @brief Converts date and time strings to Rfc 2232 and 5545 format
    # @param Takes 2 inputs, a date string '2019/01/07 - 2019/04/09' and a time string 'We 2:30PM - 3:20PM'
    # @return Returns a start and end dateTime in RFC 2232 format, and a rrule in Rfc 5545 format
    @staticmethod
    def rfc_output(date_str, time_str):
        # Extract and Process Strings
        weekdays, time_start, _, time_end = time_str.split()
        weekday_str, weekday_num = Rfc.extract_weekdays(weekdays)
        date_start, date_end = Rfc.extract_date(date_str, weekday_num)

        # Merge Strings
        start_date_time = date_start + "T" + Rfc.to_military(time_start) + ":00"    # RFC 2232 dateTime
        end_date_time = date_start + "T" + Rfc.to_military(time_end) + ":00"         # RFC 2232 dateTime
        rrule = "RRULE:FREQ=WEEKLY;UNTIL=" + date_end + "T045959Z;BYDAY=" + weekday_str  # RFC 5545 recurrence RRULE

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

            output.append(event)
        return output