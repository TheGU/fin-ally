#!/usr/bin/env python

#********************************************************************
# Filename: 	   fileCheck.py
# Authors:        Daniel Sisco
# Date Created:   1-22-2008
# 
# Abstract: A collection of Fin-ally specific utilities for database file
# location and analysis.
#
# Version History:  See repository
#
# Copyright 2008 Daniel Sisco
# This file is part of Fin-ally.
#
# Fin-ally is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Fin-ally is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Fn-ally.  If not, see <http://www.gnu.org/licenses/>.
#********************************************************************
import glob, os, sys
from dbDrivers import * 

databaseName = "dummy.db"

def InitialStartup():
    """This function returns the name of a properly formatted database from
    the Fin-ally path. It will use the first database it finds if there are more
    than one."""
    global databaseName
    
    dbFiles = list(GetDbFiles())
    if dbFiles:
        #TODO: search for appropriate .db setup in each of these files
        for tempFileName in dbFiles:
            dbNameMatch = re.search('\w+\.db$', tempFileName)
            if dbNameMatch:
                databaseName = dbNameMatch.group(0)
                break #ensures we load the first valid database
            
    if databaseName == 'dummy.db':
        # Prompt user to create a new database file
        print "Please enter a new database name ending in '.db'\n"
        databaseName = raw_input('database name: ')
        # Strip non alpha-numeric characters out of databaseName
        databaseName = re.sub('[^a-zA-Z0-9_.]','',databaseName)
        CreateBlankDatabase(databaseName)
    
def GetDbFiles():
    """This function returns a list of all *.db files in a directory"""
    for match in glob.glob(os.path.join(GetCurrentDir(), '*.db')):
        yield match
    
def GetCurrentDir():
    """This function returns the absolute path to this Python script"""
    pathname = os.path.dirname(sys.argv[0])
    return(os.path.abspath(pathname))

def GetDatabaseName():
    """This function returns the name of either the pre-existing database, or the
    database the user specifies."""
    global databaseName
    return databaseName
