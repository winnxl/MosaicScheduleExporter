## @file testGUI.py
#  @author Cassandra Nicolak, Winnie Liang, Michelle Lueng
#  @brief Automated test cases for guiClient.py. Buttons, menus and textbox updates need manual testing.
## @date 12/3/2018
 
#  Imports.
import unittest
import PySimpleGUI as sg
import parseMosaic as pm
import guiClient as gui
import connector
import converter  
import urllib 
import webbrowser


## This class represents test cases for guiClient.py.
class TestGui(unittest.TestCase):

    # initialize varaibles to be used in test cases
    def setUp(self):
        self.maxDiff = None
        self.user_input = "C:/Users/Nicolak/Desktop/My Class Schedule.html"
        self.test_url = "file:///C://Users/Nicolak/Desktop/My%20Class%20Schedule.html"        
        
        self.fetch_url = 'https://gitlab.cas.mcmaster.ca/liangw15/3XA3Project/raw/working/src/testfiles/My%20Class%20Schedule.html'


        self.fetch_str = (
                        'Course: ECON 1BB3 - Introductory Macroeconomics\nType: Lecture\nWhen: We 2:30PM - 3:20PM\nLocation: MDCL 1305\nStart/End Dates: 2019/01/07 - 2019/04/09\n\n'
                        'Course: ECON 1BB3 - Introductory Macroeconomics\nType: Tutorial\nWhen: Fr 12:30PM - 1:20PM\nLocation: ABB 271\nStart/End Dates: 2019/01/07 - 2019/04/09\n\n'
                        'Course: SFWRENG 2FA3 - Discrete Math. Application II\nType: Lecture\nWhen: TuThFr 11:30AM - 12:20PM\nLocation: ITB 137\nStart/End Dates: 2019/01/07 - 2019/04/09\n\n'
                        'Course: SFWRENG 2FA3 - Discrete Math. Application II\nType: Tutorial\nWhen: Mo 11:30AM - 12:20PM\nLocation: BSB 108\nStart/End Dates: 2019/01/07 - 2019/04/09\n\n'
                        'Course: SFWRENG 3A04 - Software Design III\nType: Lecture\nWhen: TuWeFr 3:30PM - 4:20PM\nLocation: HH 109\nStart/End Dates: 2019/01/07 - 2019/04/09\n\n'
                        'Course: SFWRENG 3A04 - Software Design III\nType: Tutorial\nWhen: Mo 3:30PM - 5:20PM\nLocation: ABB 164\nStart/End Dates: 2019/01/07 - 2019/04/09\n\n'
                        'Course: SFWRENG 3S03 - Software Testing\nType: Lecture\nWhen: MoWeTh 1:30PM - 2:20PM\nLocation: CNH B107\nStart/End Dates: 2019/01/07 - 2019/04/09\n\n'
                        'Course: SFWRENG 3S03 - Software Testing\nType: Tutorial\nWhen: Tu 4:30PM - 5:20PM\nLocation: ETB 235\nStart/End Dates: 2019/01/07 - 2019/04/09\n\n'
                        'Course: SFWRENG 4C03 - Comp Networks & Security\nType: Lecture\nWhen: MoWeTh 5:30PM - 6:20PM\nLocation: JHE 264\nStart/End Dates: 2019/01/07 - 2019/04/09\n\n'
                        'Course: SFWRENG 4C03 - Comp Networks & Security\nType: Laboratory\nWhen: Fr 8:30AM - 11:20AM\nLocation: ITB 236\nStart/End Dates: 2019/01/07 - 2019/01/12\n\n'
                        'Course: SFWRENG 4C03 - Comp Networks & Security\nType: Laboratory\nWhen: Fr 8:30AM - 11:20AM\nLocation: ITB 236\nStart/End Dates: 2019/01/21 - 2019/01/26\n\n'
                        'Course: SFWRENG 4C03 - Comp Networks & Security\nType: Laboratory\nWhen: Fr 8:30AM - 11:20AM\nLocation: ITB 236\nStart/End Dates: 2019/02/04 - 2019/02/09\n\n'
                        'Course: SFWRENG 4C03 - Comp Networks & Security\nType: Laboratory\nWhen: Fr 8:30AM - 11:20AM\nLocation: ITB 236\nStart/End Dates: 2019/02/18 - 2019/02/23\n\n'
                        'Course: SFWRENG 4C03 - Comp Networks & Security\nType: Laboratory\nWhen: Fr 8:30AM - 11:20AM\nLocation: ITB 236\nStart/End Dates: 2019/03/04 - 2019/03/09\n\n'
                        'Course: SFWRENG 4C03 - Comp Networks & Security\nType: Laboratory\nWhen: Fr 8:30AM - 11:20AM\nLocation: ITB 236\nStart/End Dates: 2019/03/18 - 2019/03/23\n\n'
                        'Course: SFWRENG 4C03 - Comp Networks & Security\nType: Laboratory\nWhen: Fr 8:30AM - 11:20AM\nLocation: ITB 236\nStart/End Dates: 2019/04/01 - 2019/04/06\n\n'
                        )

        self.sched_str = (
                        'Course: SFWRENG 2DA4 - Digital Sys & Interfacing\nType: Lecture\nWhen: MoWe 11:30AM - 12:20PM\nLocation: CNH B107\nStart/End Dates: 2018/09/04 - 2018/12/05\n\n'
                        'Course: SFWRENG 2DA4 - Digital Sys & Interfacing\nType: Lecture\nWhen: Fr 1:30PM - 2:20PM\nLocation: CNH B107\nStart/End Dates: 2018/09/04 - 2018/12/05\n\n'
                        'Course: SFWRENG 2DA4 - Digital Sys & Interfacing\nType: Laboratory\nWhen: Tu 2:30PM - 5:20PM\nLocation: ITB 238\nStart/End Dates: 2018/09/04 - 2018/12/05\n\n'
                        'Course: SFWRENG 2DM3 - Discrete Math. With Appl. I\nType: Lecture\nWhen: TuThFr 11:30AM - 12:20PM\nLocation: TSH B128\nStart/End Dates: 2018/09/04 - 2018/12/05\n\n'
                        'Course: SFWRENG 2DM3 - Discrete Math. With Appl. I\nType: Tutorial\nWhen: Mo 1:30PM - 2:20PM\nLocation: ETB 237\nStart/End Dates: 2018/09/04 - 2018/12/05\n\n'
                        'Course: SFWRENG 3XA3 - Software Project Management\nType: Lecture\nWhen: Th 1:30PM - 2:20PM\nLocation: HSC 1A1\nStart/End Dates: 2018/09/04 - 2018/12/05\n\n'
                        'Course: SFWRENG 3XA3 - Software Project Management\nType: Laboratory\nWhen: We 12:30PM - 2:20PM\nLocation: ITB 236\nStart/End Dates: 2018/09/04 - 2018/12/05\n\n'
                        'Course: SFWRENG 3XA3 - Software Project Management\nType: Laboratory\nWhen: Tu 7:00PM - 9:00PM\nLocation: ITB 236\nStart/End Dates: 2018/09/04 - 2018/12/05\n\n'
                        )
      
        self.fetch_list = [('SFWRENG 2DA4 - Digital Sys & Interfacing', 'Lecture', 'MoWe 11:30AM - 12:20PM', 'CNH B107', '2018/09/04 - 2018/12/05'), ('SFWRENG 2DA4 - Digital Sys & Interfacing', 'Lecture', 'Fr 1:30PM - 2:20PM', 'CNH B107', '2018/09/04 - 2018/12/05'), ('SFWRENG 2DA4 - Digital Sys & Interfacing', 'Laboratory', 'Tu 2:30PM - 5:20PM', 'ITB 238', '2018/09/04 - 2018/12/05'), ('SFWRENG 2DM3 - Discrete Math. With Appl. I', 'Lecture', 'TuThFr 11:30AM - 12:20PM', 'TSH B128', '2018/09/04 - 2018/12/05'), ('SFWRENG 2DM3 - Discrete Math. With Appl. I', 'Tutorial', 'Mo 1:30PM - 2:20PM', 'ETB 237', '2018/09/04 - 2018/12/05'), ('SFWRENG 3XA3 - Software Project Management', 'Lecture', 'Th 1:30PM - 2:20PM', 'HSC 1A1', '2018/09/04 - 2018/12/05'), ('SFWRENG 3XA3 - Software Project Management', 'Laboratory', 'We 12:30PM - 2:20PM', 'ITB 236', '2018/09/04 - 2018/12/05'), ('SFWRENG 3XA3 - Software Project Management', 'Laboratory', 'Tu 7:00PM - 9:00PM', 'ITB 236', '2018/09/04 - 2018/12/05')]
        

    # tests to see if parse_mosaic() is executed correctly and the order of when fetch() is called
    def test_fetch(self):
        gui.set_list(self.fetch_list)
        
        # executes parse_mosaic() the first time
        self.assertEqual(gui.fetch(self.fetch_url),'Extracted schedule information: \n\n' + self.fetch_str)
        
        # executes parse_mosaic() the second time
        self.assertEqual(gui.fetch(self.fetch_url),'Error: Please restart the application and try again. Only one Fetch can be performed per session.  \n\nCurrent list that ready to be imported: \n\n' + self.fetch_str)

    # tests to see if the url is converted properly
    def test_convert_url(self):
        self.assertEqual(gui.convert_url(self.user_input),self.test_url)
    

    # tests to see if the global varaible is set properly
    def test_set_list(self):
        gui.set_list(self.fetch_list)
        self.assertEqual(gui._fetched_list,self.fetch_list)


    # tests to see if the correct string is returned
    def test_print_sched(self):
        self.assertEqual(gui.print_sched(self.fetch_list),self.sched_str)


    # tests to see if an error is raised if an incorrect type is passed through.
    def test_print_sched_err(self):
        with self.assertRaises(TypeError):
            self.assertEqual(gui.print_sched(1),self.sched_str)


    # tests to see if an error is raised if called before a connection is created
    def test_push_schedule_err(self):
        with self.assertRaises(AttributeError):
            self.assertEqual(gui.push_schedule(),True)

        with self.assertRaises(AttributeError):
            self.assertEqual(gui.push_schedule(),False)          

    # tests to see if an error is raised if called before a connection is created
    def test_login_err(self):
        with self.assertRaises(AttributeError):       
            self.assertEqual(gui.login(),True)  

        with self.assertRaises(AttributeError):       
            self.assertEqual(gui.login(),False) 


    # tests to see if the function returns false if the user is not logged in
    def test_logout(self):
        self.assertEqual(gui.logout(),False) 



# execute unit testing
if __name__ == '__main__':
    unittest.main()



'''

MANUAL TESTING:
    test_fetch_button():
    test_login_button():
    test_import_button():
    test_fetch_popup():  

Tested with other test suite:
    test_conn()
    test_login()
    test_push_schedule()

testParse.py tests this functionality:
    test_parse_mosaic():  

'''