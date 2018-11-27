import sys, os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = r'C:\\Users\\Michelle\\Anaconda3\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\\Users\\Michelle\\Anaconda3\\tcl\\tk8.6'

build_exe_options = {"packages": ["os", "twisted", "scrapy", "tkinter", "zope", "idna"], "excludes": [], "include_msvcr": True}#, "include_files": ['client_secrets.json']
base = None

setup(name = 'ScheduleImporter',
		version = "0.1",
		description = "",
		options = {"build_exe": build_exe_options},
		executables = [Executable("guiClient.py", base=base)])


"""
from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

DATA=[('imageformats',['C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qjpeg4.dll',
    'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qgif4.dll',
    'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qico4.dll',
    'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qmng4.dll',
    'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qsvg4.dll',
    'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qtiff4.dll'
    ])]


setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True,"includes":["sip"]}},
    windows = [{'script': "guiClient.py"}],
    zipfile = None,
    #data_files = DATA,
)
"""