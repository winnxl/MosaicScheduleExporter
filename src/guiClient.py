#!/usr/bin/env Python3    

'''
******************************************************************************
This GUI uses PySimpleGUI which depends on Tkinter.
Documentation: https://pysimplegui.readthedocs.io/


******************************************************************************
cmds to install:
******************************************************************************
conda install -c anaconda tk

pip install --upgrade PySimpleGUI

pip install Scrapy

pip install --upgrade oauth2client
pip install --upgrade google-api-python-client

pip install PyInstaller
******************************************************************************
'''

## @file parse_mosaic.py
#  @author Cassandra Nicolak, Winnie Liang, Michelle Leung
#  @brief macID: nicolace, liangw15, leungm16
## @date 11/9/2018


## @brief Imported packages and libraries. 
#  @details Imports the PySimpleGUI (which is dependent on Tkinter), webbrowser and urllib. 
#  Also imports local modules parse_mosaic, connector, and converter.
import PySimpleGUI as sg
import parseMosaic as pm
import connector
import converter  
import urllib 
import webbrowser



# Global Variables
_fetch_flg = False
_fetched_list = []
_google_conn = None



## @brief A method that converts a url from a path name to an absolute file path.
#  @details parse_mosaic() requires a specific url format. This method uses the urllib library to convert it.
#  @param user_input A file path name.
#  @return user_url An file url.
def convert_url(user_input):
    pathname = user_input
    url = urllib.request.pathname2url(pathname)
    user_url = urllib.parse.urljoin('file:///C:/', url)
    return user_url


## @brief Parses a locally saved html document.
#  @details This method uses the local module parseMosic's runMe() function. This method will only be executed once per session.
#  due to the functionalty of twisted.internet's reactor which the scrapy library depends on.
#  @param url An file url.
def parse_mosaic(url):
    global _fetched_list
    _fetched_list = pm.run_me(url)
    print(url)


## @brief Formats the visual output for the schedule textbox.
#  @details This method converts the _fetched_list into a more readable format for the user.
#  @param fetch_list A list containing tuples (a,b,c,d,e).
#  @return user_sched A large string of the converted list.
def print_sched(fetch_list):
    user_sched = ''

    for course, component, times, location, startend in fetch_list:
        user_sched += ('Course: ' + str(course) + '\n'
        'Type: ' + str(component) + '\n'
        'When: ' + str(times) + '\n'
        'Location: ' + str(location) + '\n'
        'Start/End Dates: ' + str(startend) + '\n\n'
        )
    return user_sched



# ## @brief Primary function for Import button.
#  @details Adds a Google calendar.
#  @return _google_conn.push_to_schedule() Returns True if the import is successful. Returns False if the import is unsuccessful.
def push_schedule():
    global _google_conn
    return _google_conn.push_to_schedule()



# ## @brief Primary function for Fetch button.
#  @details Uses two global variables _fetch_flg and _fetched_list. This is because parse_mosaic()
#  cannot be executed twice in one session due to the limitations with the scrapy library.
#  @param url The input url needed to parse a locally saved html file.
#  @return print_sched(_fetched_list) If True, updates tbxSchedule with a properly formatted string.
#  If False, updates tbxSchedule with an error message and a properly formatted string.
def fetch(url):
    global _fetch_flg
    global _fetched_list
    if not _fetch_flg:
        set_fetch()
        parse_mosaic(url)
        return 'Extracted schedule information: \n\n' + print_sched(_fetched_list)
    else:
        return 'Error: Please restart the application and try again. Only one Fetch can be performed per session.  \n\nCurrent list that ready to be imported: \n\n' + print_sched(_fetched_list)


def set_fetch():
    global _fetch_flg
    _fetch_flg = True


# ## @brief Creates a connector object and sets it to the global variable: 'c'.
#  @details Converts the parse_mosaic output to Google Api inputs.
def conn():
    global _google_conn
    _google_conn = connector.Connector(converter.Converter.convert(_fetched_list))


# ## @brief Logs a user intot heir Google account.
#  @details Authorizes, authenticates, and logs a user into their google account. Checks if there is a service.
#  @return c.check_perms() Returns True if there is a service. Returns false if there is not service.
def login():
    global _google_conn
    _google_conn.login()
    return _google_conn.check_perms()



