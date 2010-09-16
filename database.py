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

#import sqlite3
import sys, re, os
from utils import *
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

Base = declarative_base()

def IdentifyDatabase():
	"""This method will locate a database (.db) file and then load specific pieces of information
	into the appropriate variables for consumption by other modules"""
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
				fullName = os.path.abspath(databaseName)
				Database().SetName(fullName)
				dPrint(fullName)
				
				break #ensures we load the first valid database
			
	else: # if no database files present, prompt user to create a new database file...
		print "Please enter a new database name ending in '.db'\n"
		databaseName = raw_input('database name: ')
		# Strip non alpha-numeric characters out of databaseName
		databaseName = re.sub('[^a-zA-Z0-9_.]','',databaseName)
		
		# store full name and flag as a new database
		fullName = os.path.abspath(databaseName)
		d = Database()
		d.SetName(fullName)
		d.__class__.newDb = True
	
	return fullName

#********************************************************************
#							CLASSES
#********************************************************************
class Database():
	"""The Database object contains database meta data such as name, size, and location, 
	as well as methods for locating a database, arbitrating between several databases, 
	and checking database validity."""
	
	# static variables - will be populated by methods of this class
	fullName = ""
	newDb = False
			
	def Create(self):
		"""connects to a specific database"""
		print "creating all tables"
		Base.metadata.create_all(engine)
		
		if 1 == self.newDb:
			print "creating blank database"
			self.InitBlankDb()
			self.newDb = False
		
	def InitBlankDb(self):
		"""This function is called during powerup to ensure that a database
		of the appropriate name exists. The object defined here will be discarded,
		but the database will remain."""
		
		session = SessionObject()
		
		print "Creating database: \n\t", Database.fullName, "\n\n"
		rhs = User(name='Rachel Sisco', shortName='Rachel')
		dls = User(name='Daniel Sisco', shortName='Dan')
		session.add_all([rhs, dls])
		session.commit()
		clothing = ExpenseType(description='clothing!')
		makeup   = ExpenseType(description='makeup!')
		session.add_all([clothing, makeup])
		session.commit()
		e1 = Expense(user=rhs, expenseType=makeup, amount='15.01', date=date.today(), description='makeup for mah FACE!')
		e2 = Expense(user=dls, expenseType=clothing, amount='50.25', date=date.today(), description='clothing for mah parts.')
		session.add_all([e1,e2])
		session.commit()
		
		session.close()
	
	def CreateUser(self, user):
		"""Creates a new user"""
		session = SessionObject()
		session.commit()
		session.close()
		
	def CreateType(self, type):
		"""Creates a new type"""
		session = SessionObject()
		session.commit()
		session.close()
	
	def CreateExpense(self, amount, desc, date, userName, typeDesc):
		"""Creates a new expense"""
		session = SessionObject()

		e = Expense()
		e.amount = amount
		e.description = desc
		e.date = date
		e.user = session.query(User).filter(User.name==userName).one()
		e.expenseType = session.query(ExpenseType).filter(ExpenseType.description==typeDesc).one()

		session.add(e)
		session.commit()		
		session.close()
		
	def EditExpense(self, amount, desc, date, userId, typeId, inputId):
		"""Edits an existing object - expects to get arguments corresponding
		to Expense object members:
			amount
			description
			date
			user_id
			expenseType_id
			id
		"""
		#TODO: can we just pass an ExpenseObject?
		session = SessionObject()
		
		e = session.query(Expense).filter(Expense.id==inputId).one()
		e.amount = amount
		e.description = desc
		e.date = date
		e.user_id = userId
		e.expenseType_id = typeId
		
		session.commit()
		session.close()
		
	def DeleteExpense(self, deleteId):
		"""Removes an expense with the appropriate ID from the database"""
		session = SessionObject()
		expense = session.query(Expense).filter(Expense.id==deleteId)
		session.delete(expense)
		session.commit()
		session.close()
	
	def GetUserList(self):
		"""Returns a list of user names - nothing else."""
		list = []
		session = SessionObject()
		userList = session.query(User).all()
		for i in userList:
			list.append(str(i.name))
		session.close()
		return list
	
	def GetUser(self, userName):
		"""returns the User object matching the input name"""
		#TODO: add fault handling here
		session = SessionObject()
		u = session.query(User).filter(User.name==userName).one()
		session.close()
		return u
	
	def GetUserId(self, userName):
		"""reurns the User object id matching the input name"""
		#TODO: add fault handling here
		session = SessionObject()
		uId = session.query(User).filter(User.name==userName).one().id
		session.close()
		return uId
	
	def GetAllUsers(self):
		"""returns all user data in the database in a 2D list in the following format:
		
		   [ 0  ][5 ]
		[0][user][id]
		[1][user][id]
		
		user and expenseType are dereferenced down to the underlying string, 
		and amount and date are cast to string types to appease the grid."""
		
		minorList=[]
		majorList=[]
		session = SessionObject()

		# grab all expenses
		userList = session.query(User).all()
		
		# iterate through expenses - packing into listxlist
		for i in userList:
			# dereference these all the way down to the string
			minorList.append(i.name) 
			minorList.append(str(i.id))
			
			# push minorList into majorList 
			majorList.append(minorList)
			minorList=[]
			
		session.close()
			
		return majorList		
	
	def GetTypeList(self):
		"""Returns a list of expense types - nothing else."""
		list = []
		session = SessionObject()
		typeList = session.query(ExpenseType).all()
		for i in typeList:
			list.append(str(i.description))
		session.close()
		return list
	
	def GetExpenseType(self, typeName):
		"""returns an ExpenseType object matching the typeName argument"""
		#TODO add fault handling here
		session = SessionObject()
		t = session.query(ExpenseType).filter(ExpenseType.description == typeName).one()
		session.close()
		return t
	
	def GetExpenseTypeId(self, typeName):
		"""returns an ExpenseType id matching the typeName argument"""
		#TODO add fault handling here
		session = SessionObject()
		tId = session.query(ExpenseType).filter(ExpenseType.description==typeName).one().id
		session.close()
		return tId
	
	def GetAllTypes(self):
		"""returns all user data in the database in a 2D list in the following format:
		
		   [     0     ][5 ]
		[0][description][id]
		[1][description][id]
		"""
		
		minorList=[]
		majorList=[]
		session = SessionObject()

		# grab all expenses
		typeList= session.query(ExpenseType).all()
		
		# iterate through expenses - packing into listxlist
		for i in typeList:
			# dereference these all the way down to the string
			minorList.append(i.description) 
			minorList.append(str(i.id))
			
			# push minorList into majorList 
			majorList.append(minorList)
			minorList=[]
			
		session.close()
		return majorList
	
	def GetExpense(self, reqId):
		"""returns the Expense object matching the reqId input"""
		#TODO: add fault handling here
		session = SessionObject()
		e = session.query(Expense).filter(Expense.id==reqId).one()
		session.close()
		return e
	
	def GetAllExpenses(self):
		"""returns all data in the database in a 2D list in the following format:
		
		   [ 0  ][      1    ][  2   ][ 3  ][     4     ][5 ][6  ]
		[0][user][expenseType][amount][date][description][id][del]
		[1][user][expenseType][amount][date][description][id][del]
		
		user and expenseType are dereferenced down to the underlying string, 
		and amount and date are cast to string types to appease the grid."""
		
		minorList=[]
		majorList=[]
		session = SessionObject()

		# grab all expenses
		expenseList = session.query(Expense).all()
		
		# iterate through expenses - packing into listxlist
		for i in expenseList:
			# print "DAN: ", i
			# dereference these all the way down to the string
			minorList.append(i.user.name) 
			minorList.append(i.expenseType.description)
			
			# convert these into strings
			minorList.append(str(i.amount))
			minorList.append(str(i.date))
			
			# this is just normal
			minorList.append(i.description)
			minorList.append(i.id)
			
			# append the 'delete' column
			minorList.append("delete")
			
			# push minorList into majorList 
			majorList.append(minorList)
			minorList=[]
			
		session.close()
			
		return majorList
	
	def SetName(self, name):
		self.fullName = name
		
	def FlagNewDb(self):
		self.newDb = True
	
