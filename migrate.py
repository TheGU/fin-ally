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

from database import *
import os

def versionCheck():
    """checks compatibility between the FINally version and the database version"""
    # read database version into a tuple
    storedDbVersion = (Version.query.all()[0].version_major, Version.query.all()[0].version_minor)
    
    # check compatibility
    if(dbVer != storedDbVersion):
        # perform migration
        print "mismatch - please upgrade from version", storedDbVersion, "to version", dbVer, "!"   
        exit(1)
        
def migrate(storedVer, desiredVer):
    """migrates the SQLite database from the stored version to the new version."""
    # create a backup of the database with a new name
    print "creating backup of database..."
    string = "cp %s %s.backup" % (Database().name, Database().name)
    os.popen(string)
    
    if(desiredVer == (1,1)):
        # we're moving to version 1.1
        if(storedVer == (1,0)):
            # we're coming from version 1.0
            #dump all entries
            print "dumping all tables"
            ExpenseTypeList = ExpenseType.query.all()
            ExpenseList = Expense.query.all()
            UserListNames = session.query(User.name)
            print "User table names:", UserListNames
            UserListExpenses = session.query(User.expenses)
            print "User table expenses:", UserListExpenses
            exit(1)
            