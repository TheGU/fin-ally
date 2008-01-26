#!/usr/bin/env python

#********************************************************************
# Filename: 	SQLiteCommands.py
# Authors:      Daniel Sisco
# Date Created: 1-23-2008
# 
# Abstract: The actual SQLite commands in string format. These can be
# quite lengthy and there are many of them, so we have pulled them into
# their own file.
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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#********************************************************************

#********************************************************************
# EXPENSE TABLE
#********************************************************************

# Used for creation of the base 'expenses' table
SQLDEF_EXPENSES = """
CREATE TABLE IF NOT EXISTS exp (
id INTEGER PRIMARY KEY,
who TEXT,
amount NUMBER,
date DATE,
desc TEXT
)
"""

# Used for deleting a specific record with matching id from table
# 'expenses'
SQLDEF_DELETE = """
DELETE FROM exp
WHERE %s = id
"""

# Used for inserting a complete record into 'expenses'
SQLDEF_INSERT_EXPENSES = """
INSERT INTO exp (who, amount, date, desc) 
VALUES ('%s', '%f', '%s', '%s')
"""

# Used for returning all records from 'expenses'
SQLDEF_GET_ALL = """
SELECT * from exp
"""

# Used for returning some records with certain criteria from 'expenses'
SQLDEF_GET_RANGE = """
SELECT * FROM exp
WHERE %s
"""

# Used for returning some values with certain criteria from 'expenses'
SQLDEF_GET_SOME = """
SELECT (%s) from exp
WHERE (%s)
"""

# Used for changing the value of some record from 'expenses'
SQLDEF_UPDATE = """
UPDATE exp
SET %s = '%s'
WHERE id = %s
"""

#********************************************************************
# USER INFO TABLE
#********************************************************************

# Used for creating the userInfo table in the database
SQLDEF_USER_INFO = """
CREATE TABLE IF NOT EXISTS userInfo (
id INTEGER PRIMARY KEY,
dbName TEXT,
creationDate DATE,
purpose TEXT,
version NUMBER
"""

# Used for inserting a complete record into 'userInfo' 
SQLDEF_INSERT_USER_INFO = """
INSERT INTO userInfo (dbName, creationDate, purpose, version) 
VALUES ('%s', '%s', '%s', '%f')
"""
