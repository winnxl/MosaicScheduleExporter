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


## This class represents test cases for parseMosaic.py.
class TestGui(unittest.TestCase):

    # initialize varaibles to be used in test cases
    def setUp(self):
        self.user_input = "C:/Users/Nicolak/Desktop/My Class Schedule.html"
        self.test_url = "file:///C://Users/Nicolak/Desktop/My%20Class%20Schedule.html"        
        
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
        
        # currently unused:
        #self.empty_fetched_list = []   
        #self.f_fetch_flg = False
        #self.t_fetch_flg = True     

        #self.google_conn = connector.Connector(converter.Converter.convert(_fetched_list))




    # testParse.py tests this functionality.
    #def test_parse_mosaic(self):


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


    # testConnection.py will test this functionality?
    #def test_push_schedule(self)


    # tests to see if an error is raised if called before a connection is created
    def test_push_schedule_err(self):
        with self.assertRaises(AttributeError):
            self.assertEqual(gui.push_schedule(),True)

        with self.assertRaises(AttributeError):
            self.assertEqual(gui.push_schedule(),False)          


    # tests to see if parse_mosaic() is executed correctly and the  order of when fetch() is called
    def test_fetch(self):
        gui.set_list(self.fetch_list)
        
        # executes parse_mosaic() the first time
        self.assertEqual(gui.fetch(self.test_url),'Extracted schedule information: \n\n' + self.sched_str)
        
        # executes parse_mosaic() the secondt time
        self.assertEqual(gui.fetch(self.test_url),'Error: Please restart the application and try again. Only one Fetch can be performed per session.  \n\nCurrent list that ready to be imported: \n\n' + self.sched_str)


    # testConnection.py will test this functionality?
    #def test_conn(self)


    # testConnection.py will test this functionality?
    #def test_login(self)


    # unsure, under investigation:
    # Namespace(auth_host_name='localhost', auth_host_port=[8080, 8090], logging_level='ERROR', noauth_local_webserver=False)
    #--noauth_local_webserver
    def test_login_err(self):
        with self.assertRaises(AttributeError):       
            self.assertEqual(gui.login(),True)  

        with self.assertRaises(AttributeError):       
            self.assertEqual(gui.login(),False) 


    # tests to see if the function returns false if the user is not logged in
    def test_logout(self):
        self.assertEqual(gui.logout(),False) 


    # MANUAL TESTING:
    #def test_fetch_button(self):
    #def test_login_button(self):
    #def test_import_button(self):
    #def fetch_popup():  
        

    #def tearDown(self):
        
# execute unit testing
if __name__ == '__main__':
    unittest.main()


