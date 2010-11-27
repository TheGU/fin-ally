#!/usr/bin/env python

#********************************************************************
# Filename:            userDialog.py
# Authors:             Daniel Sisco
# Date Created:        11/5/2010
# 
# Abstract: This files contains the user add/edit/delete dialog.
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
import wx.calendar as callib
import wx.grid     as gridlib
import cfg
import os
from   datetime import date, datetime
from   database import *

#********************************************************************
class UserColumnInfo:
    """This class defines the information required to create and modify columns in
    a grid. This keeps all columns definition data together, but adding information here
    does complete the addition of a new column."""
    
    colLabels = ('user', 'short')
    colWidth  = [100, 50]
    colRO     = [0, 0] # 0 = R/W, 1 = R
    colType   = [gridlib.GRID_VALUE_STRING,
                 gridlib.GRID_VALUE_STRING]  
    rowHeight = 20
    
#********************************************************************
class SimpleUserGrid(gridlib.Grid):
    """This is a simple grid class - which means most of the methods are automatically
    defined by the wx library"""
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1, size=(250,300))
        self.CreateGrid(25,2)
        
        # apply column labels
        for i in range(len(UserColumnInfo.colLabels)):
            self.SetColLabelValue(i, UserColumnInfo.colLabels[i])
        
        # apply columns width    
        for i in range(len(UserColumnInfo.colWidth)):
            self.SetColSize(i, UserColumnInfo.colWidth[i])
        
        # create a Database object and pull some data out of it
        self.database = Database()
        data = self.database.GetUserList()
        
        self.oldNameValue = ""
        
        self.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange)
        self.Bind(gridlib.EVT_GRID_EDITOR_SHOWN, self.OnEditorShown)
        
        self.rowAttr = gridlib.GridCellAttr()
        self.CreateReadOnlyCols()
        
        # push data into grid, line by line
        for i in range(len(data)):
            self.SetCellValue(i,0,str(data[i].name))
            self.SetCellValue(i,1,str(data[i].shortName))
        
    def OnCellChange(self, evt):
        """Using a class variable that stores the previous ExpenseType description,
        this method edits the ExpenseType table in the database"""
        
        # new value and ID are the same for both columns    
        newValue = self.GetCellValue(evt.GetRow(), evt.GetCol())
        uId = self.database.GetUserId(self.oldNameValue)
            
        if 0 == evt.GetCol():
            self.database.EditUser(newValue, self.GetCellValue(evt.GetRow(), evt.GetCol()+1), uId)
        else:
            self.database.EditUser(self.GetCellValue(evt.GetRow(), evt.GetCol()-1), newValue, uId)
            
        evt.Skip()
        
    def OnEditorShown(self, evt):
        """This method stores the current value into a class variable before
        the user attempts to edit. This allows us to look-up ExpenseType id
        by the 'old description' before the user changes it"""
        if 0 == evt.GetCol():
            self.oldNameValue = self.GetCellValue(evt.GetRow(), evt.GetCol())
        else:
            self.oldNameValue = self.GetCellValue(evt.GetRow(), evt.GetCol()-1)
        evt.Skip()         
            
    def RefreshData(self, delete=0):
        """The delete argument removes one row from the top of the simple grid.
        There is currently no way to delete more than one row at a time, so this
        is safe."""
        if(delete == 1):
            # remove the last row
            self.DeleteRows(0,1)
        
        # push data into grid, line by line
        data = self.database.GetUserList()
        for i in range(len(data)):
            self.SetCellValue(i,0,str(data[i].name))
            self.SetCellValue(i,1,str(data[i].shortName))         
            
    def CreateReadOnlyCols(self):
        """creates read-only columns"""
        self.rowAttr.SetReadOnly(1)
        for i in range(len(UserColumnInfo.colRO)):
            if UserColumnInfo.colRO[i] == 1: 
                self.SetColAttr(i,self.rowAttr) 
        self.rowAttr.IncRef()      

