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

import sys, re, os
from utils import GenFileList, dPrint, BLANK_TERM
from datetime import date, datetime
from schema_2_2 import *
from colInfo import colInfo

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
		d.FlagNewDb()
	
	return fullName

#********************************************************************
#							CLASSES
#********************************************************************
class FilterTerms():
	"""Class containing filter terms for global use. Methods 
	include getters and setters for all filter methods."""
	
	startMonth = datetime.now().month
	monthRange = 1
	searchTerms = "[BLANK]"
	
	def SetStartMonth(self, month):
		self.__class__.startMonth = month
	
	def GetStartMonth(self):
		return self.__class__.startMonth
	
	def SetMonthRange(self, range):
		self.__class__.monthRange = range

	def GetMonthRange(self):
		return self.__class__.monthRange
	
	def SetSearchTerms(self, terms):
		self.__class__.searchTerms = terms

	def GetSearchTerms(self):
		return self.__class__.searchTerms

def RegexMatch():
	""""""
	searchString = FilterTerms().GetSearchTerms()
	
	if(searchString != BLANK_TERM):
		# replace + with literal version
		pattern = re.compile('\+')
		searchString = pattern.sub('\+', searchString)
		
		pattern = re.compile('\(')
		searchString = pattern.sub('\(', searchString)
		
		pattern = re.compile('\)')
		searchString = pattern.sub('\)', searchString)
		
		pattern = re.compile('\/')
		searchString = pattern.sub('\/', searchString)
		
		pattern = re.compile('\!')
		searchString = pattern.sub('\!', searchString)
		
		pattern = re.compile('\?')
		searchString = pattern.sub('\?', searchString)
		
		pattern = re.compile('\.')
		searchString = pattern.sub('\.', searchString)
	else:
		searchString = "."

	return searchString

