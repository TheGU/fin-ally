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

from database import dbVer, Database

# TODO can this be moved into the migration function?
dict = {}

def dumpFrom1_0():
    from schema_1_0 import SchemaObject
    global dict
    object = SchemaObject(Database().name)
    dict = object.dump()

def loadTo1_1():
    from schema_1_1 import SchemaObject
    global dict
    object = SchemaObject(Database().name)
    object.load(dict)

def versionCheck():
    """
    checks compatibility between the FINally version and the database version
    """
    # read database version into a tuple
    storedDbVersion = Database().GetVersion()
    
    print "stored version is: ", storedDbVersion
    print "local version is: ", dbVer
    
    # check compatibility
    if(dbVer != storedDbVersion):
        # perform migration
        print "mismatch - please upgrade from version", storedDbVersion, "to version", dbVer, "!" 
        migrate(storedDbVersion, dbVer)  
        
def migrate(storedVer, desiredVer):
    """migrates the SQLite database from the stored version to the new version."""
    dict = {}
    
    #TODO: this needs to be replaced by more svelte functionality
    if(desiredVer == (1,1)):
        # we're moving to version 1.1
        if(storedVer == (1,0)):
            print "updating from 1.0 to 1.1"
            dumpFrom1_0()
            loadTo1_1()
            
# Test main functionality
if __name__ == '__main__':   
    print "creating database\n"
    dbPath = "test.db"
    connString = 'sqlite:///' + dbPath
    
    con = sqlite3.connect(dbPath)
    # print list of tables in database
    c = con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    for i in c:
        print i
        
    # print list of users in database
    c = con.execute("SELECT * from User")
    for i in c:
        print i
       
    try:
        c = con.execute("ALTER TABLE User ADD COLUMN defaultUser INTEGER")
    except sqlite3.OperationalError:
        print "table likely already exists"
    
    c = con.execute("SELECT * from USER")
    for i in c:
        print i