# ## @brief Logs the user out their google account if the application is closes.
#  @details Deletes the access key file.
def logout():
    global _google_conn
    try:
        _google_conn.logout()
        print('Logged out.')
    except AttributeError:
        print("User wasn't logged in.")


# ## @brief Primary function for Fetch button.
#  @details If the _fetch_flg is false, a popup window is activated. If the user selects Yes, the fetch() method 
#  is activated, otherwise it updates tbxSchedule with no_sched_msg. If the _fetch_flg is true, the fetch method 
#  is activated. When _fetch_flg is true, it prevents the popup from appearing after a user has selected 'Yes'.
def fetch_button():
    no_sched_msg = "Click the browse button above to find your schedule file."        
    if (_fetch_flg == False):
        if (fetch_popup() == True):
            window.FindElement('tbxSchedule').Update(str(fetch(convert_url(value['txtBrowse']))))
        else:
            window.FindElement('tbxSchedule').Update(no_sched_msg)
    else:
        window.FindElement('tbxSchedule').Update(str(fetch(convert_url(value['txtBrowse']))))


# ## @brief Handles popup button event.
#  @details Executes a PopupYesNo for the user.
#  @return True The user selects 'Yes'.
#  @return False The user selects 'No'.
def fetch_popup():
    popup_var = sg.PopupYesNo('Warning:', 'You can only Fetch once per session.', ' ', 'Have you selected your schedule with the Browse button first?', ' ')
    if (popup_var == "Yes"):
        return True
    else:
        return False



# ## @brief Primary function for Login button.
#  @details Opens a new connection. If the returned value of login() is true, update tbxLogin with success_msg, 
#  otherwise update tbxLogin with unsuccess_msg.
def login_button():
    success_msg = "Login successful. You are now ready to Import. \n\nPlease note: this may take up to 30 seconds depending on your connection speed."
    unsuccess_msg = "Login unsuccessful. Please try again."
    conn() # open a new connection
    if login() == True:
        window.FindElement('tbxLogin').Update(success_msg)
    else:
        window.FindElement('tbxLogin').Update(unsuccess_msg)



# ## @brief Primary function for Import button.
#  @details If the returned value of push_schedule() is true, update tbxImport with success_msg, otherwise update
#  tbxImport with unsuccess_msg. Catch exception AttributeError and update tbxImport with error_msg.
def import_button():
    success_msg = "Import successful."
    unsuccess_msg = "Import unsuccessful."
    error_msg = "Unable to import. Make sure you are logged in first."
    try:
        if push_schedule() == True:
            window.FindElement('tbxImport').Update(success_msg)
        else:
            window.FindElement('tbxImport').Update(unsuccess_msg)
    except AttributeError:
            window.FindElement('tbxImport').Update(error_msg)      


# gui colour
sg.ChangeLookAndFeel('Reddit')


# menu
menu_def = [['File', ['Open Timetable', 'Open Calendar', 'Exit']],
            ['How to use', ['Obtaining your schedule', 'Fetching your schedule', 'Logging into your google account', 'Importing your schedule']],         
            ['Help', ['Full User Manual', 'About...']]]      


# gui layout
layout = [      
    [sg.Menu(menu_def, tearoff=True)],      
    [sg.Text('Welcome to the Mosaic Schedule Importer application. Please use the [How to use] menu for instructions.', size=(80, 2), justification='center', font=("Helvetica", 10), relief=sg.RELIEF_RIDGE)],       
    [sg.Text(''  * 80)],      
    [sg.Text('Select the file of your saved schedule:', size=(30, 1), auto_size_text=True, justification='right'),      
        sg.InputText('..\My Class Schedule.html', key='txtBrowse'), sg.FileBrowse()],      
    [sg.Text(''  * 80)],           
    [sg.Text('Please check if the below information is correct. If so, click "Login" to login to your Google account.')],                
    [sg.Multiline(default_text='Schedule information will appear here.', size=(95, 10), key='tbxSchedule')],
    [sg.Button('Fetch Schedule')],          
    [sg.Text('_'  * 97)],      
    [sg.Text(''  * 80)],
    [sg.Frame('Google Authentication', [ 
        [sg.Text('After you click Login, your default browser will open')],
         [sg.Text('and you will be asked to login to your Google account.')],       
        [sg.Text(''  * 35)],                           
        [sg.Multiline(default_text='Not logged in.', size=(40, 3), key='tbxLogin')],
        [sg.Button('Login')],       
        [sg.Text(''  * 35)]
        ]),        
        sg.Frame('Import to Calendar',[
            [sg.Text('Once you have successfully logged into your Google')],
            [sg.Text('account, click Import.')],              
            [sg.Text(''  * 35)],                                      
            [sg.Multiline(default_text='Not ready to import.', size=(40, 3), key='tbxImport')],
            [sg.Button('Import')],             
            [sg.Text(''  * 35)]
        ])]           
]      


