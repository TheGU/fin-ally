#!/usr/bin/env python

#********************************************************************
# Filename: 	  utils.py
# Authors:        Daniel Sisco
# Date Created:   1-22-2008
# 
# Abstract: A collection of utilities for the Fin-ally project. This 
# file should include most generic utilities. Examples include debug print
# function, file locators, current directory locators, etc.
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
import glob, os, sys, re, cfg
from datetime import date, datetime
 
#********************************************************************
def GenFileList(searchString):
    """This generator function returns a list of all files matching the searchString in a directory"""
    for match in glob.glob(os.path.join(GetCurrentDir(), searchString)):
        yield match

#********************************************************************
def GetCurrentDir():
    """This function returns the absolute path to this Python script"""
    pathname = os.path.dirname(sys.argv[0])
    return(os.path.abspath(pathname))

#********************************************************************
def dPrint(string):
    if cfg.DEBUG == 1:
        print string
        
#********************************************************************
def dateMatch(dateString):
    """Parses the dateString looking for a pre-defined date/time format. 
    Returns a safe datetime object (Jan 1, 1A) if no match is found. 
    Returns the datetime object corresponding to the dateString if a match
    is found."""
    if(re.match('\d{1.2}-\d{1,2}-\d{4}', dateString)):
        localDate = datetime.strptime(dateString, "%m-%d-%Y")
    elif(re.match('\d{1,2}\/\d{1,2}\/\d{4}', dateString)):
        localDate = datetime.strptime(dateString, "%m/%d/%Y")
    elif(re.match('\d{1,2}\.\d{1,2}\.\d{4}', dateString)):
        localDate = datetime.strptime(dateString, "%m.%d.%Y")
    else:
        dateString = '1/1/0001'
        localDate = datetime.strptime(dateString, "%m/%d/%Y")
        print "using default date - no match found"
    return localDate
    
# Test main functionality
if __name__ == '__main__':
    print "Please run Fin-ally by launching FINally.py!"