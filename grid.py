#!/usr/bin/env python

#********************************************************************
# Filename:            FINally.py
# Authors:         Daniel Sisco
# Date Created:       4-20-2007
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
import cfg
from datetime import date, datetime
from database import *

#********************************************************************    
class columnInfo:
    """This class defines the information required to create and modify columns in
    a grid. This keeps all columns definition data together, but adding information here
    does complete the addition of a new column."""
    
    # TODO: consolidate these into a dict or some other structure
    colLabels = ('user', 'type', 'amount', 'date', 'desc', 'id', 'del')
    colWidth  = [100, 50, 50, 200, 300, 50, 50]
    colRO     = [0,0,0,0,0,1,0] # 0 = R/W, 1 = R
    colType   = [gridlib.GRID_VALUE_CHOICE,
                  gridlib.GRID_VALUE_CHOICE,
                  gridlib.GRID_VALUE_NUMBER,
                  gridlib.GRID_VALUE_STRING, # should be GRID_VALUE_DATETIME
                  gridlib.GRID_VALUE_STRING,
                  gridlib.GRID_VALUE_NUMBER,
                  gridlib.GRID_VALUE_STRING]
    
    rowHeight = 20
    
# create global instances of classes
colInfo = columnInfo()

#********************************************************************        
class GraphicsGrid(gridlib.Grid):
    """
    Class Name:     GraphicsGrid
    Extends:        wx.grid.Grid (gridlib.Grid)
    Description:    This class is responsible for grid format and operator event binding
    such as right-clicking the grid or creating an editor while changing a cell. This
    class does not manage data directly, and instead uses a table base member for data
    management.
    """

    #TODO: determine how much control to give this over the data we want to see. Consider adding
    #another class for the data itself, a class that would be passed to everything and modified
    #in many places. This would allow a future calculation object to make changes and force them
    #to show up in the graphics page.
        
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent)
        
        # pull some data out of the database and push it into the tableBase
        self.database = Database()
        self.tableBase = CustomDataTable(self,self.database.GetAllExpenses())    # define the base
        
        self.SetTable(self.tableBase)         # set the grid table
        self.SetColFormatFloat(2,-1,2)        # formats the monetary entries correctly
        self.AutoSize()         # auto-sizing here ensures that scrollbars will always be present
                                # during window resizing
        
        # Make certain cols read only
        self.rowAttr = gridlib.GridCellAttr()
        self.InitialTableFormat()

        # bind editor creation to an event so we can 'catch' unique editors
        self.Bind(gridlib.EVT_GRID_EDITOR_CREATED,
                  self.OnGrid1GridEditorCreated)
        
        # bind grid-based context menu if active
        if cfg.GRID_CONTEXT_MENU == 1:
            self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.onGridRightClick)
        
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.onGridClick)
        
    def onGridClick(self, event):
        if(event.GetCol() == 6):
            self.tableBase.DeleteRow(event.GetRow())
        event.Skip()

    def onGridRightClick(self, event):
        if cfg.GRID_CONTEXT_MENU == 1:
            # highlight the grid row in red
            row = event.GetRow()
            attr = gridlib.GridCellAttr()
            attr.SetBackgroundColour(wx.RED)
            self.SetRowAttr(row, attr)
            self.ForceRefresh()
            
            # only do this part the first time so the events are only bound once
            #
            # Yet another alternate way to do IDs. Some prefer them up top to
            # avoid clutter, some prefer them close to the object of interest
            # for clarity. 
            if not hasattr(self, "popupDeleteId"):
                self.popupDeleteId = wx.NewId()
    
            # use of lambda functions prevent two new methods
            self.Bind(wx.EVT_MENU, lambda evt, temp=row: self.OnPopupDelete(evt, temp), id=self.popupDeleteId)
    
            # create a menu and pack it some some options
            menu = wx.Menu()
            menu.Append(self.popupDeleteId, "Delete")
    
            self.PopupMenu(menu)
            menu.Destroy()
        else:
            event.Skip

    def OnPopupDelete(self, event, row):
        if cfg.GRID_CONTEXT_MENU == 1:
            # delete the current row
            # TODO: add a #define here or something
            self.tableBase.DeleteRow(row)
        else:
            event.Skip()

    def OnGrid1GridEditorCreated(self, event):
        """This function will fire when a cell editor is created, which seems to be 
        the first time that cell is edited (duh). Standard columns will be left alone 
        in this method, but unique columns (ie: comboBoxes) will be set explicitly."""
        
        Row = event.GetRow()
        Col = event.GetCol()

        # Col 0 is the User object column
        if Col == 0:
            #Get a reference to the underlying ComboBox control.
            self.comboBox = event.GetControl()
            
            #Bind the ComboBox events.
            self.comboBox.Bind(wx.EVT_COMBOBOX, self.ComboBoxSelection)
            
            # load combo box with all user types
            for i in self.database.GetSimpleUserList():
                self.comboBox.Append(i)
                
        # Col 1 is the Expense Type object column
        elif Col == 1:
            self.comboBox = event.GetControl()
            self.comboBox.Bind(wx.EVT_COMBOBOX, self.ComboBoxSelection)
            for i in self.database.GetExpenseTypeList():
                self.comboBox.Append(i)
        
    def ComboBoxSelection(self, event):
        """This method fires when the underlying ComboBox object is done with
        it's selection"""

        # DAN: is this code useless? It seems like it is...
        value       = self.comboBox.GetValue()
        selection = self.comboBox.GetSelection()
        pass
        
    def InitialTableFormat(self):
        """Performs initial table configuration, """

        # create read-only columns        
        self.rowAttr.SetReadOnly(1)
        for i in range(len(colInfo.colRO)):
            if colInfo.colRO[i] == 1: 
                self.SetColAttr(i,self.rowAttr) 
        self.rowAttr.IncRef() 
        
        # apply editors and row height to each row
        for i in range(self.GetNumberRows()):
            self.FormatTableRow(i)
            
        # format column width
        tmp = 0
        for i in colInfo.colWidth:
            self.SetColSize(tmp,i)
            tmp += 1
            
    def FormatTableRow(self, row):
        """Formats a single row entry - editor types, height, color, etc..."""
        # create 'drop down' style choice editors for two columns
        userChoiceEditor = gridlib.GridCellChoiceEditor([], allowOthers = False)
        typeChoiceEditor = gridlib.GridCellChoiceEditor([], allowOthers = False)
        
        self.SetCellEditor(row,0,userChoiceEditor)
        self.SetCellEditor(row,1,typeChoiceEditor)
        self.SetCellEditor(row,2,gridlib.GridCellFloatEditor(-1,2))
        
        self.SetRowSize(row, colInfo.rowHeight)
        
        self.SetCellBackgroundColour(row,6,"GREEN")

