#*******************************************************************************************************
# Filename: SQLite_drivers.py
# Author: Daniel Sisco, Matt Van Kirk
# Date Created: 4-20-2008
# 
# Abstract: This is the Model/Controller component of the FINally SQLite finance tool. This file provides driver
# level functions for data manipulation that can be called by the FINally View component (Model-functionality). This
# file is also responsible for post processing and manipulating data before passing it back to the View
# (Controller-functionality). 
#*******************************************************************************************************

import sqlite3
import re

#********************************************************************
database = 'dummy.db'
data = []

#********************************************************************
SQLDEF_EXPENSES = """
CREATE TABLE IF NOT EXISTS exp (
id INTEGER PRIMARY KEY,
who TEXT,
amount NUMBER,
date DATE,
desc TEXT
)
"""
SQLDEF_DELETE = """
DELETE FROM exp
WHERE %s = id
"""
SQLDEF_INSERT_EXPENSES = """
INSERT INTO exp (who, amount, date, desc) 
VALUES ('%s', '%f', '%s', '%s')
"""
SQLDEF_GET_ALL = """
SELECT * from exp
"""
SQLDEF_GET_RANGE = """
SELECT * FROM exp
WHERE %s
"""
SQLDEF_GET_SOME = """
SELECT (%s) from exp
WHERE (%s)
"""
SQLDEF_UPDATE = """
UPDATE exp
SET %s = '%s'
WHERE id = %s
"""

#*******************************************************************************************************
#					    GLOBAL FUNCTIONS
#*******************************************************************************************************
	
#********************************************************************
# MCDeleteData
#
# This function should accept an entry id and delete the data from the
# database at that location.
#********************************************************************	
def MCDeleteData(database, id):
	(cu, db) = LinkToDatabase(database)
	
	if(0 != id):
		# delete the id passed in
		temp = SQLDEF_DELETE % (id)
		cu.execute(temp)
	
	# commit and close database
	CommitChangesToDatabase(db)
	CloseDatabase(db)
	
#********************************************************************
# MCGetData
#
# This function returns all data in the current database. The SQLite
# functions return data in the form of a 2-D tuple, which is immutable.
# We convert to a 2-D list, which is mutable data. This fcn also takes
# a 'range' argument which specifies if ALL data is required, or just a
# certain date range.
#********************************************************************
def MCGetData(database, type, arg1, arg2, arg3):
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
# MCInitDatabase - this will create the appropriate tables inside the
# datbase specified via _databaseName_ if necessary. This should be the
# first function called from a View component that needs access to a certain
# database.
#********************************************************************
def MCInitDatabase(databaseName):
	database = databaseName
	
	(cu, db) = LinkToDatabase(database)
	CreateDatabaseTables(cu)
	CommitChangesToDatabase(db)
	CloseDatabase(db)
	
#********************************************************************
# MCInsertData - accepts data to insert into the EXPENSES table.
#********************************************************************    
def MCInsertData(database, who, amount, date, desc):
	(cu, db) = LinkToDatabase(database)
	
	# TODO: check for pre-existing date/amount match, if no match, insert
	
	cu.execute(SQLDEF_INSERT_EXPENSES % (who, amount, date, desc))
	
	CommitChangesToDatabase(db)
	CloseDatabase(db)

#********************************************************************
# MCUpdateOne - for entries matching 'id', this fcn replaces value of
# 'target' with 'newValue'
#********************************************************************
def MCUpdateOne(database, target, newValue, id):
	(cu, db) = LinkToDatabase(database)
	
	test = SQLDEF_UPDATE % (target, newValue, id)
	cu.execute(test)
	
	CommitChangesToDatabase(db)
	CloseDatabase(db)

#*******************************************************************************************************
#					    LOCAL FUNCTIONS
#*******************************************************************************************************

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
#
# LinkToDatabase
#
# This function will try to link to an existing database, and will create
# such a database is none exists. The single argument is the name of the
# database it is searching for.
#
#********************************************************************
def LinkToDatabase(database):
	# create global instance of database
	try:
		db = sqlite3.connect(database)
	except sqlite3.Error, errmsg:
		print "Could not open the database file: " + str(errmsg)
		sys.exit()
	
	cu = db.cursor()
	return cu, db

#*******************************************************************************************************
#                                            TEST MAIN 
#*******************************************************************************************************

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
