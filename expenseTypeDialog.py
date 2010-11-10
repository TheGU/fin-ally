#!/usr/bin/env python

#********************************************************************
# Filename:            expenseTypeDialog.py
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
from datetime import date, datetime
from database import *

#********************************************************************
class TypeColumnInfo:
    """This class defines the information required to create and modify columns in
    a grid. This keeps all columns definition data together, but adding information here
    does complete the addition of a new column."""
    
    colLabels = ('Expense Type')
    colWidth  = [100]
    colRO     = [0] # 0 = R/W, 1 = R
    colType   = [gridlib.GRID_VALUE_STRING]
    
    rowHeight = 20
    
#********************************************************************
class SimpleTypeGrid(gridlib.Grid):
    """This is a simple grid class - which means most of the methods are automatically
    defined by the wx library"""
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1, size=(200,300))
        self.CreateGrid(100,1)
        
        self.SetColLabelValue(0,"expense type")       
        
        # create a Database object and pull some data out of it
        self.database = Database()
        data = self.database.GetExpenseTypeList()
        
        self.currentValue = ""
        
        self.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange)
        self.Bind(gridlib.EVT_GRID_EDITOR_SHOWN, self.OnEditorShown)
        
        self.rowAttr = gridlib.GridCellAttr()
        self.CreateReadOnlyCols()        
        
        # push data into grid, line by line
        for i in range(len(data)):
            self.SetCellValue(i,0,str(data[i]))
            
        self.SetColSize(0,100)
        
    def OnCellChange(self, evt):
        """Using a class variable that stores the previous ExpenseType description,
        this method edits the ExpenseType table in the database"""
        value = self.GetCellValue(evt.GetRow(), evt.GetCol())
        
        # pull ID of the ExpenseType of interest and then edit the ExpenseType of that ID
        etId = self.database.GetExpenseTypeId(self.currentValue)
        self.database.EditExpenseType(value, etId)

        evt.Skip()
        
    def OnEditorShown(self, evt):
        """This method stores the current value into a class variable before
        the user attempts to edit. This allows us to look-up ExpenseType id
        by the 'old description' before the user changes it"""
        self.currentValue = self.GetCellValue(evt.GetRow(), evt.GetCol())
        evt.Skip()        
        
    def RefreshData(self, delete=0):
        """The delete argument removes one row from the top of the simple grid.
        There is currently no way to delete more than one row at a time, so this
        is safe."""
        if(delete == 1):
            # remove the last row
            self.DeleteRows(0,1)
        
        # push data into grid, line by line
        data = self.database.GetExpenseTypeList()
        for i in range(len(data)):
            self.SetCellValue(i,0,str(data[i]))
            
    def CreateReadOnlyCols(self):
        """creates read-only columns"""
        self.rowAttr.SetReadOnly(1)
        for i in range(len(TypeColumnInfo.colRO)):
            if TypeColumnInfo.colRO[i] == 1: 
                self.SetColAttr(i,self.rowAttr) 
        self.rowAttr.IncRef()       

