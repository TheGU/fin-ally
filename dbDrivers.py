#!/usr/bin/env python

#********************************************************************
# Filename:		dbDrivers.py
# Authors:		Daniel Sisco, Matt Van Kirk
# Date Created:		4-20-2007
# 
# Abstract: This is the Model/Controller component of the FINally SQLite finance tool.
# This file provides driver level functions for data manipulation that can be called
# by the FINally View component (Model-functionality). This file is also responsible
# for post processing and manipulating data before passing it back to the View
# (Controller-functionality).
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
# along with Fin-ally.  If not, see <http://www.gnu.org/licenses/>.
#********************************************************************

import sqlite3
import re
from SQLiteCommands import *

#********************************************************************
class SQLiteExpense():
	"""This is a superclass of genericExpense, and contains additional methods
	for loading data out of the database. """
	
	def __init__(self):
		self.initDatabaseSQLite()
		
	def deleteDataSQLite(self, id):
		"""This function should accept an entry id and delete the data from the
		database at that location."""
		
		(cu, db) = LinkToDatabase(self.database)
		
		if(0 != id):
			# delete the id passed in
			temp = SQLDEF_DELETE % (id)
			cu.execute(temp)
		
		# commit and close database
		db.commit()
		db.close()

	def getDataSQLite(self, type, arg1, arg2, arg3):
		"""This function returns all data in the current database. The SQLite
		functions return data in the form of a tuple (immutable). We convert
		to a list (mutable). This fcn also takes a 'range' argument which
		specifies if ALL data is required, or just a certain date range."""
		
		# create database connection
		(cu, db) = LinkToDatabase(self.database)
		
		# gather data based on selection type
		if 1 == type:
			# GET DEFAULT DATA
			cu.execute(SQLDEF_GET_ALL)
		if 2 == type:
			# GET RANGE DATA
			temp = SQLDEF_GET_RANGE % (arg1)
			cu.execute(temp)
			# formerly: mpData = GetAllData(cu,"date > 7002007 AND date < 8002007")
			
		# actually get the data based on the above requirements	
		tempData = cu.fetchall()
		listData = list(tempData)
		
		# turn data from tuple into a list (more easily accessible)
		rawData = []
		for i in listData:
			rawData.append(list(i))
			
		self.expenseList = rawData
		
		# close database
		db.close()
		
	def initDatabaseSQLite(self):
		"""This will create the appropriate tables inside the
		datbase specified via _databaseName_ if necessary. This should be the
		first function called from a View component that needs access to a certain
		database."""
		
		# TODO: how should this function be called along with setDatabase() to provide
		# the most sensible seperation of SQLite specific functionality and generic
		# functionality?
		
		(cu, db) = LinkToDatabase(self.database)
		cu.execute(SQLDEF_EXPENSES)
		db.commit()
		db.close()
		
	def insertDataSQLite(self, who, amount, date, desc):
		(cu, db) = LinkToDatabase(self.database)
		
		# TODO: check for pre-existing date/amount match, if no match, insert	
		cu.execute(SQLDEF_INSERT_EXPENSES % (who, amount, date, desc))
		
		db.commit()
		db.close()
		
	def updateOneSQLite(self, target, newValue, id):
		(cu, db) = LinkToDatabase(self.database)
		
		test = SQLDEF_UPDATE % (target, newValue, id)
		cu.execute(test)
		
		db.commit()
		db.close()

#********************************************************************
class genericExpense(SQLiteExpense):
	"""This is a generic base class, and should call functions specifically tailored
	for a particular database. Some of these functions may be plain wrappers, and some
	may contain other generic functionality. This class allows the rest of FINally to use
	database agnostic functionality."""
	
	# TODO: This class should contain all functions that are considered "generic".
	# They should provide functionality to entering, editing, deleting, and returning
	# data - but they should not touch the data itself. Data touching should be done
	# by the SQLiteExpense class
	
	database = "dummy.db"
	
	def __init__(self):
		self.expenseList = []
		#self.database = "dummy.db"
		SQLiteExpense.__init__(self)
	
	def deleteData(self, id):
		self.deleteDataSQLite(id)
		
	def editData(self, target, newValue, id):
		# this can be obsoleted if setData handles both edits and sets
		self.updateOneSQLite(target, newValue, id)
		
	def getData(self):
		return self.expenseList
	
	def loadData(self, type, arg1, arg2, arg3):
		self.getDataSQLite(type, arg1, arg2, arg3)
		
	def setData(self, who, amount, date, desc):
		# this should handle both initial imports and new arrivals if possible
		self.insertDataSQLite(who, amount, date, desc)
		
	def setDatabaseName(self, databaseName):
		"""Sets the database name used for this expense object."""
		genericExpense.database = databaseName
		
	def getDatabaseName(self):
		return genericExpense.database
		
#********************************************************************
def LinkToDatabase(database):
	"""This function will try to link to an existing database, and will create
	such a database is none exists. The single argument is the name of the
	database it is searching for."""
	
	# create global instance of database
	try:
		db = sqlite3.connect(database)
	except sqlite3.Error, errmsg:
		print "Could not open the database file: " + str(errmsg)
		sys.exit()
	
	cu = db.cursor()
	return cu, db

#********************************************************************
def CreateBlankDatabase(databaseName):
	"""This function is called during powerup to ensure that a database
	of the appropriate name exists. The object defined here will be discarded,
	but the database will remain."""
	
	blankDb = genericExpense()
	
	blankDb.setDatabaseName(databaseName)
	blankDb.initDatabaseSQLite()
	
	#DAN - remove these when tested
	blankDb.insertDataSQLite('rachel',1.11, '01012007', 'apple')
	blankDb.insertDataSQLite('rachel',2.11, '01022007', 'bear')
	
	blankDb.getData()

# Test main functionality
if __name__ == '__main__':
	print "Please run Fin-ally by launching FINally.py!"

## EXAMPLE: update one item
#dbUpdateOne(database, 'desc', 'jazz', 2)
#
## EXAMPLE: get all data
#data = dbGetData(database, 1, -1, -1, -1)
#
## EXAMPLE: get a range of data
#data = dbGetData(database, 2, "date > 1002007 AND date < 1042007", -1, -1)
