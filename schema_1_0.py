#!/usr/bin/env python

#********************************************************************
# Filename:            schema_1_0.py
# Authors:             Daniel Sisco
# Date Created:        9-4-2010
# 
# Abstract: Version 1.0 of the FINally database schema
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
Defines version 1.0 of the schema, as well as instantiates an instance of the MigrateObject class.
Implements required methods (dumpContent, loadContent).
"""

version = "1.0"
dbVer = (1,0)

#************************************
# database schema
#************************************
class User(Entity):
    using_options(tablename='User')
    name         = Field(String, unique=True)
    expenses     = OneToMany('Expense')
    
    def __repr__(self):
        return "<User ('%s', '%s', '%s')>" % (self.id, self.name, self.expenses)

#********************************************************************
class ExpenseType(Entity):
    using_options(tablename='ExpenseType')
    description = Field(String, unique=True)
    expenses     = OneToMany('Expense')

    def __repr__(self):
        return "<ExpenseType ('%s', '%s')>" % (self.id, self.description)

#********************************************************************    
class Expense(Entity):
    using_options(tablename='Expense')
    user         = ManyToOne('User')
    expenseType  = ManyToOne('ExpenseType')
    amount       = Field(Float)
    date         = Field(DateTime)
    description  = Field(String)

    def __repr__(self):
        return "<Expense ('%s', '%s', '%s', '%s', '%s', '%s')>" % (self.id, self.amount, self.date, self.description, self.user, self.expenseType)

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
        MigrateObject.__init__(self, dbPath, version)
        
    def dumpContent(self):
        """dumps User and Version tables as-is"""
        f = open('dump.txt', 'w')
        self.localDict['User'] = User.query.all()
        f.write('%s' % (self.localDict['User']))
        self.localDict['ExpenseType'] = ExpenseType.query.all()
        f.write("%s" % (self.localDict['ExpenseType']))
        self.localDict['Expense'] = Expense.query.all()
        f.write("%s" % (self.localDict['Expense']))
        f.close()
    def loadContent(self):
        """no support for v1.0 load at this time"""
        pass