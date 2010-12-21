#!/usr/bin/env python

#********************************************************************
# Filename:            threads.py
# Authors:             Daniel Sisco
# Date Created:        12-22-2010
# 
# Abstract: provides common 'thread' classes for various FINally objects.
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

class ExpenseTypeThread():
    """This class supports global ExpenseType updates. It will execute every function
    present in the class variable refreshFuncList when the method RunRefreshFuncs is
    called. This class is intended to provide unified updates for all expenseType
    components when any modification to the underlying expenseType objects are made."""
    
    refreshFuncList = []
    
    def StoreRefreshFunc(self, func):
        self.__class__.refreshFuncList.append(func)
        
    def ClearRefreshFuncList(self):
        self.__class__.refreshFuncList = []
        
    def RunRefreshFuncs(self):
        for i in self.__class__.refreshFuncList:
            i() # actually execute the function