# generates the gui window
window = sg.Window('Mosaic Google Calendar Importer', default_element_size=(40, 1), grab_anywhere=False).Layout(layout)      


# For button events. Makes sure the application doesn't close once a button is pressed.
while True:      
    (event, value) = window.Read()
  
    if event == 'Exit' or event is None:
        logout()
        print ("Exit application.")  
        break # exit application

    # window buttons 
    elif event == 'Fetch Schedule': 
        fetch_button()
        print ("Fetch button pressed.")
  

    elif event == 'Login':
        login_button()
        print ("Login button pressed.")       
  
    elif event == 'Import':
        import_button()
        print ("Import button pressed.")        




    # menu buttons

    # File
    elif event == 'Open Timetable':
        url = 'https://csprd.mcmaster.ca/psc/prcsprd/EMPLOYEE/HRMS_LS/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL?Page=SSR_SSENRL_LIST&Action=A'
        webbrowser.open(url)

    elif event == 'Open Calendar':
        url = 'https://calendar.google.com/calendar/'
        webbrowser.open(url)


    # How to use
    elif event == 'Obtaining your schedule':
        sg.Popup(
                        'Obtaining your schedule file:', ' ',      
                        '1. Click [Open Timetable] from the menu under [File].', ' ',
                        '2. This will open-up your browser and ask you to login to Mosaic.', ' ',                  
                        '3. After logging in, select your school term and click [Continue].', ' ',
                        '4. Right-click within the browser and select [Save as...]', ' ',
                        '5. Make sure the [Save as type:] says [Webpage, Complete] and not [Webpage, HTML Only].', ' ',
                        '6. Click [Save] to save your file to your computer.', ' ', 
                        )    
    elif event == 'Fetching your schedule':
        sg.Popup(                    
                        'Fetching your schedule:', ' ',                      
                        '1. In the application, select your saved file using the [Browse] button.', ' ',
                        '2. Click [Fetch Schedule].', 'Please note: At this time, you can only fetch your schedule once.', 'You must close and re-open the application to fetch a different schedule.', ' ',
                        '3. If successful, you should see your schedule appear in the large textbox.', 'Make sure to confirm this information is correct prior to proceeding.', ' ', 
                        ) 
    elif event == 'Logging into your google account':
        sg.Popup(                 
                        'Logging into your google account:', ' ',                      
                        '1. After fetching your schedule and visually confirming that the information is correct,', ' ', ' click the [Login] button in the Mosaic Google Calendar Importer application.', ' ',
                        '2. You will be prompted to give permission through your browser.', ' ',
                        '3. After successfully logging into Google,', ' you should see the message in your Browser: ', '"The authentication flow has completed."', ' ',
                        '4. Switch back to the Mosaic Google Calendar Importer application and you should see the message: "Login successful. You are now ready to Import."',  ' ',
                        )
    elif event == 'Importing your schedule':
        sg.Popup(                 
                        'Importing your schedule:', ' ',                      
                        '1. Click the [Import] button.', ' ',
                        '2. Once you see the message: "Import successful.", your calendar will have added a new Calendar named: "Mac Schedule".', ' ',
                        '3. Click [Open Calendar] from the menu under [File] to see your calendar.', ' ',
                        )

    # Help
    elif event == 'Full User Manual':
         url = 'http://c.nicolak.ca/3XA3/User_Manual.pdf'
         webbrowser.open(url)       
        #sg.Popup('Button not implemented yet. May open a pdf')   

    elif event == 'About...':
        sg.Popup('Developers:', 'Cassandra Nicolak, Winnie Liang and Michelle Leung.', 'GitLab: https://gitlab.cas.mcmaster.ca/liangw15/3XA3Project')                           



'''
******************************************************************************
Development Notes: (status)
******************************************************************************

- Error checking must be added to account for incorrect filename inputs.
  Also, Fetch Schedule should perhaps produce a warning message if pressed
  before browsing for a url.


The authentication flow has completed.

******************************************************************************

'''