#********************************************************************
class userDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: userDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        #**** BEGIN ADD ****
        self.database = Database()
        self.userChoices = self.database.GetSimpleUserList()
        self.newUserFullName  = "new user full name..."
        self.newUserShortName = "new user short name..."
        
        self.deleteSizer_staticbox = wx.StaticBox(self, -1, "Delete Existing Users")
        self.newTypeSizer_staticbox = wx.StaticBox(self, -1, "Add New Users")
        self.editSizer_staticbox = wx.StaticBox(self, -1, "Edit Existing Users")
        
        #**** MOD ****
        self.userGrid = SimpleUserGrid(self)
        self.userEditToggle = wx.ToggleButton(self, -1, "edit users...")
        
        #*** MOD ***
        self.deleteComboBox = wx.ComboBox(self, 
                                          -1, 
                                          self.userChoices[0], #default
                                          choices=self.userChoices, 
                                          style=wx.CB_DROPDOWN)
        self.deleteButton = wx.Button(self, -1, "delete")
        self.shortNameEntry = wx.TextCtrl(self, -1, "new user short name...")
        self.addButton = wx.Button(self, -1, "add")
        self.nameEntry = wx.TextCtrl(self, -1, "new user full name...")

        self.__set_properties()
        self.__do_layout()
        
        #**** ADDED ****
        self.Bind(wx.EVT_BUTTON, self.onDeleteButton, self.deleteButton)
        self.Bind(wx.EVT_BUTTON, self.onAddButton, self.addButton)
        #**** END ADD ****
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: userDialog.__set_properties
        self.SetTitle("User Dialog")
        #**** MOD ****

        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: userDialog.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        newTypeSizer = wx.StaticBoxSizer(self.newTypeSizer_staticbox, wx.VERTICAL)
        innerNameSizer = wx.BoxSizer(wx.HORIZONTAL)
        innerShortNameSizer = wx.BoxSizer(wx.HORIZONTAL)
        deleteSizer = wx.StaticBoxSizer(self.deleteSizer_staticbox, wx.VERTICAL)
        innerDeleteSizer = wx.BoxSizer(wx.HORIZONTAL)
        editSizer = wx.StaticBoxSizer(self.editSizer_staticbox, wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        sizer_8.Add(self.userGrid, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_8.Add(self.userEditToggle, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        editSizer.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_2.Add(editSizer, 1, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5)
        innerDeleteSizer.Add(self.deleteComboBox, 1, wx.RIGHT|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        innerDeleteSizer.Add(self.deleteButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        deleteSizer.Add(innerDeleteSizer, 1, wx.EXPAND, 0)
        sizer_2.Add(deleteSizer, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5)
        innerShortNameSizer.Add(self.shortNameEntry, 1, wx.RIGHT|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        innerShortNameSizer.Add(self.addButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        newTypeSizer.Add(innerShortNameSizer, 1, wx.EXPAND, 0)
        innerNameSizer.Add(self.nameEntry, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        newTypeSizer.Add(innerNameSizer, 1, wx.TOP|wx.EXPAND, 3)
        sizer_2.Add(newTypeSizer, 0, wx.ALL|wx.EXPAND, 5)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade
        
    #**** ADDED ****
    
    def onAddButton(self, event):
        """triggers when the add button is clicked in the user dialog. This function
        determines if conditions are correct for a new user entry and creates that user"""
        
        localName      = self.nameEntry.GetValue()
        localShortName = self.shortNameEntry.GetValue()
        
        if(    localName != self.newUserFullName
           and localShortName != self.newUserShortName):
            # create new entry
            success = self.database.CreateUser(localName, localShortName)
            # reset text in text entry box
            self.nameEntry.SetValue(self.newUserFullName)
            self.shortNameEntry.SetValue(self.newUserShortName)
            # refresh Grid
            self.userGrid.RefreshData()
            
            if success:
                # refresh comboBox choices and add new entry
                self.userChoices = self.database.GetUserList()
                self.deleteComboBox.Append(localName)
        else:
            print "please enter user information!"
        event.Skip()
    
    def onDeleteButton(self, event):
        """triggered when the delete button is clicked in the user dialog. This function
        either processes the deletion of a particular user entry, or informs the user
        that a deletion is not possible at this time.
        
        TODO: trigger another dialog to allow the user to specify a 'transfer to' user
        before deleting a user record that is in use."""
        if(self.userEditToggle.GetValue()):
            typeToDelete = self.deleteComboBox.GetValue()
            IdxToDelete  = self.deleteComboBox.GetSelection()
            localId      = self.database.GetUserId(typeToDelete)
            
            if localId != -1:
                if(self.database.UserInUse(localId)):
                    # TODO: prompt user for new expenseType to apply using MigrateExpenseType
                    print "there are %s expenses using this user!" % (self.database.UserInUse(localId)) 
                else:
                    # look up type via description, get ID, delete from db
                    print "deleting %s at position %s" % (typeToDelete, IdxToDelete)
                    
                    # remove from ComboBox
                    self.deleteComboBox.Delete(IdxToDelete)
                    
                    localId = self.database.GetUserId(typeToDelete)
                    self.database.DeleteUser(localId)
                    
                    # refresh Grid with delete option activated
                    self.userGrid.RefreshData(delete=1)
            else:
                print "user %s doesn't seem to exist anymore, close dialog and try again" % (typeToDelete)      
        else:
            #TODO: open a dialoge to say this
            print "you must unlock the grid before deleting"
        event.Skip()
    
    #**** END ADD ****
