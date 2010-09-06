#!/usr/bin/env python

#********************************************************************
# Filename:            schema_1_1.py
# Authors:             Daniel Sisco
# Date Created:        9-4-2010
# 
# Abstract: Version 1.1 of the FINally database schema
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

from elixir import *
from sqlalchemy import UniqueConstraint
from elixirmigrate.migrate import MigrateObject

"""
Defines version 1.1 of the schema, as well as instantiates an instance of the MigrateObject class.
Implements required methods (dumpContent, loadContent).
"""

version = "1.1"
dbVer = (1,1)

#************************************
# database schema
#************************************
class User(Entity):
    using_options(tablename='User')
    name         = Field(String, unique=True)
    expenses     = OneToMany('Expense')
    default      = OneToMany('Preference')
    
    def __repr__(self):
        return "<User ('%s')>" % (self.name)

#********************************************************************
class ExpenseType(Entity):
    using_options(tablename='ExpenseType')
    description = Field(String, unique=True)
    expenses     = OneToMany('Expense')
    default      = OneToMany('Preference')

    def __repr__(self):
        return "<ExpenseType ('%s')>" % (self.description)

#********************************************************************    
class Expense(Entity):
    using_options(tablename='Expense')
    user         = ManyToOne('User')
    expenseType = ManyToOne('ExpenseType')
    amount         = Field(Float)
    date         = Field(DateTime)
    description = Field(String)

    def __repr__(self):
        return "<Expense ('%s', '%s', '%s', '%s', '%s')>" % (self.user, self.expenseType, self.amount, self.date, self.description)

#********************************************************************
class Preference(Entity):
    using_options(tablename='Preference')
    defaultUser = ManyToOne('User')
    defaultType = ManyToOne('ExpenseType')
    defaultText = Field(String)
    
    def __repr__(self):
        return "<Preference ('%s', '%s', '%s')>" % (self.defaultUser, self.defaultType, self.defaultText)

#********************************************************************    
class Version(Entity):
    using_options(tablename='Version')
    version_major = Field(Integer)
    version_minor = Field(Integer)
    using_table_options(UniqueConstraint('version_major', 'version_minor'))
    
    def __repr__(self):
        return "<Version (%s, %s)>" % (self.version_major, self.version_minor)

#************************************
class SchemaObject(MigrateObject):
    """
    version 1.0 schema object - defines custom dumpContent and loadContent methods
    """
    def __init__(self, dbPath):
        print "creating SchemaObject with path: ", dbPath, "and version: ", version
        MigrateObject.__init__(self, dbPath, version)
        
    def dumpContent(self):
        """dumps User and Version tables as-is"""
        self.localDict['User'] = User.query.all()
        self.localDict['ExpenseType'] = ExpenseType.query.all()
        self.localDict['Expense'] = Expense.query.all()
        self.localDict['Version'] = Version.query.all()
        self.localDict['Preference'] = Preference.query.all()
        
    def loadContent(self):
        """no support for v1.0 load at this time"""
        for i in self.localDict['User']:
            u = User()
            u = i
            u.default = "Rachel Sisco"
        for i in self.localDict['ExpenseType']:
            t = ExpenseType()
            t = i
            t.default = "makeup!"
        for i in self.localDict['Expense']:
            e = Expense()
            e = i
        for i in self.localDict['Version']:
            v = Version()
            v = i