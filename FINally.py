#!/usr/bin/env python

#********************************************************************
# Filename: 	   	FINally.py
# Authors: 		Daniel Sisco
# Date Created:   	4-20-2007
# 
# Abstract: This is the primary file for the FINally expense analysis tool. It is responsible for
# handling read/write access to the SQLite database as well as providing a GUI interface for the user.
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
# along with Fin-ally.  If not, see <http://www.gnu.org/licenses/>.
#********************************************************************

# import wxPython libraries - including some simplifiers for grid and calendar
import wx
import wx.grid     as gridlib
import wx.calendar as callib
from datetime import date, datetime
from database import *

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
selectionID = 0

#********************************************************************
# FINally class definitions
#********************************************************************

#********************************************************************		
class CustomDataTable(gridlib.PyGridTableBase):
	"""This is an instance of the uninstantiated base class PyGridTableBase. It must contain
	methods for actually returning or modifying data in the grid, as well as an init method
	for populating the grid"""
	
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
		return self.localData[row][col] is not None
		
	def SetValue(self, row, col, value):
		# determine the record being modified using the primary key (located in col 5)
		localExpenseObj = Expense.query.filter_by(id=self.localData[row][5]).one()
		
		# determine which value is being set
		if(0 == col):
			localUserObj         = User.query.filter_by(name=value).one()
			localExpenseObj.user = localUserObj
		if(1 == col):
			localTypeObj		 = ExpenseType.query.filter_by(description=value).one()
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

#********************************************************************
class GraphicsPage(wx.Panel):
	"""The Graphics page contains two things - a grid or table of entries, and a 
	button panel to perform some operations on the grid."""
	
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
	
		self.SetBackgroundColour("GREY")

		# create wx.Grid object
		self.grid = GraphicsGrid(self)
		
		# create a userlist and type list for the menus
		# NOTE: this must be done after the Database creation above
		# define local Expense objects for population
		self.database       = Database()
		self.userList		= self.database.GetAllUsers()
		self.typeList		= self.database.GetAllTypes()
		
		# create a panel for the buttons
		self.buttonPanel  = wx.Panel(self)
		
		# create and bind a delete button
