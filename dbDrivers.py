#!/usr/bin/env python

#********************************************************************
# Filename: 	dbDrivers.py
# Creator: 	Daniel Sisco
# Contributors: Daniel Sisco, Matt Van Kirk
# Date Created: 4-20-2007
# 
# Abstract: This is the Model/Controller component of the FINally SQLite finance tool.
# This file provides driver level functions for data manipulation that can be called
# by the FINally View component (Model-functionality). This file is also responsible
# for post processing and manipulating data before passing it back to the View
# (Controller-functionality).
#
# Version History:  See repository
#********************************************************************

import sqlite3
import re
from SQLiteCommands import *

database = 'dummy.db'
data = []
	
#********************************************************************	
def MCDeleteData(database, id):
	"""This function should accept an entry id and delete the data from the
	database at that location."""
	
	(cu, db) = LinkToDatabase(database)
	
	if(0 != id):
		# delete the id passed in
		temp = SQLDEF_DELETE % (id)
		cu.execute(temp)
	
	# commit and close database
	CommitChangesToDatabase(db)
	CloseDatabase(db)
	
#********************************************************************
def MCGetData(database, type, arg1, arg2, arg3):
	"""This function returns all data in the current database. The SQLite
	functions return data in the form of a 2-D tuple, which is immutable.
	We convert to a 2-D list, which is mutable data. This fcn also takes
	a 'range' argument which specifies if ALL data is required, or just a
	certain date range."""
	
	rawData = []
	
	# create database connection
	(cu, db) = LinkToDatabase(database)
	
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
	data = cu.fetchall()
	listData = list(data)
	
	# turn data from tuple into a list (more easily accessible)
	for i in listData:
		rawData.append(list(i))
		
	# format data for the View grid 
	# rtnData = ConvertDataToColumns(rawData)
	
	# close database
	CloseDatabase(db)
	
	return rawData

#********************************************************************
def MCInitDatabase(databaseName):
	"""This will create the appropriate tables inside the
	datbase specified via _databaseName_ if necessary. This should be the
	first function called from a View component that needs access to a certain
	database."""
	
	database = databaseName
	
	(cu, db) = LinkToDatabase(database)
	CreateDatabaseTables(cu)
	CommitChangesToDatabase(db)
	CloseDatabase(db)
	
#********************************************************************    
def MCInsertData(database, who, amount, date, desc):
	(cu, db) = LinkToDatabase(database)
	
	# TODO: check for pre-existing date/amount match, if no match, insert
	
	cu.execute(SQLDEF_INSERT_EXPENSES % (who, amount, date, desc))
	
	CommitChangesToDatabase(db)
	CloseDatabase(db)

#********************************************************************
def MCUpdateOne(database, target, newValue, id):
	(cu, db) = LinkToDatabase(database)
	
	test = SQLDEF_UPDATE % (target, newValue, id)
	cu.execute(test)
	
	CommitChangesToDatabase(db)
	CloseDatabase(db)

#********************************************************************
def CloseDatabase(db):
	db.close()
	
#********************************************************************
def CommitChangesToDatabase(db):
	db.commit()

#********************************************************************
def CreateDatabaseTables(cu):
	# create appropriate tables
	cu.execute(SQLDEF_EXPENSES)
	
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

# Test main functionality
if __name__ == '__main__':
	
	# EXAMPLE: Initialize database
	MCInitDatabase(database)

	# EXAMPLE: insert some data
	MCInsertData(database, 'rachel',1.11, '01012007', 'apple')
	MCInsertData(database, 'rachel',2.11, '01022007', 'bear')
	MCInsertData(database, 'rachel',3.11, '01032007', 'camel')
	MCInsertData(database, 'daniel',4.11, '01042007', 'beer')
	MCInsertData(database, 'daniel',5.11, '01052007', 'suit')
	MCInsertData(database, 'daniel',6.11, '01062007', 'elephant')

	# EXAMPLE: update one item
	MCUpdateOne(database, 'desc', 'jazz', 2)
	
	# EXAMPLE: get all data
	data = MCGetData(database, 1, -1, -1, -1)
	
	# EXAMPLE: get a range of data
	data = MCGetData(database, 2, "date > 1002007 AND date < 1042007", -1, -1)
	
	MCDeleteData(database, 1)
