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

## @file parseMosaic.py
#  @author Cassandra Nicolak, Winnie Liang, Michelle Leung
#  @brief macID: nicolace, liangw15, leungm16
## @date 11/9/2018


## @brief Imported packages and libraries. 
#  @details Imports the PySimpleGUI (which is dependent on Tkinter), webbrowser and urllib. 
#  Also imports local modules parseMosaic, connector, and converter.
import PySimpleGUI as sg
import parseMosaic as pm
import connector
import converter  
import urllib 
import webbrowser



# State Variables
fetchFLG = False
fetchedList = []
googleConn = None



## @brief A method that converts a url from a path name to an absolute file path.
#  @details parseMosaic() requires a specific url format. This method uses the urllib library to convert it.
#  @param userInput A file path name.
#  @return userURL An file url.
def convertURL(userInput):
    pathname = userInput
    url = urllib.request.pathname2url(pathname)
    userURL = urllib.parse.urljoin('file:///C:/', url)
    return userURL


## @brief Parses a locally saved html document.
#  @details This method uses the local module parseMosic's runMe() function. This method will only be executed once per session.
#  due to the functionalty of twisted.internet's reactor which the scrapy library depends on.
#  @param url An file url.
def parseMosaic(url):
    global fetchedList
    fetchedList = pm.runMe(url)
    print(url)


## @brief Formats the visual output for the schedule textbox.
#  @details This method converts the fetchedList into a more readable format for the user.
#  @param fetchList A list containing tuples (a,b,c,d,e).
#  @return userSched A large string of the converted list.
def printSched(fetchList):
    userSched = ''

    for course, component, times, location, startend in fetchList:
        userSched += ('Course: ' + str(course) + '\n'
        'Type: ' + str(component) + '\n'
        'When: ' + str(times) + '\n'
        'Location: ' + str(location) + '\n'
        'Start/End Dates: ' + str(startend) + '\n\n'
        )
    return userSched


# ## @brief Primary function for Fetch button.
#  @details Uses two global variables fetchFLG and fetchedList. This is because parseMosaic()
#  cannot be executed twice in one session due to the limitations with the scrapy library.
#  @param url The input url needed to parse a locally saved html file.
#  @return printSched(fetchedList) If True, updates tbxSchedule with a properly formatted string.
#  If False, updates tbxSchedule with an error message and a properly formatted string.
def fetch(url):
    global fetchFLG
    global fetchedList
    if not fetchFLG:
        fetchFLG = True
        parseMosaic(url)
        return 'Extracted schedule information: \n\n' + printSched(fetchedList)
    else:
        return 'Error: Please restart the application and try again. Only one Fetch can be performed per session.  \n\nCurrent list that ready to be imported: \n\n' + printSched(fetchedList)


# ## @brief Creates a connector object and sets it to the global variable: 'c'.
#  @details Converts the parseMosaic output to Google Api inputs.
def conn():
    global googleConn
    googleConn = connector.Connector(converter.Converter.convert(fetchedList))


# ## @brief Primary function for Login button.
#  @details Authorizes, authenticates, and logs a user into their google account. Checks if there is a service.
#  @return c.check_perms() Returns True if there is a service. Returns false if there is not service.
def login():
    global googleConn
    googleConn.login()
    return googleConn.check_perms()



# ## @brief Logs the user out their google account if the application is closes.
#  @details Deletes the access key file.
def logout():
    global googleConn
    try:
        googleConn.logout()
        print('Logged out.')
    except AttributeError:
        print("User wasn't logged in")






# ## @brief Primary function for Import button.
#  @details Adds a Google calendar.
#  @return googleConn.push_to_schedule() Returns True if the import is successful. Returns False if the import is unsuccessful.
def pushSchedule():
    global googleConn
    return googleConn.push_to_schedule()


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
        break # exit application

    # window buttons 
    elif event == 'Fetch Schedule':    
        if (fetchFLG == False):
            if (sg.PopupYesNo('Warning:', 'You can only Fetch once per session.', ' ', 'Have you selected your schedule with the Browse button first?', ' ') == "Yes"):
                window.FindElement('tbxSchedule').Update(str(fetch(convertURL(value['txtBrowse']))))
            else:
                window.FindElement('tbxSchedule').Update("Click the browse button above to find your schedule file.")
        else:
            window.FindElement('tbxSchedule').Update(str(fetch(convertURL(value['txtBrowse']))))
  

    elif event == 'Login':
        conn() # open a new connection
        if login() == True:
            window.FindElement('tbxLogin').Update(str("Login successful. You are now ready to Import. \n\nPlease note: this may take up to 30 seconds depending on your connection speed."))
        else:
            window.FindElement('tbxLogin').Update(str("Login unsuccessful. Please try again."))
         
  
    elif event == 'Import':
        try:
            if pushSchedule() == True:
                window.FindElement('tbxImport').Update(str("Import successful."))
            else:
                window.FindElement('tbxImport').Update(str("Import unsuccessful."))
        except AttributeError:
                window.FindElement('tbxImport').Update(str("Unable to import. Make sure you are logged in first."))           




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