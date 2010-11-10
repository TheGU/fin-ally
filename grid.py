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
from database import Database
from utils import dateMatch

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
        self.tableBase = CustomDataTable(self,1)    # define the base
        
        self.SetTable(self.tableBase)         # set the grid table
        self.SetColFormatFloat(2,-1,2)        # formats the monetary entries correctly
        self.AutoSize()         # auto-sizing here ensures that scrollbars will always be present
                                # during window resizing     
                             
        self.rowAttr = gridlib.GridCellAttr()                               
        self.FormatTableRows()  
        self.FormatTableCols()                       

        # bind editor creation to an event so we can 'catch' unique editors
        self.Bind(gridlib.EVT_GRID_EDITOR_CREATED,
                  self.OnGrid1GridEditorCreated)
        
        # bind grid-based context menu if active
        if cfg.GRID_CONTEXT_MENU == 1:
            self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.onGridRightClick)
        
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.onGridClick)
        self.Bind(gridlib.EVT_GRID_CMD_LABEL_LEFT_CLICK, self.onColClick)
        
    def onColClick(self, event):
        if event.GetRow() == -1 and event.GetCol() != -1:
            localSortBy = colInfo.colLabels[event.GetCol()]
            
            # some col names match the database sort term, but some do not
            if localSortBy == 'user':
                self.database.SetSortTerm(1, 'user_id')
            elif(localSortBy == 'type'):
                self.database.SetSortTerm(1, 'expenseType_id')
            elif(localSortBy == 'amount'):
                self.database.SetSortTerm(1, 'amount')
            elif(localSortBy == 'date'):
                self.database.SetSortTerm(1, 'date')     
            elif(localSortBy == 'desc'):
                self.database.SetSortTerm(1, 'description')
            elif(localSortBy == 'id'):
                self.database.SetSortTerm(1, 'id')           
        else:
            print "you did not click a column"
            
        self.tableBase.UpdateData()
        self.ForceRefresh()
        event.Skip()
        
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
        event.Skip()
    
    def FormatTableCols(self):
        if self.tableBase.GetNumberRows():
            # create read-only columns        
            self.rowAttr.SetReadOnly(1)
            for i in range(len(colInfo.colRO)):
                if colInfo.colRO[i] == 1: 
                    self.SetColAttr(i,self.rowAttr) 
            self.rowAttr.IncRef() 
                
            # format column width
            tmp = 0
            for i in colInfo.colWidth:
                self.SetColSize(tmp,i)
                tmp += 1
    
    def FormatTableRows(self, skipEditorRefresh=0):
        for i in range(self.tableBase.GetNumberRows()):
            self._FormatTableRow(i, skipEditorRefresh)
            
    def _FormatTableRow(self, row, skipEditorRefresh):
        """Formats a single row entry - editor types, height, color, etc..."""
        if skipEditorRefresh == 0:
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
    
    previousRowCnt = 0
    previousColCnt = 0
    localData = []
    parent = 0
    
    # used to turn this class into a Borg class 
    __shared_state = {}

    def __init__(self, parent, first=0):
        # bind the underlyng Python dictionary to a class variable
        self.__dict__ = self.__shared_state
        
        gridlib.PyGridTableBase.__init__(self)
        
        # TODO: This needs to be cleaned up so that CustomDataTable does not have to
        # deal with so much data specification. This should be a single fcn call for
        # data
        self.__class__.previousRowCnt = 0
        self.__class__.previousColCnt = 0
        
        self.database = Database()
        self.__class__.localData = self.database.GetAllExpenses()
        
        if(first):
            self.__class__.parent = parent
    
    #***************************
    # REQUIRED METHODS
    #***************************
        
    def GetNumberRows(self):
        return len(self.__class__.localData)
    
    def GetNumberCols(self):
        if self.GetNumberRows():
            return len(self.__class__.localData[0])
        else:
            return 0
    
    def GetValue(self, row, col):
        return self.__class__.localData[row][col]
    
    def IsEmptyCell(self, row, col):
        try:
            if self.__class__.localData[row][col] != "":
                return True
            else:
                return False
        except:
            return False    
        
    def SetValue(self, row, col, value):
        comboBoxEdit = 0
        
        # determine the record being modified using the primary key (located in col 5)
        e = self.database.GetExpense(self.__class__.localData[row][5])
        
        # determine which value is being set
        if(0 == col):
            e.user_id = self.database.GetUserId(value)
            comboBoxEdit = 1
        if(1 == col):
            e.expenseType_id = self.database.GetExpenseTypeId(value)
            comboBoxEdit = 1
        if(2 == col):
            e.amount = float(value)
        if(3 == col):
            # strptime will pull a datetime object out of an explicitly formatting string
            localDate = dateMatch(value)
            e.date = localDate
        if(4 == col):
            e.description = value
        
        self.database.EditExpense(e.amount, 
                                  e.description, 
                                  e.date,
                                  e.user_id, 
                                  e.expenseType_id, 
                                  self.__class__.localData[row][5])
        
        # we want to avoid trying to modify the editor property if we've 
        # just finished working with an editor.
        self.UpdateData(comboBoxEdit)
            
    #***************************
    # OPTIONAL METHODS
    #***************************
    
    def UpdateData(self, skipEditorRefresh=0):
        """This function performs the following actions: (1) pulls data from the 
        database in the specified order and lying within the specific window criteria.
        (2) checks to see if a resize attempt is necessary. (3) updates old col/row counts
        (4) refreshes grid. This function is intended to be the single point of contact 
        for performing a data refresh."""
        
        self.__class__.previousColCnt = self.GetNumberCols()
        self.__class__.previousRowCnt = self.GetNumberRows()
        self.__class__.localData = self.database.GetAllExpenses()
        self.__ResetView(skipEditorRefresh)
    
    def GetPrevNumberRows(self):
        return self.__class__.previousRowCnt
    
    def GetPrevNumberCols(self):
        return self.__class__.previousColCnt
    
    def DeleteRow(self, row):
        """This function determines the ID of the element being deleted, removed it from the 
        database, informs the grid that a specific row is being removed, and then removes it from the 
        localData data collection. This is faster than re-loading all the expenses."""
        
        # remove from the database
        id = self.__class__.localData[row][5]
        self.database.DeleteExpense(id)
        self.UpdateData()
    
    def __ResetView(self, skipEditorRefresh):
        """This function can be found at: http://wiki.wxpython.org/wxGrid 
        It implements a generic resize mechanism that uses the previous and current
        row and col count to determine if the grid should be trimmed or extended. It
        refreshes grid data and resizes the scroll bars using a 'jiggle trick'"""
        
        self.GetView().BeginBatch()
        for current, new, delmsg, addmsg in [(self.__class__.previousRowCnt, self.GetNumberRows(), gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED),
                                             (self.__class__.previousColCnt, self.GetNumberCols(), gridlib.GRIDTABLE_NOTIFY_COLS_DELETED, gridlib.GRIDTABLE_NOTIFY_COLS_APPENDED)]:
            # determine if we've added or removed a row or col...
            if new < current:
                msg = gridlib.GridTableMessage(self,
                                               delmsg,
                                               new,    # position
                                               current-new)
                self.GetView().ProcessTableMessage(msg)
            elif new > current:
                msg = gridlib.GridTableMessage(self,
                                               addmsg,
                                               new-current)
                self.GetView().ProcessTableMessage(msg)
                        
        # refresh all data
        msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        self.GetView().ProcessTableMessage(msg)
        self.GetView().EndBatch()
        
        # apply correct formatting to each row after update
        self.__class__.parent.FormatTableRows(skipEditorRefresh)
        self.__class__.parent.FormatTableCols()

        # The scroll bars aren't resized (at least on windows)
        # Jiggling the size of the window rescales the scrollbars
        h,w = self.__class__.parent.GetSize()
        self.__class__.parent.SetSize((h+1, w))
        self.__class__.parent.SetSize((h, w))
        self.__class__.parent.ForceRefresh()
        
    def GetColLabelValue(self, col):
        return colInfo.colLabels[col]
