#!/usr/bin/env python

#********************************************************************
# Filename:            schema_2_1.py
# Authors:             Daniel Sisco
# Date Created:        10/10/2010
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
from sqlmigratelite.migrate import MigrateObject
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, eagerload
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()
version = "2.1"
dbVer = (2,1)

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
    expenseType    = relationship(ExpenseType, backref=backref('expenses', order_by=id))
    
    def __repr__(self):
        return "<Expense('%s', '%s', '%s')>" % (self.amount, self.date, self.description)
    
#********************************************************************
class Preference(Base):
    __tablename__ = 'preferences'
    
    id          = Column(Integer, primary_key=True)
    defUser_id  = Column(Integer, ForeignKey('users.id')) 
    defUser     = relationship(User, backref=backref('preferences', order_by=id))
    defExpenseType_id = Column(Integer, ForeignKey('expenseTypes.id'))
    defExpenseType    = relationship(ExpenseType, backref=backref('preferences', order_by=id))
    defAmount   = Column(Integer)
    
    def __repr__(self):
        return "<Preference('%s, %s, %s')>" % (self.defUser_id, self.defExpenseType_id, self.defAmount)

#********************************************************************
class DataSort(Base):
    __tablename__ = 'dataSort'
    
    id          = Column(Integer, primary_key=True)
    sortTerm1   = Column(String)
    sortTerm2   = Column(String)
    sortTerm3   = Column(String)
    sortTerm4   = Column(String)
    sortTerm5   = Column(String)
    
    def __repr__(self):
        return "<DataSort('%s, %s, %s, %s, %s')>" % (self.sortTerm1, 
                                                     self.sortTerm2, 
                                                     self.sortTerm3, 
                                                     self.sortTerm4, 
                                                     self.sortTerm5)

#********************************************************************    
class Version(Base):
    __tablename__ = 'versions'
    id = Column(Integer, primary_key=True)
    minor = Column(Integer)
    major = Column(Integer)
    
    def __repr__(self):
        return "<Version('%s', '%s')>" % (self.minor, self.major)
    
#************************************
class SchemaObject(MigrateObject):
    """
    version 2.1 schema object - defines custom dumpContent and loadContent methods
    """
    def __init__(self, dbPath):
        MigrateObject.__init__(self, dbPath, version)
        
    def dumpContent(self):
        """dumps User and Version tables as-is"""
        self.localDict['User'] = self.session.query(User).all()
        self.localDict['ExpenseType'] = self.session.query(ExpenseType).all()
        self.localDict['Expense'] = self.session.query(Expense).all()
        self.localDict['Preference'] = self.session.query(Preference).all()
        self.localDict['DataSort'] = self.session.query(DataSort).all()
        
    def loadContent(self):
        Base.metadata.create_all(self.engine)
        
        for i in self.localDict['User']:
            u = User()
            u.name = i.name
            u.shortName = i.shortName
            self.session.add(u)
            self.session.commit()
        for i in self.localDict['ExpenseType']:
            t = ExpenseType()
            t.description = i.description
            self.session.add(t)
            self.session.commit()
        for i in self.localDict['Expense']:
            e = Expense()
            e.user_id = i.user_id
            e.expenseType_id = i.expenseType_id
            e.amount = i.amount
            e.date = i.date
            e.description = i.description
            self.session.add(e)
            self.session.commit()
        for i in self.localDict['Preference']:
            p = Preference()
            p.defUser_id = i.defUser_id
            p.defExpenseType_id = i.defExpenseType_id
            p.defAmount = i.defAmount
            self.sesion.add(p)
            self.session.commit()
        # update the version number
        # TODO: move this into sqlmigratelite core
        v = Version(minor=dbVer[1], major=dbVer[0])
        self.session.add(v)
        self.session.commit()