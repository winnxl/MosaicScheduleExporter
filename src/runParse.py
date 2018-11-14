import parseMosaic as pm
import subprocess as sp
import os

# url variable
#fileUrl = 'http://c.nicolak.ca/3XA3/My%20Class%20Schedule.html'

fileUrl = 'file:///C:/Users/Nicolak/Desktop/mcs/mcs.html'




# return parsed list of tuples
ret = pm.runMe(fileUrl)

#sp.call('cls', shell = True)   # clears the console
print(ret)


# for testing, write results
with open ("testresults.txt","w")as fp:
   for line in ret:
       fp.write(str(line)+"\n")



'''
**************************************************************************************************
Notes for Tkinter:
**************************************************************************************************
1)  Send user to this url:
    https://csprd.mcmaster.ca/psc/prcsprd/EMPLOYEE/HRMS_LS/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL?Page=SSR_SSENRL_LIST&Action=A

2)  They log in, select what term, click Continue.

3)  Right-click, save-as default is 'My Class Schedule.html'.

4)  Browse button, select locaiton of saved file.

    fileUrl variable is set to the browse button/text field's value after 'Scrape' button is pressed.


**************************************************************************************************
Notes for slicer:
**************************************************************************************************

Schedule needs to be sliced every 2 characters until space where time follows. Perhaps can also be be sliced by proper case?


Sample output:

[(['SFWRENG 2DA4 - Digital Sys & Interfacing'], ['Lecture'], ['MoWe 11:30AM - 12:20PM'], ['CNH B107']),
 (['SFWRENG 2DA4 - Digital Sys & Interfacing'], ['Lecture'], ['Fr 1:30PM - 2:20PM'], ['CNH B107']),
 (['SFWRENG 2DA4 - Digital Sys & Interfacing'], ['Laboratory'], ['Tu 2:30PM - 5:20PM'], ['ITB 238']),
 (['SFWRENG 2DM3 - Discrete Math. With Appl. I'], ['Lecture'], ['TuThFr 11:30AM - 12:20PM'], ['TSH B128']),
 (['SFWRENG 2DM3 - Discrete Math. With Appl. I'], ['Tutorial'], ['Mo 1:30PM - 2:20PM'], ['ETB 237']),
 (['SFWRENG 3BB4 - Software Design II'], ['Lecture'], ['MoWeTh 4:30PM - 5:20PM'], ['CNH B107']),
 (['SFWRENG 3BB4 - Software Design II'], ['Tutorial'], ['Th 2:30PM - 4:20PM'], ['BSB B155']),
 (['SFWRENG 3XA3 - Software Project Management'], ['Lecture'], ['Th 1:30PM - 2:20PM'], ['HSC 1A1']),
 (['SFWRENG 3XA3 - Software Project Management'], ['Laboratory'], ['We 12:30PM - 2:20PM'], ['ITB 236']),
 (['SFWRENG 3XA3 - Software Project Management'], ['Laboratory'], ['Tu 7:00PM - 9:00PM'], ['ITB 236'])
 ]



'''