class Database():
	"""The Database object contains database meta data such as name, size, and location, 
	as well as methods for locating a database, arbitrating between several databases, 
	and checking database validity."""
	
	# static variables - will be populated by methods of this class
	fullName = ""
	newDb = False
			
	def Create(self):
		"""connects to a specific database"""
		# create all tables
		Base.metadata.create_all(engine)
		
		if 1 == self.newDb:
			print "creating blank database"
			self.InitBlankDb()
			self.__class__.newDb = False
		
	def InitBlankDb(self):
		"""This function is called during powerup to ensure that a database
		of the appropriate name exists. The object defined here will be discarded,
		but the database will remain."""
		
		session = SessionObject()
		print "Creating database: \n\t", Database().fullName, "\n\n"
		
		# create User table
		rhs = User(name='Rachel Sisco', shortName='Rachel')
		dls = User(name='Daniel Sisco', shortName='Dan')
		session.add_all([rhs, dls])
		session.commit()
		
		# create expenseType table
		clothing = ExpenseType(description='clothing!')
		makeup   = ExpenseType(description='makeup!')
		session.add_all([clothing, makeup])
		session.commit()
		
		# create demo expense table
		e1 = Expense(user=rhs, expenseType=makeup, amount='15.01', date=date.today(), description='makeup for mah FACE!')
		e2 = Expense(user=dls, expenseType=clothing, amount='50.25', date=date.today(), description='clothing for mah parts.')
		session.add_all([e1,e2])
		session.commit()
		
		# create dataSort table
		ds = DataSort(sortTerm1='date')
		session.add(ds)
		session.commit()
		
		# create version table
		v = Version(minor=dbVer[1], major=dbVer[0])
		session.add(v)
		session.commit()
		
		# create preference table
		colString = colInfo.defColWidth # pull default from grid.py
		p = Preference(frameHeight=300, frameWidth=900, colWidths=colString)
		session.add(p)
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
		
		try:
			e = session.query(Expense).filter(Expense.id==inputId).one()
			e.amount = amount
			e.description = desc
			e.date = date
			e.user_id = userId
			e.expenseType_id = typeId
		except NoResultFound:
			print "edit error"
			e = -1 
		
		session.commit()
		session.close()
		
	def DeleteExpense(self, deleteId):
		"""Removes an expense with the appropriate ID from the database"""
		session = SessionObject()
		e = session.query(Expense).filter(Expense.id==deleteId).one()
		session.delete(e)
		session.commit()
		session.close()	
	
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

		localSortTerm = self.GetSortTerm(1)
		filters = FilterTerms()
		
		# generate date objects for start and end dates
		startDate = date(2010, filters.GetStartMonth(), 1)
		temp = filters.GetStartMonth() + filters.GetMonthRange()
		
		# TODO: update this to work correctly with years
		if (temp <= 12):
			endDate = date(2010, temp, 1)
		else:
			endDate = date(2010, 12, 31)
		
		# grab all expenses
		expenseList = session.query(Expense).filter(Expense.date >= startDate). \
											 filter(Expense.date <= endDate).    \
											 order_by(localSortTerm).all()
			
		# compile regex match terms
		matchString = RegexMatch()
											 
		# iterate through expenses - packing into listxlist
		for i in expenseList:
			if(re.search(matchString, i.description)):
				minorList = [i.user.name, 
							i.expenseType.description, 
							str(i.amount), 
							str(i.date), 
							i.description, 
							i.id, 
							"delete"]
				majorList.append(minorList)
			
		session.close()
		
		return majorList		
	
	def GetUserList(self):
		"""Returns a list of the entire User object (name and shortName)"""
		list = []
		session = SessionObject()
		userList = session.query(User).order_by(User.name).all()
		for i in userList:
			list.append(i)
		session.close()
		return list
	
	def GetSimpleUserList(self):
		"""Returns a list of just the user name - like the name implies"""
		list = []
		session = SessionObject()
		userList = session.query(User).order_by(User.name).all()
		for i in userList:
			list.append(i.name)
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
		try:
			uId = session.query(User).filter(User.name==userName).one().id
		except NoResultFound:
			uId = -1
		session.close()
		return uId	
	
	def CreateUser(self, name, shortName):
		"""Creates a new user"""
		session = SessionObject()
		success = 0

		# ensure that type with this description does not already exist
		try:
			session.query(User).filter(User.name== name).one()
		except NoResultFound:
			u = User()
			u.name = name
			u.shortName = shortName
			session.add(u)
			session.commit()	
			success = 1
				
		session.close()
		return success
		
	def EditUser(self, name, shortName, inputId):
		session = SessionObject()
		u = session.query(User).filter(User.id == inputId).one()
		u.name = name
		u.shortName = shortName
		session.commit()
		session.close()	
		
	def DeleteUser(self, inputId):
		session = SessionObject()
		try:
			u = session.query(User).filter(User.id == inputId).one()
			session.delete(u)
			session.commit()
		except NoResultFound:
			print "record with id %s does not exist!" % inputId
		session.close			
		
	def UserInUse(self, typeId):
		"""returns the number of expenses using the user with the input ID"""
		session = SessionObject()
		cnt = len(session.query(Expense).filter(Expense.user_id == typeId).all())
		session.close
		return cnt	
	
	def GetExpenseTypeList(self):
		"""Returns a list of expense types - nothing else."""
		list = []
		session = SessionObject()
		typeList = session.query(ExpenseType).order_by(ExpenseType.description).all()
		for i in typeList:
			list.append(str(i.description))
		session.close()
		return list
	
	def GetExpenseType(self, desc):
		"""returns an ExpenseType object matching the typeName argument"""
		#TODO add fault handling here
		session = SessionObject()
		t = session.query(ExpenseType).filter(ExpenseType.description == desc).one()
		session.close()
		return t
	
	def GetExpenseTypeId(self, desc):
		"""returns an ExpenseType id matching the typeName argument"""
		#TODO add fault handling here
		session = SessionObject()
		try: 
			tId = session.query(ExpenseType).filter(ExpenseType.description==desc).one().id
		except NoResultFound:
			tId = -1
		session.close()
		return tId

	def CreateExpenseType(self, desc):
		"""Creates a new expense"""
		session = SessionObject()
		success = 0

		# ensure that type with this description does not already exist
		try:
			session.query(ExpenseType).filter(ExpenseType.description == desc).one()
		except NoResultFound:
			t = ExpenseType()
			t.description = desc
			session.add(t)
			session.commit()	
			success = 1
				
		session.close()
		return success
		
	def EditExpenseType(self, desc, inputId):
		session = SessionObject()
		et = session.query(ExpenseType).filter(ExpenseType.id == inputId).one()
		et.description = desc
		session.commit()
		session.close()	
		
	def DeleteExpenseType(self, inputId):
		session = SessionObject()
		try:
			et = session.query(ExpenseType).filter(ExpenseType.id == inputId).one()
			session.delete(et)
			session.commit()
		except NoResultFound:
			print "record with id %s does not exist!" % inputId
		session.close	
	
	def MigrateExpenseType(self, fromId, toId):
		"""migrates any expenses using expense type with ID 'fromId' to expense type 
		with ID 'toId'. Does nothing if no expenses are using expense type with Id
		'fromId'."""
		
	def ExpenseTypeInUse(self, typeId):
		"""returns the number of expenses using the expense type with the input ID"""
		session = SessionObject()
		cnt = len(session.query(Expense).filter(Expense.expenseType_id == typeId).all())
		session.close
		return cnt
	
	def SetName(self, name):
		self.__class__.fullName = name
		
	def FlagNewDb(self):
		self.__class__.newDb = True
		
	def EditPrefs(self, inputDefUserId, inputDefExpTypeId, inputDefAmount):
		session = SessionObject()
		
		# there should only be one preference entry in the table
		# otherwise the table is blank - create it
		try: 
			p = session.query(Preference).one()
		except NoResultFound:
			p = Preference()
			session.add(p)
			session.commit()
			
		p.defUser_id 		= inputDefUserId
		p.defExpenseType_id = inputDefExpTypeId
		p.defAmount         = inputDefAmount
		session.commit()
		session.close()
		
	def GetPrefs(self):
		session = SessionObject()
		
		# there should only be one preference entry in the table
		# otherwise the table is blank - create it
		try: 
			p = session.query(Preference).options(eagerload('defUser'), eagerload('defExpenseType')).one()
		except NoResultFound:
			p = Preference()
			session.add(p)
			session.commit()
			p = session.query(Preference).options(eagerload('defUser'), eagerload('defExpenseType')).one()
			
		session.close()
		return p
	
	def SetSortTerm(self, term, value):
		session = SessionObject()
		try:
			st = session.query(DataSort).one()
		except NoResultFound:
			st = DataSort()
			session.add(st)
			session.commit()
			st = session.query(DataSort).one()
		
		#TODO: support the other sort terms later
		if(term == 1):
			st.sortTerm1 = value
			session.commit()
		session.close()
		
	def GetSortTerm(self, term):
		session = SessionObject()
		try:
			localTerm = session.query(DataSort).one().sortTerm1
		except NoResultFound:
			localTerm = "date"
			
		session.close()
		return localTerm
		
	def GetVersion(self):
		session = SessionObject()
		v = session.query(Version).one()
		session.close()
		return (v.major, v.minor)
	
#********************************************************************
#					  DATABASE.PY CONTENT
#********************************************************************
connString = 'sqlite:///' + IdentifyDatabase()
engine = create_engine(connString, echo=False)
SessionObject = sessionmaker(bind=engine)

#********************************************************************
#							MAIN
#********************************************************************

# Test main functionality
if __name__ == '__main__':
	print "Please run Fin-ally by launching FINally.py!"