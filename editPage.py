#!/usr/bin/env python

#********************************************************************
# Filename:        editPage.py
# Authors:         Daniel Sisco
# Date Created:    8-16-2010
# 
# Abstract: This is the primary file for the FINally expense analysis tool. It is responsible for
# handling read/write access to the SQLite database as well as providing a GUI interface for the user.
#
# Copyright 2008-2010 Daniel Sisco
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

# import wxPython libraries - including some simplifiers for grid and calendar
import wx
import wx.grid     as gridlib
import wx.calendar as callib
from datetime import date, datetime
from database import *

class UserColumnInfo:
    """This class defines the information required to create and modify columns in
    a grid. This keeps all columns definition data together, but adding information here
    does complete the addition of a new column."""
    
    # TODO: consolidate these into a dict or some other structure
    colLabels = ('user', 'id')
    colWidth  = [100, 50]
    colRO     = [1,1] # 0 = R/W, 1 = R
    colType   = [gridlib.GRID_VALUE_STRING,
                 gridlib.GRID_VALUE_STRING]
    
    rowHeight = 20

class TypeColumnInfo:
    """This class defines the information required to create and modify columns in
    a grid. This keeps all columns definition data together, but adding information here
    does complete the addition of a new column."""
    
    # TODO: consolidate these into a dict or some other structure
    colLabels = ('Expense Type', 'id')
    colWidth  = [100, 50]
    colRO     = [1,1] # 0 = R/W, 1 = R
    colType   = [gridlib.GRID_VALUE_STRING,
                 gridlib.GRID_VALUE_STRING]
    
    rowHeight = 20

#********************************************************************
class EditPage(wx.Panel):
    """The Edit page contains grids to display all the current User and Type objects,
    as well as allow operators to create new ones in the database"""
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.SetBackgroundColour("WHITE")
        
        # create User and Type grids and set column labels
        self.userGrid = SimpleUserGrid(self)
        self.typeGrid = SimpleTypeGrid(self)

        # create new user and new type button
        self.newUserButton = wx.Button(self,
                            id = -1,
                            label = "New User!",
                            pos = (0,0))
        self.Bind(wx.EVT_BUTTON, self.OnNewUserClick, self.newUserButton)
        
        self.newTypeButton = wx.Button(self,
                            id = -1,
                            label = "New Type!",
                            pos = (0,0))
        self.Bind(wx.EVT_BUTTON, self.OnNewTypeClick, self.newTypeButton)

        # BEGIN BOX SIZER SHENANIGANS
        self.sizer = wx.BoxSizer(wx.VERTICAL)
    
        self.sizer.Add(SampleWindow(self, ""), 1, wx.EXPAND) #top
    
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box2.Add(SampleWindow(self, ""), 1, wx.EXPAND)      #left
        userBox = wx.BoxSizer(wx.VERTICAL)
        userBox.AddMany([ (self.newUserButton, 0, wx.EXPAND),
                          (self.userGrid, 0, wx.EXPAND),
                        ])
        box2.Add(userBox, 0, wx.EXPAND)
        box2.Add(SampleWindow(self, ""), 1, wx.EXPAND)      # middle
        typeBox = wx.BoxSizer(wx.VERTICAL)
        typeBox.AddMany([ (self.newTypeButton,0, wx.EXPAND),
                          (self.typeGrid, 0, wx.EXPAND),
                        ])
        box2.Add(typeBox, 0, wx.EXPAND)
        box2.Add(SampleWindow(self, ""), 1, wx.EXPAND)      #right
    
        self.sizer.Add(box2, 0, wx.EXPAND)
    
        self.sizer.Add(SampleWindow(self, ""), 1, wx.EXPAND)#bottom
        
        self.SetSizer(self.sizer)
    
    def OnNewUserClick(self, evt):
        """fires when the new user button is clicked, this method creates a new user object"""
        dia = NewUserDialog(self, -1, 'Create New User')
        dia.ShowModal()
        dia.Destroy()
        evt.Skip()
        
    def OnNewTypeClick(self, evt):
        """fires when the new user button is clicked, this method creates a new user object"""
        dia = NewTypeDialog(self, -1, 'Create New Expense Type')
        dia.ShowModal()
        dia.Destroy()
        evt.Skip()
        
#********************************************************************
class NewTypeDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(350,300))
        
        # create a userlist and type list for the menus
        # NOTE: this must be done after the Database creation above
        # define local Expense objects for population
        self.database       = Database()
        self.typeList       = self.database.GetTypeList()
        
        self.parent = parent
        
        self.sizer        = wx.BoxSizer(wx.VERTICAL)  # define new box sizer    
        self.buttonPanel  = wx.Panel(self)              # create a panel for the buttons
        
        self.entryButton = wx.Button(self.buttonPanel,
                                    id = -1,
                                    label = "Enter!",
                                    pos = (0,0))
        self.Bind(wx.EVT_BUTTON, self.OnEnterClick, self.entryButton)
    
        # create and bind a description box
        self.typeEntry    = wx.TextCtrl(self.buttonPanel, 
                                        -1, 
                                        "Expense type", 
                                        pos = (100,25), 
                                        size = (173,21))
        self.Bind(wx.EVT_TEXT, self.OnTypeEntry, self.typeEntry)
        
        self.sizer.Add(self.buttonPanel, 0, wx.ALIGN_LEFT)    # add panel (no resize vert and aligned left horz)
        self.SetSizer(self.sizer)
        
    def OnEnterClick(self, evt):
        """respond to the user clicking 'enter!' by pushing the local objects into the database 
        layer"""
        
        # it's critical to create new database objects here
        localTypeObject    = ExpenseType()
        
        # if not evt.GetString() in self.userList:  
        localTypeObject.description = self.typeEntry.GetValue()
        
        # create new User in database
        self.database.CreateType(localTypeObject)
        self.parent.typeGrid.RefreshData()
        
        self.Close()
        
    #***************************
    # NOT REQUIRED AT THIS TIME
    #***************************
    
    def OnTypeEntry(self, evt):
        pass