#		self.deleteButton = wx.Button(self.buttonPanel, 
#									  id=-1, 
#									  label = "Delete", 
#									  pos = (0,0))
#		self.Bind(wx.EVT_BUTTON, self.OnDeleteClick, self.deleteButton)
		
		self.entryButton = wx.Button(self.buttonPanel,
									id = -1,
									label = "Enter!",
									pos = (0,0))
		self.Bind(wx.EVT_BUTTON, self.OnEnterClick, self.entryButton)
		
		# create and bind a user selection box
		self.userSelect   = wx.ComboBox(self.buttonPanel, 
									    id=-1,
									    value=self.userList[0],
									    choices=self.userList,
						  				pos=(100,0), 
						  				style=wx.CB_DROPDOWN)
		self.Bind(wx.EVT_COMBOBOX, self.OnUserSelect, self.userSelect)
		
		# create and bind a type selection box
		self.typeSelect	  = wx.ComboBox(self.buttonPanel, 
									    id=-1,
									    value=self.typeList[0],
									    choices=self.typeList,
						  				pos=(200,0), 
						  				style=wx.CB_DROPDOWN)
		self.Bind(wx.EVT_COMBOBOX, self.OnTypeSelect, self.typeSelect)
		
		# create and bind a calendar box
		self.cal 		  = callib.CalendarCtrl(self.buttonPanel, 
												-1, 
												wx.DateTime_Now(), 
												pos = (600,0),
						    					style = callib.CAL_SHOW_HOLIDAYS | callib.CAL_SUNDAY_FIRST)
		self.Bind(callib.EVT_CALENDAR_SEL_CHANGED, self.OnCalSelChanged, self.cal)

		# create and bind a value entry box
		self.valueEntry   = wx.TextCtrl(self.buttonPanel, 
									    -1, 
									    "0.00", 
									    pos = (300,0), 
									    size = (90, 21))
		self.Bind(wx.EVT_TEXT, self.OnValueEntry, self.valueEntry)

		# create and bind a description box
		self.descEntry    = wx.TextCtrl(self.buttonPanel, 
									    -1, 
									    "item description", 
									    pos = (400,0), 
									    size = (173,21))
		self.Bind(wx.EVT_TEXT, self.OnDescEntry, self.descEntry)
		
		# create a sizer for this Panel and add the buttons and the table
		self.sizer = wx.BoxSizer(wx.VERTICAL)      # define new box sizer	
		self.sizer.Add(self.grid, 1, wx.GROW)     # add grid (resize vert and horz)
		self.sizer.Add(self.buttonPanel, 0, wx.ALIGN_LEFT)    # add panel (no resize vert and aligned left horz)
		self.SetSizer(self.sizer)

	#def OnDeleteClick(self, evt):
	#	"""this should delete whatever piece of data is selected from the database"""

		#self.expenses.deleteData(selectionID)
		#self.table.UpdateGrid()
	
	def OnEnterClick(self, evt):
		"""respond to the user clicking 'enter!' by pushing the local objects into the database 
		layer"""
		
		# it's critical to create new database objects here
		localUserObject    = User()
		localTypeObject    = ExpenseType()
		localExpenseObject = Expense()
		
		#
		# NOTE: operator selects both User and ExpenseType by selecting a string.
		# This string is used to look up the existing database objects, which are
		# fed to the overall Expense object for creation. 
		# 
		# TODO: this needs to be smarter: (A) what if the string doesn't match an existing
		# object? (B) What if the user wants to enter a new object?
		#
		localUserObject = User.query.filter_by(name=self.userSelect.GetValue()).one()
		localTypeObject = ExpenseType.query.filter_by(description=self.typeSelect.GetValue()).one()
		# configure amount, description, and date
		amount = self.valueEntry.GetValue()
		# place something here to avoid math errors
		if(amount == ""):
			amount = 0.00
		localExpenseObject.amount=float(amount)
		localExpenseObject.description=self.descEntry.GetValue()
		localExpenseObject.date=self.cal.PyGetDate()
		
		# consolidate objects into one expense type
		localExpenseObject.user 	   = localUserObject
		localExpenseObject.expenseType = localTypeObject
		self.database.CreateExpense(localExpenseObject)
		self.grid.UpdateGrid()
	
    #***************************
	# NOT REQUIRED AT THIS TIME
	#***************************
	
	def OnUserSelect(self, evt):
		pass
		
	def OnTypeSelect(self, evt):
		pass
		
	def OnCalSelChanged(self, evt):
		print "DATE", self.cal.PyGetDate()
		pass
		
	def OnValueEntry(self, evt):
		pass
		
	def OnDescEntry(self, evt):
		pass

#********************************************************************		
class GraphicsGrid(gridlib.Grid):
	"""This is primarily a display class, and it is responsible for maintaining the grid table
	itself. It is not responsible for data management."""
		
	#TODO: determine how much control to give this over the data we want to see. Consider adding
	#another class for the data itself, a class that would be passed to everything and modified
	#in many places. This would allow a future calculation object to make changes and force them
	#to show up in the graphics page.
		
	def __init__(self, parent):
		gridlib.Grid.__init__(self, parent)
		
		# pull some data out of the database and push it into the tableBase
		self.database = Database()
		self.tableBase = CustomDataTable(self,self.database.GetAllExpenses())	# define the base
		
		self.SetTable(self.tableBase) 		# set the grid table
		self.SetColFormatFloat(2,-1,2)		# formats the monetary entries correctly
		self.AutoSize() 		# auto-sizing here ensures that scrollbars will always be present
								# during window resizing
		
		# Make certain cols read only
		self.rowAttr = gridlib.GridCellAttr() 
		self.CreateReadOnlyCols()
		self.InitialTableFormat()		

		# bind editor creation to an event so we can 'catch' unique editors
		self.Bind(gridlib.EVT_GRID_EDITOR_CREATED,
				  self.OnGrid1GridEditorCreated)

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
			for i in self.database.GetAllUsers():
				self.comboBox.Append(i)
				
		# Col 1 is the Expense Type object column
		elif Col == 1:
			self.comboBox = event.GetControl()
			self.comboBox.Bind(wx.EVT_COMBOBOX, self.ComboBoxSelection)
			for i in self.database.GetAllTypes():
				self.comboBox.Append(i)
		
	def ComboBoxSelection(self, event):
		"""This method fires when the underlying ComboBox object is done with
		it's selection"""

		# DAN: is this code useless? It seems like it is...
		value 	  = self.comboBox.GetValue()
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
class ImportPage(wx.Panel):
	
	def __init__(self, parent, localExpenses):
		wx.Panel.__init__(self, parent)
		self.expenses = localExpenses
		self.variables = entryVariables()
		
		self.importButton = wx.Button(self, -1, label = "import expenses", pos = (10,10))
		self.Bind(wx.EVT_BUTTON, self.OnImportClick, self.importButton)
		
		self.userList = wx.ListBox(self, -1, pos = (10, 70), size = (90, 30),
					   choices = users, style = wx.LB_SINGLE)
		self.Bind(wx.EVT_LISTBOX, self.OnListBox, self.userList)
		self.userList.SetSelection(0)
	
	def OnListBox(self, evt):
		self.variables.desiredUser = evt.GetString()
	
	def OnImportClick(self, evt):
		print "begin import"
		# spawn a file browser and ask user to locate import file
		wildcard = "text file (*.txt)|*.txt|" \
			"All files (*.*)|*.*"
		dialog = wx.FileDialog(None, "Choose a file", os.getcwd(),
				       "", wildcard, wx.OPEN)
		if dialog.ShowModal() == wx.ID_OK:
			print dialog.GetPath()
			path = dialog.GetPath()
		dialog.Destroy()
		
		# TODO: make sure all buttons have been set correctly
		
		# do the import
		file_object = open(path)
		# iterate over each line in file
		for line in file_object:
			line = line.rstrip('\n') 	#strip trailing newline
			line_array = line.split(',') 	#split on commas
	
			# load global desiredVars structure
			self.variables.desiredValue = float(line_array[0])
			self.variables.desiredDate  = line_array[1]
			# remove all non-standard characters that the import will choke on
			line_array[2] = re.sub('\'','', line_array[2])
			self.variables.desiredDesc  = line_array[2]

			self.expenses.getData(self.variables.desiredUser,
					      self.variables.desiredValue,
					      self.variables.desiredDate,
					      self.variables.desiredDesc)

		file_object.close() # close file object
