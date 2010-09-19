#!/usr/bin/env python

#********************************************************************
# Filename:            migrate.py
# Authors:             Daniel Sisco
# Date Created:        9-19-010
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

import sys, re, os
from utils import GenFileList
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

# globals
Base = declarative_base()
dict          = {}
dbName        = ""
storedVersion = [0,0]
schemaVersion = [0,0]

#*****************************************************
class Version(Base):
    __tablename__ = 'versions'
    id = Column(Integer, primary_key=True)
    minor = Column(Integer)
    major = Column(Integer)
    
    def __repr__(self):
        return "<Version('%s', '%s')>" % (self.minor, self.major)

#*****************************************************
def dumpFrom1_0():
    from schema_1_0 import SchemaObject
    global dict
    object = SchemaObject(name)
    dict = object.dump()

#*****************************************************
def loadTo1_1():
    from schema_1_1 import SchemaObject
    global dict
    object = SchemaObject(name)
    object.load(dict)
    
#*****************************************************
def IdentifyDatabase():
    """This method will locate a database (.db) file and then load specific pieces of information
    into the appropriate variables for consumption by other modules"""
    global dbName
    dbFiles = list(GenFileList('*.db'))

    # if any files were present...
    if dbFiles:
        #TODO: search for appropriate .db setup in each of these files
        for tempFileName in dbFiles:
            dbNameMatch = re.search('\w+\.db$', tempFileName)
            if dbNameMatch:                
                # remove the database name from the regex match
                databaseName = dbNameMatch.group(0)
                
                # store name for global access
                dbName = os.path.abspath(databaseName)
                cont = True
                break #ensures we load the first valid database
            
    else: # if no database files present, prompt user to create a new database file...
        cont = False
    
    return cont
     
#*******************************************************************************************************
#                                                 MAIN 
#*******************************************************************************************************
if __name__ == '__main__':   
    # identify database file
    if(True == IdentifyDatabase()):
        
        # pull argument from argv
        tempArgs = sys.argv[1]
        temp = re.split('_', tempArgs)
        schemaVersion[0] = int(temp[0]) 
        schemaVersion[1] = int(temp[1])
        #print "schemaVersion: %s.%s" % (schemaVersion[0], schemaVersion[1])
            
        # remove version from database
        connString = 'sqlite:///' + dbName
        engine = create_engine(connString, echo=False)
        SessionObject = sessionmaker(bind=engine)
        session = SessionObject()
        
        v = session.query(Version).one()
        storedVersion[0] = v.major
        storedVersion[1] = v.minor
        #print "storedVersion: %s.%s" % (storedVersion[0], storedVersion[1])
       
        if(schemaVersion != storedVersion):
            # perform migration
            print "mismatch - please upgrade from version", storedVersion, "to version", schemaVersion, "!" 
            
            if(schemaVersion == (1,1)):
                # we're moving to version 1.1
                if(storedVersion == (1,0)):
                    print "updating from 1.0 to 1.1"
                    dumpFrom1_0()
                    loadTo1_1()
        else:
            print "no migration required"
    else: 
        print "no migration required"
