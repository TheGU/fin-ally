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
from elixir import *
from utils import *
#from datetime import datetime
from datetime import date

#********************************************************************
#							FUNCTIONS
#********************************************************************
def CreateBlankDatabase():
	"""This function is called during powerup to ensure that a database
	of the appropriate name exists. The object defined here will be discarded,
	but the database will remain."""
	
	print "Creating database: \n\t", Database.fullName, "\n\n"
	rhs = User(name='Rachel Sisco')
	dls = User(name='Daniel Sisco')
	clothing = ExpenseType(description='clothing!')
	makeup   = ExpenseType(description='makeup!')
	e1 = Expense(user=rhs, expenseType=makeup, amount='15.01', date=date.today(), description='makeup for mah FACE!')
	e2 = Expense(user=dls, expenseType=clothing, amount='50.25', date = date.today(), description='clothing for mah parts.')
	
	session.commit()
	
#********************************************************************
def DbConnect():
	"""This function is responsible for pre-processing the database name gathered at
	powerup into the appropriate format, and then connecting to the database and create
	a global connection object"""
	
	dbPath = Database.fullName
	connString = 'sqlite:///' + dbPath
	dPrint(connString)
	metadata.bind = connString
	metadata.bind.echo = False
	
	setup_all()
	create_all()
	
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
		"""returns all data in the database in a 2D list in the following format:
		
		   [ 0  ][      1    ][  2   ][ 3  ][     4     ]
		[0][user][expenseType][amount][date][description]
		[1][user][expenseType][amount][date][description]
		
		names in the above diagram correspond to members of the Expense class
		and have types as described in the Expense class."""
		
		minorList=[]
		majorList=[]

		# grab all expenses
		expenseList= Expense.query.all()
		
		# iterate through expenses
		for i in list(expenseList):
			minorList.append(i.user)
			minorList.append(i.expenseType)
			minorList.append(i.amount)
			minorList.append(i.date)
			minorList.append(i.description)
			majorList.append(minorList)
			minorList=[] # clear minor list for next pass
			
		return majorList
	
#********************************************************************
# Create SQLAlchemy tables in the form of python classes.
#********************************************************************
class User(Entity):
	name 		= Field(String)
	expenses 	= OneToMany('Expense')
	
	def __repr__(self):
		return "<User ('%s')>" % (self.name)

class ExpenseType(Entity):
	description = Field(String)
	expenses 	= OneToMany('Expense')

	def __repr__(self):
		return "<ExpenseType ('%s')>" % (self.description)
	
class Expense(Entity):
	user 		= ManyToOne('User')
	expenseType = ManyToOne('ExpenseType')
	amount 		= Field(Float)
	date 		= Field(DateTime)
	description = Field(String)

	def __repr__(self):
		return "<Expense ('%s', '%s', '%s', '%s', '%s')>" % (self.user, self.expenseType, self.amount, self.date, self.description)

#********************************************************************
#							MAIN
#********************************************************************

# Test main functionality
if __name__ == '__main__':
	
	print "creating database\n"
	dbPath = "toots.db"
	connString = 'sqlite:///' + dbPath
	dPrint(connString)
	metadata.bind = connString
	#metadata.bind.echo = True
	
	print "adding sample entries\n"
	
	setup_all()
	create_all()
	
	rhs = User(name="Rachel Sisco")
	print rhs
	dls = User(name="Daniel Sisco")
	print dls
	clothing = ExpenseType(description="clothing!")
	print clothing
	makeup   = ExpenseType(description="makeup!")
	print makeup
	e1 = Expense(user=rhs, expenseType=makeup, amount="15.01", date=date.today(), description="makeup for mah FACE!")
	#e1.user.append(rhs)
	#e1.expenseType.append(makeup)
	e2 = Expense(user=dls, expenseType=clothing, amount="50.25", date = date.today(), description="clothing for mah parts.")
	#e2.user.append(dls)
	#e2.expenseType.append(clothing)
	print "adding", e1, "and", e2, "\n"
	
	print "committing!\n"
	session.commit()
	
	print "dumping database\n"
	q = Expense.query.all()
	print q
	
	print "Please run Fin-ally by launching FINally.py!"