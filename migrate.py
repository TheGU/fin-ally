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
    global dict, dbName
    object = SchemaObject(dbName)
    dict = object.dump()

#*****************************************************
def loadTo2_0():
    from schema_2_0 import SchemaObject
    global dict, dbName
    object = SchemaObject(dbName)
    object.load(dict)
    
#*****************************************************
def dumpFrom2_0():
    from schema_2_0 import SchemaObject
    global dict, dbName
    object = SchemaObject(dbName)
    dict = object.dump()
    
#*****************************************************
def loadTo2_1():
    from schema_2_1 import SchemaObject
    global dict, dbName
    object = SchemaObject(dbName)
    object.load(dict)    
     
#*******************************************************************************************************
#                                                 MAIN 
#*******************************************************************************************************
if __name__ == '__main__':   
    print "Please run Fin-ally by launching FINally.py!"