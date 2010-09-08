#!/usr/bin/env python

#********************************************************************
# Filename:            migrate.py
# Authors:             Daniel Sisco
# Date Created:        8-24-2010
# 
# Abstract: This is the Model/Controller component of the FINally SQLite finance tool.
# This file provides driver level functions for data manipulation that can be called
# by the FINally View component (Model-functionality). This file is also responsible
# for post processing and manipulating data before passing it back to the View
# (Controller-functionality).
#
# Version History:  See repository
#
# Copyright 2010 Daniel Sisco
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
# along with Fin-ally.  If not, see <http://www.gnu.org/licenses/>.
#********************************************************************

import sys

# TODO can this be moved into the migration function?
dict          = {}
dbName        = ""
storedVersion = (0,0)
schemaVersion = (0,0)

def dumpFrom1_0():
    from schema_1_0 import SchemaObject
    global dict
    object = SchemaObject(name)
    dict = object.dump()

def loadTo1_1():
    from schema_1_1 import SchemaObject
    global dict
    object = SchemaObject(name)
    object.load(dict)
     
# Test main functionality
if __name__ == '__main__':

    for arg in sys.argv:
        print arg

    name = sys.argv[3]
    tempStoredVersion = sys.argv[1]
    tempSchemaVersion = sys.argv[2]
    storedVersion = (int(tempStoredVersion[0]), int(tempStoredVersion[1]))
    schemaVersion = (int(tempSchemaVersion[0]), int(tempSchemaVersion[1]))
   
    if(schemaVersion != storedVersion):
        # perform migration
        print "mismatch - please upgrade from version", storedVersion, "to version", schemaVersion, "!" 
        
        if(schemaVersion == (1,1)):
            # we're moving to version 1.1
            if(storedVersion == (1,0)):
                print "updating from 1.0 to 1.1"
                dumpFrom1_0()
                loadTo1_1()