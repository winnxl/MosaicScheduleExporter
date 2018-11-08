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
pip install PyInstaller
******************************************************************************


******************************************************************************
Development Notes: (the todos)
******************************************************************************

Right now most components don't work. The browse button works, 
but it doesn't send that information anywhere. It will eventually
be used as the fileURL although it may need to be properly formatted to:

    file:///C:/Users/../Desktop/My%20Class%20Schedule.html

fetch() updated the output box. The actual message the user will see
should be different and not just the list of tuples converted into a string.

Many of the elements need to have a  key='namehere'assigned to them.

Currently, most buttons by default close the application. This is expected.

login() and importToCal() are not implemented yet.

After all of this is working correctly, error checking must be added to
account to incorrect filename inputs.


Lastly, PyInstaller and Py2Exe is not cooperating with the scrapy library.
The following works if anything related to the imported parseMosaic lib
is commented out:

pyinstaller -wF guiClient.py

******************************************************************************

'''

# libraries
import PySimpleGUI as sg
import parseMosaic as pm    

# url variable
fileUrl = 'http://c.nicolak.ca/3XA3/My%20Class%20Schedule.html'

#fileUrl = 'file:///C:/Users/Nicolak/Desktop/My%20Class%20Schedule.html'


# The callback functions      
def fetch():
    # return parsed list of tuples      
    ret = pm.runMe(fileUrl)  
    return str(ret)
 
def login():      
    print('Not working.') 

def importToCal():      
    print('Not working.')  


sg.ChangeLookAndFeel('White')      

# ------ Menu Definition ------ #      
menu_def = [['File', ['Open', 'Save', 'Exit', 'Properties']],      
            ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],      
            ['Help', 'About...'], ]      
  

layout = [      
    [sg.Menu(menu_def, tearoff=True)],      
    [sg.Text('Obtaining your class schedule... (user info/guide goes here)', size=(80, 2), justification='center', font=("Helvetica", 10), relief=sg.RELIEF_RIDGE)],       
    [sg.Text(''  * 80)],  
    [sg.Text('Select the file of your saved schedule.', size=(35, 1))],      
    [sg.Text('Choose A File', size=(15, 1), auto_size_text=False, justification='right'),      
        sg.InputText('..\My Class Schedule.html'), sg.FileBrowse()],      
    [sg.Text(''  * 80)],          
    [sg.Button('Fetch Schedule'), sg.Text('Status: ')],
    [sg.Text('_'  * 97)],
    [sg.Text(''  * 80)],   
    [sg.Text('Please check if the below information is correct. If so, login to your Google account.')],                
    [sg.Multiline(default_text='Schedule information will appear here.', size=(95, 10), key='scheduleInfo')],      
    [sg.Text(''  * 80)],
    [sg.Text('_'  * 97)],      
    [sg.Text(''  * 80)],
    [sg.Frame('Google Authentication', [ 
        [sg.Text('After you click Login, your default browser will open')],
         [sg.Text('and you will be asked to login to your Google account.')],       
        [sg.Text(''  * 35)],                           
        [sg.Button('Login')],
        [sg.Text(''  * 35)],  
        [sg.Text('Status: ')],
        [sg.Multiline(default_text='Schedule information will appear here.', size=(40, 3))],
        [sg.Text(''  * 35)]
        ]),        
        sg.Frame('Import to Calendar',[
            [sg.Text('Once you have successfully logged into your Google')],
            [sg.Text('account, click Import.')],              
            [sg.Text(''  * 35)],                                   
            [sg.Button('Import')],
            [sg.Text(''  * 35)],         
            [sg.Text('Status: ')],       
            [sg.Multiline(default_text='Schedule information will appear here.', size=(40, 3))],
            [sg.Text(''  * 35)]
        ])],      
                
    [sg.Exit()]                
]      


window = sg.Window('Mosaic Google Calendar Importer', default_element_size=(40, 1), grab_anywhere=False).Layout(layout)      

#event, values = window.Read()  

while True:      
    (event, value) = window.Read()      
    if event == 'EXIT'  or event is None:      
        break # exit button clicked      
    if event == 'Fetch Schedule':      
        window.FindElement('scheduleInfo').Update(fetch())    
    elif event == 'Login':      
        break # exit button clicked      
    elif event == 'Import':      
        break # exit button clicked 


'''
sg.Popup('Title',      
            'The results of the window.',      
            'The button clicked was "{}"'.format(event),      
            'The values are', values)    

#    [sg.InputText('This is my text')],
#    [sg.Multiline(default_text='Box1', size=(35, 3)),      
#        sg.Multiline(default_text='Box2', size=(35, 3))],                  
'''