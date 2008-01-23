#!/usr/bin/env python

#********************************************************************
# Filename: 	fileCheck.py
# Creator: 	Daniel Sisco
# Contributors: Daniel Sisco
# Date Created: 1-22-2008
# 
# Abstract: A collection of Fin-ally specific utilities for database file
# location and analysis.
#
# Version History:  See repository
#********************************************************************
import glob, os, sys

def InitialStartup():
    """This function returns the name of a properly formatted database from
    the Fin-ally path. It will use the first database it finds if there are more
    than one."""
    dbFiles = list(GetDbFiles())
    if dbFiles:
        #search for appropriate .db setup in each of these files
        dan = 1
    else:
        #prompt user to input a new name
        dan = 0
        #create a new database file
    
def GetDbFiles():
    """This function returns a list of all *.db files in a directory"""
    for match in glob.glob(os.path.join(GetCurrentDir(), '*.db')):
        yield match
    
def GetCurrentDir():
    """This function returns the absolute path to this Python script"""
    pathname = os.path.dirname(sys.argv[0])
    return(os.path.abspath(pathname))

InitialStartup()