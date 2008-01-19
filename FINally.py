#*******************************************************************************************************
# Filename: FINally.py
# Author: Daniel Sisco
# Date Created: 4-20-2007
# 
# Abstract: This is the primary file for the FINally expense analysis tool. It is responsible for
# handling read/write access to the SQLite database as well as providing a GUI interface for the user.
#
# * Make sure the cell you've selected is the row you will delete
# * Make the raw data column invisible or hide it somehow
#*******************************************************************************************************

import datetime
import os
import wx.grid
import re
import sys
import wx
import wx.calendar
from SQLite_drivers import * 

#********************************************************************
# Global variables, structures, and definitions
#********************************************************************
version = "1.0.0"
database = "FINally_data.db"
users = ['rachel','daniel']

#********************************************************************
class desiredVariables:
	"""This class contains the variables required for entry into the EXPENSES
	table of the assoiated FINally database."""

	desiredUser 		= users[0]
	desiredDate 		= '01012007'
	desiredValue 		= float(1.11)
	desiredDesc 		= ""

#********************************************************************	
class columnInfo:
	"""This class defines the information required to create and modify columns in
	a grid. This keeps all columns definition data together, but adding information here
	does complete the addition of a new column."""

	colLabels = ['id', 'who', 'amount', 'date', 'desc']
	colWidth  = [50, 50, 50, 50, -1]
	colType   = [wx.grid.GRID_VALUE_NUMBER,
		     wx.grid.GRID_VALUE_CHOICE + ':rachel, daniel',
		     wx.grid.GRID_VALUE_NUMBER,
		     wx.grid.GRID_VALUE_STRING, # should be GRID_VALUE_DATETIME
		     wx.grid.GRID_VALUE_STRING]
	
	rowHeight = 20
	
# create global instances of classes
desiredVars = desiredVariables()
colInfo = columnInfo()
selectionID = 0

# TODO: capture the data here
masterDate = datetime.date.today()
currMonthStart = str(masterDate.month) + '00' + str(masterDate.year)
currMonthEnd = str(masterDate.month) + '31' + str(masterDate.year)

#********************************************************************
# FINally class definitions
#********************************************************************

#********************************************************************
class EntryPage(wx.Panel):
	
	def __init__(self, parent, grid):
		
		wx.Panel.__init__(self, parent)
		
		self.grid = grid

		# control definitions
		self.enterButton = wx.Button(self, -1, label = "enter expense", pos = (10,10))
		self.Bind(wx.EVT_BUTTON, self.OnEnterClick, self.enterButton)

		self.userList = wx.ListBox(self, -1, pos = (10, 70), size = (90, 30),
					   choices = users, style = wx.LB_SINGLE)
		self.Bind(wx.EVT_LISTBOX, self.OnListBox, self.userList)
		self.userList.SetSelection(0)

		self.cal = wx.calendar.CalendarCtrl(self, -1, wx.DateTime_Now(), pos = (110,10),
						    style = wx.calendar.CAL_SHOW_HOLIDAYS
						    | wx.calendar.CAL_SUNDAY_FIRST)
		self.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED, self.OnCalSelChanged, self.cal)
		# TODO: set calendar date (force)

		self.valueEntry = wx.TextCtrl(self, -1, "0.00", pos = (10,160), size = (90, 21))
		self.Bind(wx.EVT_TEXT, self.OnValueEntry, self.valueEntry)

		self.descEntry = wx.TextCtrl(self, -1, "item description", pos = (110,160), size = (173,21))
		self.Bind(wx.EVT_TEXT, self.OnDescEntry, self.descEntry)

	def OnCalSelChanged(self, evt):
		global desiredVars
		
		date = evt.PyGetDate() # grab selected date
		desiredVars.desiredDate = date.strftime("%m%d%Y")

	def OnDescEntry(self, evt):
		global desiredVars
	
		desiredVars.desiredDesc = evt.GetString()
	
	def OnEnterClick(self, evt):
		global desiredVars
		
		MCInsertData(database,
			     desiredVars.desiredUser,
			     desiredVars.desiredValue,
			     desiredVars.desiredDate,
			     desiredVars.desiredDesc)
		
		# clear the buttons so they don't show the old info
		self.valueEntry.SetValue("0.00")
		self.descEntry.SetValue("item description")
		
		self.grid.table.UpdateGrid()
	
	def OnListBox(self, evt):
		global desiredVars
		
		desiredVars.desiredUser = evt.GetString()
	
	def OnValueEntry(self, evt):
		global desiredVars
		
		amount = evt.GetString()
		# place something here to avoid math errors
		if(amount == ""):
			amount = 0.00
		
		desiredVars.desiredValue = float(amount)

