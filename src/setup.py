## @file setup.py
#  @author Cassandra Nicolak, Winnie Liang, Michelle Leung
#  @brief Setup file to use cx_freeze to convert python program to executable.
## @date 11/26/2018

#importing necessary modules, files, etc.
import sys, os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = r'C:\\Users\\Michelle\\Anaconda3\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\\Users\\Michelle\\Anaconda3\\tcl\\tk8.6'

#build options: to include all needed packages for the program
build_exe_options = {"packages": ["os", "twisted", "scrapy", "tkinter", "zope", "idna"], "excludes": [], "include_msvcr": True}#, "include_files": ['client_secrets.json']
base = None

#setting up the conversion of guiClient.py to an executable.
setup(name = 'ScheduleImporter',
		version = "0.1",
		description = "",
		options = {"build_exe": build_exe_options},
		executables = [Executable("guiClient.py", base=base)])
