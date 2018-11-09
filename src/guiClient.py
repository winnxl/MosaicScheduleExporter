#!/usr/bin/env Python3    

'''
******************************************************************************
This GUI uses PySimpleGUI which depends on Tkinter.
Documentation: https://pysimplegui.readthedocs.io/


******************************************************************************
cmds to install:
******************************************************************************
pip install python-tk
pip install --upgrade PySimpleGUI

pip install Scrapy

pip install --upgrade oauth2client
pip install --upgrade google-api-python-client

pip install PyInstaller
******************************************************************************
'''

## @file parseMosaic.py
#  @author Cassandra Nicolak, Winnie Liang, Michelle Lueng
#  @brief macID: nicolace, x, x
#  Student #: 000971847, x, x
## @date 11/9/2018


## @brief Imported packages and libraries. 
#  @details Imports the PySimpleGUI which is dependent on Tkinter and urllib. 
#  Also imports local modules parseMosaic, connector, and converter.
import PySimpleGUI as sg
import parseMosaic as pm
import connector
import converter  
import urllib 



# State Variables
fetchFLG = False
fetchedList = []



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


## @brief ...
#  @details ...
#  @param x ...
#  @return x ...
def check_perms():
    if True:
        print ('good to go')


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
        return printSched(fetchedList)
    else:
        return 'Error: Please restart the application and try again. Only one Fetch can be performed per session.  \n\n\n' + printSched(fetchedList)


# ## @brief Primary function for Login button.
#  @details ...
#  @param x ...
#  @return x ...
def login():
    c = connector.Connector(converter.Converter.convert(fetchedList))      
    return c.login()


# ## @brief Primary function for Import button.
#  @details ...
#  @param x ...
#  @return x ...
def push_to_schedule():
    c = connector.Connector(converter.Converter.convert(fetchedList))
    c.push_to_schedule()
    c.remove_new_cal()     
    print('Not working.')
    if True:
        print ('good to go') 


# gui colour
sg.ChangeLookAndFeel('White')      


# menu
menu_def = [['File', ['Open Mosaic', 'Exit']],         
            ['Help', ['Schedule File', 'User Manual', 'Developers']]]      


# gui layout
layout = [      
    [sg.Menu(menu_def, tearoff=True)],      
    [sg.Text('Obtaining your class schedule... (user info/guide goes here)', size=(80, 2), justification='center', font=("Helvetica", 10), relief=sg.RELIEF_RIDGE)],       
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
        break # exit button clicked      
    if event == 'Fetch Schedule':  
        window.FindElement('tbxSchedule').Update(str(fetch(convertURL(value['txtBrowse']))))

    elif event == 'Login':
        window.FindElement('tbxLogin').Update(login())           
  
    elif event == 'Import':
        window.FindElement('tbxImport').Update('Not implemented yet.')    



'''
******************************************************************************
Unused Code:
******************************************************************************
sg.Popup('Title',      
            'The results of the window.',      
            'The button clicked was "{}"'.format(event),      
            'The values are', values)    
            

******************************************************************************
Development Notes: (status)
******************************************************************************

- Most buttons in the menu close the application by default. This is expected.

- Need to implement Login and Import button functionality.

- Error checking must be added to account for incorrect filename inputs.
  Also, Fetch Schedule should perhaps produce a warning message if pressed
  before browsing for a url.

- More doxygen comments need to be added.

-----------------------------------------------------------------------------
Convert from python to exe:
PyInstaller and Py2Exe is not cooperating with the scrapy library.
Also, we need to account for the many modules used.

cmd:
pyinstaller -wF guiClient.py

******************************************************************************

'''