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
#import wx.calendar as callib
from datetime import date, datetime
from database import *
#from wx._core import WXK_F1, WXK_F2

#********************************************************************    
class columnInfo:
    """This class defines the information required to create and modify columns in
    a grid. This keeps all columns definition data together, but adding information here
    does complete the addition of a new column."""
    
    # TODO: consolidate these into a dict or some other structure
    colLabels = ('user', 'type', 'amount', 'date', 'desc', 'id')
    colWidth  = [100, 50, 50, 200, 350, 50]
    colRO     = [0,0,0,0,0,1] # 0 = R/W, 1 = R
    colType   = [gridlib.GRID_VALUE_CHOICE,
                  gridlib.GRID_VALUE_CHOICE,
                  gridlib.GRID_VALUE_NUMBER,
                  gridlib.GRID_VALUE_STRING, # should be GRID_VALUE_DATETIME
                  gridlib.GRID_VALUE_STRING,
                  gridlib.GRID_VALUE_NUMBER]
    
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
        self.CreateReadOnlyCols()
        self.InitialTableFormat()

        # bind editor creation to an event so we can 'catch' unique editors
        self.Bind(gridlib.EVT_GRID_EDITOR_CREATED,
                  self.OnGrid1GridEditorCreated)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.onGridRightClick)

    def onGridRightClick(self, event):
        # highlight the grid row in red
        row = event.GetRow()
        attr = gridlib.GridCellAttr()
        attr.SetBackgroundColour(wx.RED)
        self.SetRowAttr(row, attr)
        self.UpdateGrid()
        
        # only do this part the first time so the events are only bound once
        #
        # Yet another anternate way to do IDs. Some prefer them up top to
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

    def OnPopupDelete(self, event, row):
        # delete the current row
        # TODO: add a #define here or something
        self.tableBase.DeleteRow(row)
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
            for i in self.database.GetUserList():
                self.comboBox.Append(i)
                
        # Col 1 is the Expense Type object column
        elif Col == 1:
            self.comboBox = event.GetControl()
            self.comboBox.Bind(wx.EVT_COMBOBOX, self.ComboBoxSelection)
            for i in self.database.GetTypeList():
                self.comboBox.Append(i)
        
    def ComboBoxSelection(self, event):
        """This method fires when the underlying ComboBox object is done with
        it's selection"""

        # DAN: is this code useless? It seems like it is...
        value       = self.comboBox.GetValue()
        selection = self.comboBox.GetSelection()
        pass
            
    def CreateReadOnlyCols(self):
        """creates read-only columns"""
        self.rowAttr.SetReadOnly(1)
        for i in range(len(colInfo.colRO)):
            if colInfo.colRO[i] == 1: 
                self.SetColAttr(i,self.rowAttr) 
        self.rowAttr.IncRef() 
            
    def UpdateGrid(self):
        """Called after a grid value is edited or newly entered. re-loads
        underlying grid data and forces grid to display new data"""
        self.tableBase.localData = self.database.GetAllExpenses()
        self.tableBase.UpdateValues(self)
        self.tableBase.ResetView(self)
        # DAN: we need to set the editor for new rows only - find out how to do that
        
    def InitialTableFormat(self):
        """Formats the grid table - adding width, height, and unique editors"""
        
        # create 'drop down' style choice editors for two columns
        userChoiceEditor = gridlib.GridCellChoiceEditor([], allowOthers = False)
        typeChoiceEditor = gridlib.GridCellChoiceEditor([], allowOthers = False)

        # apply editors and row height to each row
        for i in range(self.GetNumberRows()):
            self.SetCellEditor(i,0,userChoiceEditor)
            self.SetCellEditor(i,1,typeChoiceEditor)
            self.SetCellEditor(i,2,gridlib.GridCellFloatEditor(-1,2))
            
            self.SetRowSize(i, colInfo.rowHeight)
            
        # format column width
        tmp = 0
        for i in colInfo.colWidth:
            self.SetColSize(tmp,i)
            tmp += 1

#********************************************************************        
class CustomDataTable(gridlib.PyGridTableBase):
    """
    Class Name:     CustomDataTable
    Extends:        wx.grid.PyGridTableBase (gridlib.PyGridTableBase)
    Description:    An instance of the uninstantiatd base class PyGridTableBase. This instance
    must contain several methods (listed below) for modifying/viewing/querying data in the grid.
    As well as an init method that populates the grid with data. 
    
    Requred members are: GetNumber[Rows|Cols], GetValue, SetValue, and IsEmptyCell.
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
        #print "(", row, ",", col, ")"
        return self.localData[row][col]
    
    def IsEmptyCell(self, row, col):
        return self.localData[row][col] is not None
        
    def SetValue(self, row, col, value):
        # determine the record being modified using the primary key (located in col 5)
        localExpenseObj = Expense.query.filter_by(id=self.localData[row][5]).one()
        
        # determine which value is being set
        if(0 == col):
            localUserObj         = User.query.filter_by(name=value).one()
            localExpenseObj.user = localUserObj
        if(1 == col):
            localTypeObj         = ExpenseType.query.filter_by(description=value).one()
            localExpenseObj.expenseType = localTypeObj
        if(2 == col):
            localExpenseObj.amount = float(value)
        if(3 == col):
            # strptime will pull a datetime object out of an explicitly formatting string
            localDate = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            localExpenseObj.date = localDate
        if(4 == col):
            localExpenseObj.description = value
            
        self.database.CreateExpense(localExpenseObj)
        self.parent.UpdateGrid()
        
    def DeleteRow(self, row):
        """removes the row provided in the argument and removes data from the database"""
        print "you deleted a row!"
        #id = self.GetValue(row,5)
        #self.database.DeleteExpense(id)
        #self.UpdateValues(self.parent)
        #self.ResetView(self.parent)    
            
    #***************************
    # OPTIONAL METHODS
    #***************************
    
    def GetColLabelValue(self, col):
        return colInfo.colLabels[col]
    
    def ResetView(self, grid):
        """
        (Grid) -> Reset the grid view.   Call this to
        update the grid if rows and columns have been added or deleted
        """
        grid.BeginBatch()
        
        for current, new, delmsg, addmsg in [
            (self._rows, self.GetNumberRows(),gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED),
            (self._cols, self.GetNumberCols(),gridlib.GRIDTABLE_NOTIFY_COLS_DELETED, gridlib.GRIDTABLE_NOTIFY_COLS_APPENDED),
        ]:
            if new < current:
                msg = gridlib.GridTableMessage(self,delmsg,new,current-new)
                grid.ProcessTableMessage(msg)
            elif new > current:
                msg = gridlib.GridTableMessage(self,addmsg,new-current)
                grid.ProcessTableMessage(msg)
                self.UpdateValues(grid)
        
        grid.EndBatch()
        
        self._rows = self.GetNumberRows()
        self._cols = self.GetNumberCols()
        # update the column rendering plugins
        #self._updateColAttrs(grid)
        
        # update the scrollbars and the displayed part of the grid
        grid.AdjustScrollbars()
        grid.ForceRefresh()
        
    def UpdateValues(self, grid):
        """Update all displayed values"""
        # This sends an event to the grid table to update all of the values
        msg = gridlib.GridTableMessage(self,gridlib.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        grid.ProcessTableMessage(msg)