#********************************************************************
# Create SQLAlchemy tables in the form of python classes.
#********************************************************************
class User(Base):
	__tablename__ = 'users'
	id        = Column(Integer, primary_key=True)
	name      = Column(String)
	shortName = Column(String)
	
	def __repr__(self):
		return "<User('%s', '%s')>" % (self.name, self.shortName)

#********************************************************************
class ExpenseType(Base):
	__tablename__ = 'expenseTypes'
	
	id          = Column(Integer, primary_key=True)
	description = Column(String)
	
	def __repr__(self):
		return "<ExpenseType('%s')>" % (self.description)

#********************************************************************	
class Expense(Base):
	__tablename__ = 'expenses'
	id      = Column(Integer, primary_key=True)
	amount  = Column(Integer)
	date    = Column(String)
	description = Column(String)
	
	# define user_id to support database level link and user for class level link
	user_id = Column(Integer, ForeignKey('users.id'))
	user    = relationship(User, backref=backref('expenses', order_by=id))
	
	expenseType_id = Column(Integer, ForeignKey('expenseTypes.id'))
	expenseType    = relationship(ExpenseType, backref=backref('expenseTypes', order_by=id))
	
	def __repr__(self):
		return "<Expense('%s', '%s', '%s')>" % (self.amount, self.date, self.description)

class Version(Base):
	__tablename__ = 'versions'
	id = Column(Integer, primary_key=True)
	minor = Column(Integer)
	major = Column(Integer)
	
	def __repr__(self):
		return "<Version('%s', '%s')>" % (self.minor, self.major)
	
#********************************************************************
#					  DATABASE.PY CONTENT
#********************************************************************
connString = 'sqlite:///' + IdentifyDatabase()
dPrint(connString)

engine = create_engine(connString, echo=False)
SessionObject = sessionmaker(bind=engine)

Database().Create()

#********************************************************************
#							MAIN
#********************************************************************

# Test main functionality
if __name__ == '__main__':
	print "Please run Fin-ally by launching FINally.py!"