#********************************************************************        
class CustomDataTable(gridlib.PyGridTableBase):
    """
    Class Name:     CustomDataTable
    Extends:        wx.grid.PyGridTableBase (gridlib.PyGridTableBase)
    Description:    An instance of the uninstantiated base class PyGridTableBase. This instance
    must contain several methods (listed below) for modifying/viewing/querying data in the grid.
    As well as an init method that populates the grid with data. 
    
    Required members are: GetNumber[Rows|Cols], GetValue, SetValue, and IsEmptyCell.
    """
    
    dataTypes = colInfo.colType # used for custom renderers
    
    def __init__(self, parent, data):
        # TODO: This needs to be cleaned up so that CustomDataTable does not have to
        # deal with so much data specification. This should be a single fcn call for
        # data
        self.localData = data
        self.database = Database()
        self.parent = parent
        
        self._rows = self.GetNumberRows()
        self._cols = self.GetNumberCols()
        
        gridlib.PyGridTableBase.__init__(self)
    
    #***************************
    # REQUIRED METHODS
    #***************************
        
    def GetNumberRows(self):
        return len(self.localData)
    
    def GetNumberCols(self):
        return len(self.localData[0])
    
    def GetValue(self, row, col):
        return self.localData[row][col]
    
    def IsEmptyCell(self, row, col):
        try:
            if self.localData[row][col] != "":
                return True
            else:
                return False
        except:
            return False    
        
    def SetValue(self, row, col, value):
        # determine the record being modified using the primary key (located in col 5)
        e = self.database.GetExpense(self.localData[row][5])
        
        # determine which value is being set
        if(0 == col):
            e.user_id = self.database.GetUserId(value)
        if(1 == col):
            e.expenseType_id = self.database.GetExpenseTypeId(value)
        if(2 == col):
            e.amount = float(value)
        if(3 == col):
            # strptime will pull a datetime object out of an explicitly formatting string
            localDate = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            e.date = localDate
        if(4 == col):
            e.description = value
        
        self.database.EditExpense(e.amount, 
                                  e.description, 
                                  e.date,
                                  e.user_id, 
                                  e.expenseType_id, 
                                  self.localData[row][5])
        self.localData = self.database.GetAllExpenses()
            
    #***************************
    # OPTIONAL METHODS
    #***************************
    
    def DeleteRow(self, row):
        # remove from the database
        id = self.localData[row][5]
        self.database.DeleteExpense(id)
        # inform the grid
        self.GetView().ProcessTableMessage(gridlib.GridTableMessage(self,
                                           gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, 
                                           row, 1))
        # remove from the local data   
        self.localData.pop(row)
    
    def AddRow(self):
        # reload all expenses
        self.localData = self.database.GetAllExpenses()
        #inform the grid
        self.GetView().ProcessTableMessage(gridlib.GridTableMessage(self,
                                           gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED,
                                           1))
        
    def GetColLabelValue(self, col):
        return colInfo.colLabels[col]