#********************************************************************

class AppMainFrame(wx.Frame):
	"""This class inherts wx.Frame methods, and is the top level window of our application."""
	
	size = (900,900)
	
	def __init__(self, title):
		wx.Frame.__init__(	self,
				  	None,
				  	id=-1,
				  	title=title,
				  	pos=wx.DefaultPosition,
		  			size=AppMainFrame.size,
		  			style=wx.DEFAULT_FRAME_STYLE)

		# add an icon!
		self.icon = wx.Icon("img/FINally.ico", wx.BITMAP_TYPE_ICO)
		self.SetIcon(self.icon)

		self.panel    = wx.Panel(self) # basically just a container for the notebook
		self.notebook = wx.Notebook(self.panel, size=AppMainFrame.size)

		self.gPage = GraphicsPage(self.notebook)
		self.notebook.AddPage(self.gPage, "Graphics")

		# arrange notebook windows in a simple box sizer
		self.sizer = wx.BoxSizer()
		self.sizer.Add(self.notebook, 1, wx.EXPAND)
		self.panel.SetSizer(self.sizer)

	def SetBackgroundColor(self, colorString):
		self.SetBackgroundColour(colorString)

#********************************************************************
class AppLauncher(wx.App):
	"""This class inherits wx.App methods, and should be the first object created during FINally
	operation. This will be the only instance of an application class and will contain the primary
	Frame (top level window)."""
	
	# static variables go here
	version = "2.0.1"
	title   = "FINally version " + version
	
	def OnInit(self):
		"""Should be used instead of __init__ for Application objects"""
		
		# create and make visible a "top level window" of type wxFrame
		self.frame = AppMainFrame(AppLauncher.title)
		self.frame.Show(True)
		self.SetTopWindow(self.frame)
		
		return True # required during OnInit
	
	def Main(self):
		"""kicks off the application heartbeat, which means that we let wxPython watch for user
		input (mouse, keyboard, etc...) and respond"""
		self.MainLoop()
	
	def GetTitle(self):
		"""returns the title of the application - as shown in the top level window"""
		return AppLauncher.title
	
	def GetVersion(self):
		"""returns the version of this application"""
		return AppLauncher.version

#*******************************************************************************************************
#                                                 MAIN 
#*******************************************************************************************************

if __name__ == '__main__':
	"""This is the starting point for the FIN-ally application. All functionality that must occur
	pre-GUI-start must be placed here. The final action in this main fcn should be the launch of
	the GUI Main."""
	
	# create an instance of the Database class and then perform the initial database ID
	db = Database();
	db.IdentifyDatabase();
	
	# create highest level wx object (wxApp) instance
	launcher = AppLauncher(redirect=False) 
	launcher.Main()