#********************************************************************
class expenseTypeDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: expenseTypeDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        #**** BEGIN ADD ****
        self.database = Database()
        self.expenseTypeChoices = self.database.GetExpenseTypeList()
        self.newTypeText = "new type description..."
        
        self.deleteSizer_staticbox = wx.StaticBox(self, -1, "Delete Existing Types")
        self.newTypeSizer_staticbox = wx.StaticBox(self, -1, "Add New Types")
        self.editSizer_staticbox = wx.StaticBox(self, -1, "Edit Existing Types")
        #**** MOD ****
        self.expenseTypeGrid = SimpleTypeGrid(self)
        self.expenseTypeEditToggle = wx.ToggleButton(self, -1, "edit expense types...")
        #*** MOD ***
        self.deleteComboBox = wx.ComboBox(self, 
                                          -1, 
                                          self.expenseTypeChoices[0], #default
                                          choices=self.expenseTypeChoices, 
                                          style=wx.CB_DROPDOWN)
        self.deleteButton = wx.Button(self, -1, "delete")
        self.newExpenseTypeEntry = wx.TextCtrl(self, -1, self.newTypeText)
        self.addButton = wx.Button(self, -1, "add")

        self.__set_properties()
        self.__do_layout()
        
        #**** ADDED ****
        self.Bind(wx.EVT_BUTTON, self.onDeleteButton, self.deleteButton)
        self.Bind(wx.EVT_BUTTON, self.onAddButton, self.addButton)
        #**** END ADD ****
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: expenseTypeDialog.__set_properties
        self.SetTitle("Expense Type Dialog")
        #**** MOD ****
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: expenseTypeDialog.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        newTypeSizer = wx.StaticBoxSizer(self.newTypeSizer_staticbox, wx.VERTICAL)
        innerNewTypeSizer = wx.BoxSizer(wx.HORIZONTAL)
        deleteSizer = wx.StaticBoxSizer(self.deleteSizer_staticbox, wx.VERTICAL)
        innerDeleteSizer = wx.BoxSizer(wx.HORIZONTAL)
        editSizer = wx.StaticBoxSizer(self.editSizer_staticbox, wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        sizer_8.Add(self.expenseTypeGrid, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_8.Add(self.expenseTypeEditToggle, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        editSizer.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_2.Add(editSizer, 1, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5)
        innerDeleteSizer.Add(self.deleteComboBox, 1, wx.RIGHT|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        innerDeleteSizer.Add(self.deleteButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        deleteSizer.Add(innerDeleteSizer, 1, wx.EXPAND, 0)
        sizer_2.Add(deleteSizer, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5)
        innerNewTypeSizer.Add(self.newExpenseTypeEntry, 1, wx.RIGHT|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        innerNewTypeSizer.Add(self.addButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        newTypeSizer.Add(innerNewTypeSizer, 1, wx.EXPAND, 0)
        sizer_2.Add(newTypeSizer, 0, wx.ALL|wx.EXPAND, 5)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade
        
    #**** ADDED ****
    
    def onAddButton(self, event):
        """triggers when the add button is clicked in the expense type dialog. This function
        determines if conditions are correct for a new expense type entry and creates that type"""
        localText = self.newExpenseTypeEntry.GetValue()
        if(localText != self.newTypeText):
            # create new entry
            success = self.database.CreateExpenseType(localText)
            # reset text in text entry box
            self.newExpenseTypeEntry.SetValue(self.newTypeText)
            # refresh Grid
            self.expenseTypeGrid.RefreshData()
            
            if success:
                # refresh comboBox choices and add new entry
                self.expenseTypeChoices = self.database.GetExpenseTypeList()
                self.deleteComboBox.Append(localText)
        else:
            print "please enter a new expense type description!"
        event.Skip()
    
    def onDeleteButton(self, event):
        """triggered when the delete button is clicked in the expense type dialog. This function
        either processes the deletion of a particular type entry, or informs the user
        that a deletion is not possible at this time.
        
        TODO: trigger another dialog to allow the user to specify a 'transfer to' type 
        before deleting an expense type record that is in use."""
        if(self.expenseTypeEditToggle.GetValue()):
            typeToDelete = self.deleteComboBox.GetValue()
            IdxToDelete  = self.deleteComboBox.GetSelection()
            localId      = self.database.GetExpenseTypeId(typeToDelete)
            
            if(self.database.ExpenseTypeInUse(localId)):
                # TODO: prompt user for new expenseType to apply using MigrateExpenseType
                print "there are %s expenses using this type!" % (self.database.ExpenseTypeInUse(localId)) 
            else:
                # look up type via description, get ID, delete from db
                print "deleting %s at position %s" % (typeToDelete, IdxToDelete)
                
                # remove from ComboBox
                self.deleteComboBox.Delete(self.deleteComboBox.GetSelection())
                
                localId = self.database.GetExpenseTypeId(typeToDelete)
                self.database.DeleteExpenseType(localId)
                
                # refresh Grid with delete option activated
                self.expenseTypeGrid.RefreshData(delete=1)
        else:
            #TODO: open a dialoge to say this
            print "you must unlock the grid before deleting"
        event.Skip()
    
    #**** END ADD ****
