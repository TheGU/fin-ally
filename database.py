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
import sys, re, os
from sqlobject import *
from utils import *
from datetime import datetime

#********************************************************************
#							FUNCTIONS
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
	exp2 = Expense(user=rhs, expenseType=et2, amount=30.45,
				description='BareMinerals makeup', date=datetime.now())
	
#********************************************************************
def DbConnect():
	"""This function is responsible for pre-processing the database name gathered at
	powerup into the appropriate format, and then connecting to the database and create
	a global connection object"""
	
	dbPath = Database.fullName
	connPath = dbPath.replace(':', '|') # required by SQLObject for the connection string
	connString = 'sqlite:/' + connPath
	dPrint(connString)
	
	# create a connection for all queries to use
	connection = connectionForURI(connString)
	sqlhub.processConnection = connection
	
#********************************************************************
#							CLASSES
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
					DbConnect()
					break #ensures we load the first valid database
				
		else: # if no database files present, prompt user to create a new database file...
			print "Please enter a new database name ending in '.db'\n"
			self.databaseName = raw_input('database name: ')
			# Strip non alpha-numeric characters out of databaseName
			self.databaseName = re.sub('[^a-zA-Z0-9_.]','',self.databaseName)
			
			# create a blank db with the appropriate name
			Database.name= self.databaseName
			Database.fullName= os.path.abspath(Database.name)
			DbConnect()
			CreateBlankDatabase()	
			
	def GetDatabaseName(self):
		return Database.name
	
	def GetDatabaseSize(self):
		"""Returns database size in bytes"""
		return Database.size
	
	def GetUserExpenses(self):
		"""returns all data in the database"""
		minorList=[]
		majorList=[]
		userlist = User.select()
		User.sqlmeta.addJoin(MultipleJoin('Expense', joinMethodName='expenses'))
		
		for i in list(userlist):
			#print i.name,"\n"
			#print i.expenses,"\n"
			minorList.append(i.name)
			minorList.append(i.expenses)
			majorList.append(minorList)
			minorList=[]
			
		return majorList
			
		#print "\n"
		#for j in majorList:
		#	print j,"\n"
			
		#print majorList[0][1]
	
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
#							MAIN
#********************************************************************

# Test main functionality
if __name__ == '__main__':
	#database = Database()
	#database.IdentifyDatabase()
	#x = database.GetUserExpenses()
	print "Please run Fin-ally by launching FINally.py!"