#********************************************************************
class NewUserDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(350,300))
        
        # create a userlist and type list for the menus
        # NOTE: this must be done after the Database creation above
        # define local Expense objects for population
        self.database       = Database()
        self.userList       = self.database.GetUserList()
        
        self.parent = parent
        
        self.sizer        = wx.BoxSizer(wx.VERTICAL)  # define new box sizer    
        self.buttonPanel  = wx.Panel(self)              # create a panel for the buttons
        
        self.entryButton = wx.Button(self.buttonPanel,
                                    id = -1,
                                    label = "Enter!",
                                    pos = (0,0))
        self.Bind(wx.EVT_BUTTON, self.OnEnterClick, self.entryButton)
    
        # create and bind a description box
        self.nameEntry    = wx.TextCtrl(self.buttonPanel, 
                                        -1, 
                                        "User Name", 
                                        pos = (100,25), 
                                        size = (173,21))
        self.Bind(wx.EVT_TEXT, self.OnNameEntry, self.nameEntry)
        
        self.sizer.Add(self.buttonPanel, 0, wx.ALIGN_LEFT)    # add panel (no resize vert and aligned left horz)
        self.SetSizer(self.sizer)
        
    def OnEnterClick(self, evt):
        """respond to the user clicking 'enter!' by pushing the local objects into the database 
        layer"""
        
        # it's critical to create new database objects here
        localUserObject    = User()
        
        # if not evt.GetString() in self.userList:  
        localUserObject.name = self.nameEntry.GetValue()
        
        # create new User in database
        self.database.CreateUser(localUserObject)
        self.parent.userGrid.RefreshData()
        
        self.Close()
        
    #***************************
    # NOT REQUIRED AT THIS TIME
    #***************************
    
    def OnNameEntry(self, evt):
        pass

#********************************************************************
class SampleWindow(wx.PyWindow):
    """ A simple window that is used as sizer items in the tests below to
    show how the various sizers work."""
    def __init__(self, parent, text, pos=wx.DefaultPosition, size=wx.DefaultSize):
        wx.PyWindow.__init__(self, parent, -1)
        self.text = text
        if size != wx.DefaultSize:
            self.bestsize = size
        else:
            self.bestsize = (80,25)
        self.SetSize(self.GetBestSize())
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnPaint(self, evt):
        sz = self.GetSize()
        dc = wx.PaintDC(self)
        w,h = dc.GetTextExtent(self.text)
        dc.Clear()
        dc.DrawText(self.text, (sz.width-w)/2, (sz.height-h)/2)

    def OnSize(self, evt):
        self.Refresh()

#********************************************************************
class SimpleTypeGrid(gridlib.Grid):
    """This is a simple grid class - which means most of the methods are automatically
    defined by the wx library"""
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1, size=(250,300))
        self.CreateGrid(100,2)
        
        self.SetColLabelValue(0,"expense type")
        self.SetColLabelValue(1,"id")        
        
        # create a Database object and pull some data out of it
        self.database = Database()
        data = self.database.GetAllTypes()
        
        self.rowAttr = gridlib.GridCellAttr()
        self.CreateReadOnlyCols()        
        
        # push data into grid, line by line
        for i in range(len(data)):
            self.SetCellValue(i,0,str(data[i][0]))
            self.SetCellValue(i,1,str(data[i][1]))
            
        self.SetColSize(0,100)
        self.SetColSize(1,50)
        
    def RefreshData(self):
        data = self.database.GetAllTypes()
        
        # push data into grid, line by line
        for i in range(len(data)):
            self.SetCellValue(i,0,str(data[i][0]))
            self.SetCellValue(i,1,str(data[i][1]))
            
    def CreateReadOnlyCols(self):
        """creates read-only columns"""
        self.rowAttr.SetReadOnly(1)
        for i in range(len(TypeColumnInfo.colRO)):
            if TypeColumnInfo.colRO[i] == 1: 
                self.SetColAttr(i,self.rowAttr) 
        self.rowAttr.IncRef()             
        
#********************************************************************
class SimpleUserGrid(gridlib.Grid):
    """This is a simple grid class - which means most of the methods are automatically
    defined by the wx library"""
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1, size=(250,300))
        self.CreateGrid(25,2)
        
        self.SetColLabelValue(0,"user")
        self.SetColLabelValue(1,"id")
        
        # create a Database object and pull some data out of it
        self.database = Database()
        data = self.database.GetAllUsers()
        
        self.rowAttr = gridlib.GridCellAttr()
        self.CreateReadOnlyCols()
        
        # push data into grid, line by line
        for i in range(len(data)):
            self.SetCellValue(i,0,str(data[i][0]))
            self.SetCellValue(i,1,str(data[i][1]))
        
        self.SetColSize(0,100)
        self.SetColSize(1,50)
        
    def RefreshData(self):
        data = self.database.GetAllUsers()
        
        # push data into grid, line by line
        for i in range(len(data)):
            self.SetCellValue(i,0,str(data[i][0]))
            self.SetCellValue(i,1,str(data[i][1]))
            
    def CreateReadOnlyCols(self):
        """creates read-only columns"""
        self.rowAttr.SetReadOnly(1)
        for i in range(len(UserColumnInfo.colRO)):
            if UserColumnInfo.colRO[i] == 1: 
                self.SetColAttr(i,self.rowAttr) 
        self.rowAttr.IncRef() 