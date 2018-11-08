
# bodies = None # Array of Dictionaries of Body items
# get Bodies

class Converter:
    # Testing Constants
    # Todo: Remove me in Final or move to a test file
    # Parser Output
    po = [(['SFWRENG 2DA4 - Digital Sys & Interfacing'], ['Lecture'], ['MoWe 11:30AM - 12:20PM'], ['CNH B107']),
        #(['SFWRENG 2DA4 - Digital Sys & Interfacing'], ['Lecture'], ['Fr 1:30PM - 2:20PM'], ['CNH B107']),
        #(['SFWRENG 2DA4 - Digital Sys & Interfacing'], ['Laboratory'], ['Tu 2:30PM - 5:20PM'], ['ITB 238']),
        #(['SFWRENG 2DM3 - Discrete Math. With Appl. I'], ['Lecture'], ['TuThFr 11:30AM - 12:20PM'], ['TSH B128']),
        #(['SFWRENG 2DM3 - Discrete Math. With Appl. I'], ['Tutorial'], ['Mo 1:30PM - 2:20PM'], ['ETB 237']),
        #(['SFWRENG 3BB4 - Software Design II'], ['Lecture'], ['MoWeTh 4:30PM - 5:20PM'], ['CNH B107']),
        #(['SFWRENG 3BB4 - Software Design II'], ['Tutorial'], ['Th 2:30PM - 4:20PM'], ['BSB B155']),
        #(['SFWRENG 3XA3 - Software Project Management'], ['Lecture'], ['Th 1:30PM - 2:20PM'], ['HSC 1A1']),
        #(['SFWRENG 3XA3 - Software Project Management'], ['Laboratory'], ['We 12:30PM - 2:20PM'], ['ITB 236']),
        (['SFWRENG 3XA3 - Software Project Management'], ['Laboratory'], ['Tu 7:00PM - 9:00PM'], ['ITB 236'])]

    # Todo: Resolve if this is needed
    def __init__(self):
        self.input = Converter.po

    @staticmethod
    def find_weekdays(input):
        list = []
        if "Mo" in input:
            list.append("Mo")
        if "Tu" in input:
            list.append("Tu")
        if "We" in input:
            list.append("We")
        if "Th" in input:
            list.append("Th")
        if "Fr" in input:
            list.append("Fr")
        return list

    @staticmethod
    def process_time(input):

        return None, None

    def convert(self):
        output = []
        for item in self.input:
            start, end = self.process_time(item[2][0])

            event = {
                'summary': item[0][0].split()[1] + " " + item[1][0],
                'location': item[3][0],
                'start': {'dateTime': start,},
                'end': {'dateTime': end,},
            }

            print(event)
            output.append(event)
        return output
