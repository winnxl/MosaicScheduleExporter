import unittest
import datetime
import converter as cv

class TestConverter(unittest.TestCase):

    def setUp(self):
        # Inputs from parseMosaic Module
        # For the corresponding output_#'s below

        # Fall 2018 default YYYY/MM/DD & AM/PM Time (Selection)
        self.input_1 = [('SFWRENG 3MX3 - Signals and Systems',
          'Tutorial',
          'Mo 13:30 - 14:20',
          'ABB B118',
          '04/09/2018 - 05/12/2018'),('SFWRENG 3XA3 - Software Project Management',
          'Lecture',
          'Th 13:30 - 14:20',
          'HSC 1A1',
          '04/09/2018 - 05/12/2018'),('SFWRENG 3XA3 - Software Project Management',
          'Laboratory',
          'We 12:30 - 14:20',
          'ITB 236',
          '04/09/2018 - 05/12/2018')]
        # Winter 2019 default YYYY/MM/DD & AM/PM Time (Selection)
        self.input_2 = [ ('SFWRENG 3I03 - Communications Skills',
  'Laboratory',
  'Th 08:30 - 11:20',
  'ITB 236',
  '01/04/2019 - 06/04/2019'),('SFWRENG 3SH3 - Operating Systems',
  'Lecture',
  'MoWe 08:30 - 09:20',
  'BSB B136',
  '07/01/2019 - 09/04/2019'), ('SFWRENG 3SH3 - Operating Systems',
  'Lecture',
  'Fr 10:30 - 11:20',
  'BSB B136',
  '07/01/2019 - 09/04/2019')]
        # Fall 2018 default DD/MM/YYYY & Military Time (Selection)
        self.input_3 = [('SFWRENG 3RA3 - Sfwr Requirements&Secur Con',
  'Lecture',
  'MoWe 2:30PM - 3:20PM',
  'ABB 102',
  '2018/09/04 - 2018/12/05'), ('SFWRENG 3RA3 - Sfwr Requirements&Secur Con',
  'Lecture',
  'Fr 4:30PM - 5:20PM',
  'ABB 102',
  '2018/09/04 - 2018/12/05')]
        # Winter 2019 default DD/MM/YYYY & Military Time (Selection)
        self.input_4 = [ ('SFWRENG 3SH3 - Operating Systems',
  'Laboratory',
  'Tu 11:30AM - 2:20PM',
  'ITB 236',
  '2019/03/04 - 2019/03/09'),('SFWRENG 3SH3 - Operating Systems',
  'Laboratory',
  'Tu 11:30AM - 2:20PM',
  'ITB 236',
  '2019/03/18 - 2019/03/23'), ('SFWRENG 3SH3 - Operating Systems',
  'Laboratory',
  'Tu 11:30AM - 2:20PM',
  'ITB 236',
  '2019/04/01 - 2019/04/06')]


        # Correct outputs of Converter.convert (for Connector Module)
        # For the corresponding input_#'s above
        self.output_1 = [{'end': {'dateTime': '2018-9-10T14:20:00', 'timeZone': 'America/Toronto'},
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
        self.output_2 = [{'end': {'dateTime': '2019-4-4T11:20:00', 'timeZone': 'America/Toronto'},
  'location': 'ITB 236',
  'recurrence': ['RRULE:FREQ=WEEKLY;UNTIL=20190406T045959Z;BYDAY=TH'],
  'start': {'dateTime': '2019-4-4T08:30:00', 'timeZone': 'America/Toronto'},
  'summary': '3I03 Laboratory'},{'end': {'dateTime': '2019-1-7T09:20:00', 'timeZone': 'America/Toronto'},
  'location': 'BSB B136',
  'recurrence': ['RRULE:FREQ=WEEKLY;UNTIL=20190409T045959Z;BYDAY=MO,WE'],
  'start': {'dateTime': '2019-1-7T08:30:00', 'timeZone': 'America/Toronto'},
  'summary': '3SH3 Lecture'},{'end': {'dateTime': '2019-1-11T11:20:00', 'timeZone': 'America/Toronto'},
  'location': 'BSB B136',
  'recurrence': ['RRULE:FREQ=WEEKLY;UNTIL=20190409T045959Z;BYDAY=FR'],
  'start': {'dateTime': '2019-1-11T10:30:00', 'timeZone': 'America/Toronto'},
  'summary': '3SH3 Lecture'}]
        self.output_3 = [{'end': {'dateTime': '2018-9-5T15:20:00', 'timeZone': 'America/Toronto'},
  'location': 'ABB 102',
  'recurrence': ['RRULE:FREQ=WEEKLY;UNTIL=20181205T045959Z;BYDAY=MO,WE'],
  'start': {'dateTime': '2018-9-5T14:30:00', 'timeZone': 'America/Toronto'},
  'summary': '3RA3 Lecture'}, {'end': {'dateTime': '2018-9-7T17:20:00', 'timeZone': 'America/Toronto'},
  'location': 'ABB 102',
  'recurrence': ['RRULE:FREQ=WEEKLY;UNTIL=20181205T045959Z;BYDAY=FR'],
  'start': {'dateTime': '2018-9-7T16:30:00', 'timeZone': 'America/Toronto'},
  'summary': '3RA3 Lecture'}]
        self.output_4 = [{'end': {'dateTime': '2019-3-5T14:20:00', 'timeZone': 'America/Toronto'},
  'location': 'ITB 236',
  'recurrence': ['RRULE:FREQ=WEEKLY;UNTIL=20190309T045959Z;BYDAY=TU'],
  'start': {'dateTime': '2019-3-5T11:30:00', 'timeZone': 'America/Toronto'},
  'summary': '3SH3 Laboratory'}, {'end': {'dateTime': '2019-3-19T14:20:00', 'timeZone': 'America/Toronto'},
  'location': 'ITB 236',
  'recurrence': ['RRULE:FREQ=WEEKLY;UNTIL=20190323T045959Z;BYDAY=TU'],
  'start': {'dateTime': '2019-3-19T11:30:00', 'timeZone': 'America/Toronto'},
  'summary': '3SH3 Laboratory'}, {'end': {'dateTime': '2019-4-2T14:20:00', 'timeZone': 'America/Toronto'},
  'location': 'ITB 236',
  'recurrence': ['RRULE:FREQ=WEEKLY;UNTIL=20190406T045959Z;BYDAY=TU'],
  'start': {'dateTime': '2019-4-2T11:30:00', 'timeZone': 'America/Toronto'},
  'summary': '3SH3 Laboratory'}]


    # Test Cases for Rfc.offset_date()
    # Case 1: Target weekday of date occurs after target
    def test_offset_date_1(self):
        date = datetime.date(2018, 12, 18)
        self.assertEqual(cv.Rfc.offset_date(date, [0]), ["2018", "12", "24"])

    # Case 2: Target weekday of date occurs before target (offset to the following week)
    def test_offset_date_2(self):
        date = datetime.date(2018, 12, 18)
        self.assertEqual(cv.Rfc.offset_date(date, [2]), ["2018", "12", "19"])

    # Case 3: Multiple target weekdays
    def test_offset_date_3(self):
        date = datetime.date(2018, 12, 18)
        self.assertEqual(cv.Rfc.offset_date(date, [3, 0, 2]), ["2018", "12", "19"])

    # Test Cases for Rfc.extract_date()
    # Case 1: YYYY/MM/DD input format
    def test_extract_date_1(self):
        date_str = "2018/09/04 - 2018/12/05"
        self.assertEqual(cv.Rfc.extract_date(date_str, [0]), ('2018-9-10', '20181205'))

    # Case 2: DD/MM/YYYY input format
    def test_extract_date_2(self):
        date_str = "04/09/2018 - 05/12/2018"
        self.assertEqual(cv.Rfc.extract_date(date_str, [0]), ('2018-9-10', '20181205'))

    # Test Cases for Rfc.to_military()
    # Case 1: Between 12:01 to 11:59 AM
    def test_to_military_1(self):
        self.assertEqual(cv.Rfc.to_military("2:00AM"), "2:00")

    # Case 2: Between 12:01 to 11:59 PM
    def test_to_military_2(self):
        self.assertEqual(cv.Rfc.to_military("2:00PM"), "14:00")

    # Case 3: 12:00 AM
    def test_to_military_3(self):
        self.assertEqual(cv.Rfc.to_military("12:00AM"), "00:00")

    # Case 4: 12:00 PM
    def test_to_military_4(self):
        self.assertEqual(cv.Rfc.to_military("12:00PM"), "12:00")

    # Test Cases for Rfc.extract_weekdays()
    # Case 1: Multiple entries from the set monday to friday
    def test_extract_weekdays_1(self):
        self.assertEqual(cv.Rfc.extract_weekdays("MoWeFr"), ("MO,WE,FR", [0, 2, 4]))

    # Case 2: Single entries from the set monday to friday
    def test_extract_weekdays_2(self):
        self.assertEqual(cv.Rfc.extract_weekdays("Tu"), ("TU", [1]))

    # Case 3: Single entries from the set monday to friday
    def test_extract_weekdays_3(self):
        self.assertEqual(cv.Rfc.extract_weekdays("Th"), ("TH", [3]))

    # Case 4: Multiple entries from the set monday to friday, out of order.
    def test_extract_weekdays_4(self):
        self.assertEqual(cv.Rfc.extract_weekdays("ThMo"), ("MO,TH", [0, 3]))

    # Test Cases for Rfc.rfc_output()
    # Case 1: Expected Input
    def test_rfc_output_1(self):
        self.assertEqual(cv.Rfc.rfc_output("2019/01/07 - 2019/04/09", "We 2:30 - 3:20PM"),
                         ('2019-1-9T2:30:00', '2019-1-9T15:20:00', 'RRULE:FREQ=WEEKLY;UNTIL=20190409T045959Z;BYDAY=WE'))

    # Test Cases for Converter.convert()
    # Case 1: Input 1 - Fall 2018 default YYYY/MM/DD & AM/PM Time
    def test_convert_1(self):
        self.assertEqual(cv.Converter.convert(self.input_1), self.output_1)

    # Case 2: Input 2 - Winter 2019 default YYYY/MM/DD & AM/PM Time
    def test_convert_2(self):
        self.assertEqual(cv.Converter.convert(self.input_2), self.output_2)

    # Case 3: Input 3 - Winter 2019 default DD/MM/YYYY & Military Time
    def test_convert_3(self):
        self.assertEqual(cv.Converter.convert(self.input_3), self.output_3)

    # Case 4: Input 4 - Winter 2019 default DD/MM/YYYY & Military Time
    def test_convert_4(self):
        self.assertEqual(cv.Converter.convert(self.input_4), self.output_4)


if __name__ == '__main__':
    unittest.main()