#********************************************************************		
class CustomDataTable(wx.grid.PyGridTableBase):
	"""This is an instance of the uninstantiated base class PyGridTableBase. Some
	of the methods in this function must be defined, and some methods provide additional
	functionality."""
	
	dataTypes = colInfo.colType # used for custom renderers
	
	def __init__(self): 
		wx.grid.PyGridTableBase.__init__(self)
		
		# TODO: we need to dynamically get the real data here so that we always
		# display the current month at startup
		#temp = "date > %s AND date < %s" % (currMonthStart, currMonthEnd)
		#self.localData = MCGetData(database, 2, temp, -1, -1)
		self.localData = MCGetData(database, 1, -1, -1, -1)
		
		self._rows = self.GetNumberRows()
		self._cols = self.GetNumberCols()
		
	def GetNumberRows(self):
		return len(self.localData)
	
	def GetNumberCols(self):
		return len(self.localData[0])
	
	def IsEmptyCell(self, row, col):
		return False
	
	def GetValue(self, row, col):
		""" Stores the entry ID to a global var to be used for deletion. """
		global selectionID
		
		selectionID = self.localData[row][0]
		return self.localData[row][col]
	
	def SetValue(self, row, col, value):
		tempId = self.localData[row][0]
		tempColumn = colInfo.colLabels[col]
		tempValue = '' 
		
		#HERE - fix this part 
		if(0 == col):
			print "this is not an editable column!"
		elif( (1 == col) or (3 == col) or (4 == col)):
			tempValue = value
		elif(2 == col):
			# match an amount
			tempValue = float(value)
		
		MCUpdateOne(database, tempColumn, tempValue, tempId)
		self.UpdateValues()
	
	def GetColLabelValue(self, col):
		return colInfo.colLabels[col]
	
	# this type allows custom renderers to be used
	def GetTypeName(self, row, col):
		return self.dataTypes[col]
	
	def UpdateValues(self):
		"""Pull new data from the database. This seems to also update the appropriate values in the table, because
		calling this and then calling ResetView (to handle added/deleted cols/rows) updates the table appropriately."""

		# TODO: We need to catch the real month here as well
		temp = "date > %s AND date < %s" % (currMonthStart, currMonthEnd)
		self.localData = MCGetData(database, 2, temp, -1, -1)
		
		# This code doesn't appear to be necessary, but is typically included in common implementations
		# if this is re-added, a 'grid' component will need to be passed to this function.
		#msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
		#grid.ProcessTableMessage(msg)
		
	def ResetView(self, grid):
		""" (Grid) -> Reset the grid view. Call this to
		update the grid if rows and columns have been added or deleted """
		grid.BeginBatch() #begin supression of screen painting
	
		for current, new, delmsg, addmsg in [
		    (self._rows, self.GetNumberRows(), wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED, wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED),
		    (self._cols, self.GetNumberCols(), wx.grid.GRIDTABLE_NOTIFY_COLS_DELETED, wx.grid.GRIDTABLE_NOTIFY_COLS_APPENDED),
		]:
	
			if new < current:
				msg = wx.grid.GridTableMessage(self,delmsg,new,current-new)
				grid.ProcessTableMessage(msg)
			elif new > current:
				msg = wx.grid.GridTableMessage(self,addmsg,new-current)
				grid.ProcessTableMessage(msg)
				self.UpdateValues()
		
		grid.EndBatch() #end supression of screen painting
	
		self._rows = self.GetNumberRows()
		self._cols = self.GetNumberCols()
	
		# update the scrollbars and the displayed part of the grid
		grid.AdjustScrollbars()
		grid.ForceRefresh()

#********************************************************************
class GraphicsPage(wx.Panel):
	
	def __init__(self, parent):
		
		wx.Panel.__init__(self, parent)
		
		# define panel and grid controls
		panel = wx.Panel(self) 
		self.SetBackgroundColour("GREY")
		self.deleteButton = wx.Button(panel, -1, label = "Delete", pos = (0,0))
		# HERE - this needs to be modified to provide a month select drop-down, as well as some sort
		# of control scheme for "searching" based on type, words, who, etc..
		self.CategorySelect = wx.ComboBox(panel, -1, "January", choices=["January", "February", "March", "April", "May", "June", "July",
										 "August", "September", "October", "November", "December"],
						  pos = (700,0), style = wx.CB_DROPDOWN)
		
		self.table = GPTable(self)
		sizer = wx.BoxSizer(wx.VERTICAL)      # define new box sizer	
		sizer.Add(self.table, 1, wx.GROW)     # add grid (resize vert and horz)
		sizer.Add(panel, 0, wx.ALIGN_LEFT)    # add panel (no resize vert and aligned left horz)
		self.SetSizer(sizer)
		
		self.Bind(wx.EVT_BUTTON, self.OnDeleteClick, self.deleteButton)
		
	def OnDeleteClick(self, evt):
		global selectionID
		
		MCDeleteData(database,selectionID)
		self.table.UpdateGrid()

