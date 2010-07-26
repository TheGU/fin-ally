#!/usr/bin/env python

#********************************************************************
# Filename:			database.py
# Authors:			Daniel Sisco, Matt Van Kirk
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
import sys, re, os, datetime
from SQLiteCommands import *
from sqlobject import *
from utils import *

#********************************************************************
class SQLiteExpense():
	"""This is a superclass of genericExpense, and contains additional methods
	for loading data out of the database. """
	
	def __init__(self):
		self.initDatabaseSQLite()
		
	def deleteDataSQLite(self, id):
		"""This function should accept an entry id and delete the data from the
		database at that location."""
		
		(cu, db) = LinkToDatabase(genericExpense.database)
		
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
		(cu, db) = LinkToDatabase(genericExpense.database)
		
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
		
		(cu, db) = LinkToDatabase(genericExpense.database)
		cu.execute(SQLDEF_EXPENSES)
		db.commit()
		db.close()
		
	def insertDataSQLite(self, who, amount, date, desc):
		(cu, db) = LinkToDatabase(genericExpense.database)
		
		# TODO: check for pre-existing date/amount match, if no match, insert	
		cu.execute(SQLDEF_INSERT_EXPENSES % (who, amount, date, desc))
		
		db.commit()
		db.close()
		
	def updateOneSQLite(self, target, newValue, id):
		(cu, db) = LinkToDatabase(genericExpense.database)
		
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
	
	database = ""
	
	def __init__(self):
		self.expenseList = []
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
def CreateBlankDatabase():
	"""This function is called during powerup to ensure that a database
	of the appropriate name exists. The object defined here will be discarded,
	but the database will remain."""
	
	print "Creating database: \n\t", Database.fullName, "\n\n"
	User.createTable()
	ExpenseType.createTable()
	Expense.createTable()
	
	dls = User(name='Daniel Sisco')
	rhs = User(name='Rachel Sisco')
	et1 = ExpenseType(description='clothes')
	et2 = ExpenseType(description='makeup')
	exp1 = Expense(user=dls, expenseType=et1, amount=50.12, 
				description='ExpressDude clothes', date=datetime.now())
	exp2 = Expenses(user=rhs, expenseType=et2, amount=30.45,
				description='BareMinerals makeup', date=datetime.now())
	
	dPrint('printing tables...')
	dPrint('Users:\n')
	dPrint(list(userList))
	dPrint('\n')
	
#********************************************************************
class Database():
	"""The Database object contains database meta data such as name, size, and location, 
	as well as methods for locating a database, arbitrating between several databases, 
	and checking database validity."""
	
	# static variables - will be populated by methods of this class
	name = "";
	fullName = ""
	size = 0;
		
	def IdentifyDatabase(self):
		"""This method will locate a database (.db) file and then load specific pieces of information
		into the appropriate variables for consumption by other modules"""
		self.dbFiles = list(GenFileList('*.db'))
	
		# if any files were present...
		if self.dbFiles:
			#TODO: search for appropriate .db setup in each of these files
			for self.tempFileName in self.dbFiles:
				self.dbNameMatch = re.search('\w+\.db$', self.tempFileName)
				if self.dbNameMatch:				
					# remove the database name from the regex match
					self.databaseName = self.dbNameMatch.group(0)
					
					# store name for global access
					Database.name = self.databaseName
					Database.size = os.path.getsize(Database.name)
					Database.fullName= os.path.abspath(Database.name)
					
					dPrint(Database.name)
					dPrint(Database.size)
					dPrint(Database.fullName)
					
					# TODO: replace with SQLObject construct here
					# self.tempExpense = genericExpense()
					# self.tempExpense.setDatabaseName(Database.name)
					
					break #ensures we load the first valid database
				
		else: # if no database files present, prompt user to create a new database file...
			print "Please enter a new database name ending in '.db'\n"
			self.databaseName = raw_input('database name: ')
			# Strip non alpha-numeric characters out of databaseName
			self.databaseName = re.sub('[^a-zA-Z0-9_.]','',self.databaseName)
			
			# create a blank db with the appropriate name
			Database.name= self.databaseName
			CreateBlankDatabase()	
			
	def GetDatabaseName(self):
		return Database.name
	
	def GetDatabaseSize(self):
		"""Returns database size in bytes"""
		return Database.size
	
#********************************************************************
class User(SQLObject):
	"""User table. Contains the name of the user."""
	name = StringCol()
	
#********************************************************************
class ExpenseType(SQLObject):
	"""Expense type table. Contains a description of the expense category"""
	description = StringCol()
	
#********************************************************************
class Expense(SQLObject):
	"""Expense table. Pulls in User and a Expense type and contains amount, 
	description, and date purchased"""
	user 		= ForeignKey('User')
	expenseType = ForeignKey('ExpenseType')
	amount 		= CurrencyCol()
	description = StringCol()
	date		= DateCol()
	
#********************************************************************
def DbConnect():
	"""This function is responsible for pre-processing the database name gathered at
	powerup into the appropriate format, and then connecting to the database and create
	a global connection object"""
	
	dbPath = Database.fullName
	connPath = dbPath.replace(':', '|') # required by SQLObject for the connection string
	connString = 'sqlite:/' + connPath
	
	# create a connection for all queries to use
	connection = connectionForURI(connString)
	sqlhub.processConnection = connection

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

