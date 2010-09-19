#!/usr/bin/env python

#********************************************************************
# Filename:            schema_1_0.py
# Authors:             Daniel Sisco
# Date Created:        9/19/2010
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
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

Base = declarative_base()
version = "1.0"
dbVer = (1,0)

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

#********************************************************************    
class Version(Base):
    __tablename__ = 'versions'
    id = Column(Integer, primary_key=True)
    minor = Column(Integer)
    major = Column(Integer)
    
    def __repr__(self):
        return "<Version('%s', '%s')>" % (self.minor, self.major)