#********************************************************************		
class GPTable(wx.grid.Grid):
		
	def __init__(self, parent):
		wx.grid.Grid.__init__(self, parent)
		
		self.tableBase = CustomDataTable()		# define the base
		self.SetTable(self.tableBase) 			# set the grid table
		self.SetColFormatFloat(2,-1,2) 			# formats the monetary entries correctly
		self.AutoSize() # auto-sizing here ensures that scrollbars will always be present
				# during window resizing
		
		self.FormatTable()
	#	self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
	#		
	#def OnContextMenu(self, evt):
	#	print"context menu triggered!"
	#	if not hasattr(self, "popupID1"):
	#		self.popupID1 = wx.NewId()
	#		self.popupID2 = wx.NewId()
	#		
	#		self.Bind(wx.EVT_MENU, self.OnCMDelete, id = self.popupID1)
	#		self.Bind(wx.EVT_MENU, self.OnCMHighlight, id = self.popupID2)
	#	
	#	menu = wx.Menu()
	#	
	#	menu.Append(self.popupID1, "Delete Row")
	#	menu.Append(self.popupID2, "Highlight High Rollers")
	#	
	#	self.PopupMenu(menu)
	#	menu.Destroy()
	#	
	#def OnCMDelete(self, evt):
	#	"""this context menu delete will read the row out of the cursor position and then try to delete it"""
	#	print "delete"
	#	tempRow = self.tableBase.localData[self.GetGridCursorRow()][0]
	#	MCDeleteData(database, tempRow)
	#	self.UpdateGrid()
	#	
	#def OnCMHighlight(self, evt):
	#	print "highlight"			

	def FormatTable(self):
		# format rows
		for i in range(self.GetNumberRows()):
			self.SetCellEditor(i,2,wx.grid.GridCellFloatEditor(-1,2))
			self.SetRowSize(i, colInfo.rowHeight)
			
		# format column width
		tmp = 0
		for i in colInfo.colWidth:
			self.SetColSize(tmp,i)
			tmp += 1
			
	def UpdateGrid(self):
		self.tableBase.UpdateValues()
		self.tableBase.ResetView(self)
		self.FormatTable()
		self.ForceRefresh()

#********************************************************************		
class ImportPage(wx.Panel):
	
	def __init__(self, parent):
		
		wx.Panel.__init__(self, parent) 
		
		self.importButton = wx.Button(self, -1, label = "import expenses", pos = (10,10))
		self.Bind(wx.EVT_BUTTON, self.OnImportClick, self.importButton)
		
		self.userList = wx.ListBox(self, -1, pos = (10, 70), size = (90, 30),
					   choices = users, style = wx.LB_SINGLE)
		self.Bind(wx.EVT_LISTBOX, self.OnListBox, self.userList)
		self.userList.SetSelection(0)
	
	def OnListBox(self, evt):
		global desiredVars

		desiredVars.desiredUser = evt.GetString()
	
	def OnImportClick(self, evt):
		global desiredVars
		
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
			desiredVars.desiredValue = float(line_array[0])
			desiredVars.desiredDate  = line_array[1]
			# remove all non-standard characters that the import will choke on
			line_array[2] = re.sub('\'','', line_array[2])
			desiredVars.desiredDesc  = line_array[2]
			
			# do the import
			MCInsertData(database,
			     desiredVars.desiredUser,
			     desiredVars.desiredValue,
			     desiredVars.desiredDate,
			     desiredVars.desiredDesc)
		
		file_object.close() # close file object
#********************************************************************
class FINallyFrame(wx.Frame):
	
	def __init__(self, parent, id, title, pos=wx.DefaultPosition,
		     size=(900,400), style=wx.DEFAULT_FRAME_STYLE):
		
		wx.Frame.__init__(self, parent, id, title, pos, size, style)
		self.SetBackgroundColour("GREY")
		
		panel = wx.Panel(self) # basically just a container for the notebook
		notebook = wx.Notebook(panel, size = self.GetSize())

		gPage = GraphicsPage(notebook)
		ePage = EntryPage(notebook, gPage)
		tPage = ImportPage(notebook)
		
		notebook.AddPage(ePage, "Expense Entry")	
		notebook.AddPage(gPage, "Graphics")
		notebook.AddPage(tPage, "Import")

		# arrange notebook windows in a simple box sizer
		sizer = wx.BoxSizer()
		sizer.Add(notebook, 1, wx.EXPAND)
		panel.SetSizer(sizer)	
		
#********************************************************************
class FINallyLauncher(wx.App):

	title = "FINally version " + version
	
	def OnInit(self):
		
		# (310, 300) is a good size for just the entry window
		# 
		# create and make visible a "top level window" of type wxFrame
		win = FINallyFrame(None, -1, self.title,
				   style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
		win.Show(True)
		self.SetTopWindow(win)
	
		MCInitDatabase(database) # create (if necessary), and init database
		
		return True # required during OnInit
	
	def Main(self):
		
		self.MainLoop() # begin program heartbeat
	
	def OnExit(self):
		dan = 1

#*******************************************************************************************************
#                                                 MAIN 
#*******************************************************************************************************

# allows temporary database name change from command line
# TODO: this should be placed in the registry
if (2 == len(sys.argv)):
	database = sys.argv[1]
	print "Database name changed"

launcher = FINallyLauncher(redirect=False) # create wxApp instance with stdout/stderr redirection
launcher.Main()
