#!/usr/bin/env python

#********************************************************************
# Filename: 	   	FINally.py
# Authors: 		Daniel Sisco
# Date Created:   	4-20-2007
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
from wx._core import WXK_F1, WXK_F2
from editPage import EditPage
from grid import GraphicsGrid

#********************************************************************
# FINally class definitions
#********************************************************************

#********************************************************************
class NewExpenseDialog(wx.Dialog):
	"""
	Class Name: 	NewExpenseDialog
	Extends: 		wx.Dialog
	Description:	Dialog to support the addition of a new Expense to the database.
	This dialog should trigger both a database update, and a grid update.
	"""
	
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size=(350,300))
		
		# create a userlist and type list for the menus
		# NOTE: this must be done after the Database creation above
		# define local Expense objects for population
		self.database       = Database()
		self.userList		= self.database.GetUserList()
		self.typeList		= self.database.GetTypeList()
		
		self.parent = parent
		
		self.sizer        = wx.BoxSizer(wx.VERTICAL)  # define new box sizer	
		self.buttonPanel  = wx.Panel(self)		      # create a panel for the buttons
		
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
												pos = (0,50),
						    					style = callib.CAL_SHOW_HOLIDAYS | callib.CAL_SUNDAY_FIRST)
		self.Bind(callib.EVT_CALENDAR_SEL_CHANGED, self.OnCalSelChanged, self.cal)
	
		# create and bind a value entry box
		self.valueEntry   = wx.TextCtrl(self.buttonPanel, 
									    -1, 
									    "0.00", 
									    pos = (0,25), 
									    size = (90, 21))
		self.Bind(wx.EVT_TEXT, self.OnValueEntry, self.valueEntry)
	
		# create and bind a description box
		self.descEntry    = wx.TextCtrl(self.buttonPanel, 
									    -1, 
									    "item description", 
									    pos = (100,25), 
									    size = (173,21))
		self.Bind(wx.EVT_TEXT, self.OnDescEntry, self.descEntry)
		
		self.sizer.Add(self.buttonPanel, 0, wx.ALIGN_LEFT)    # add panel (no resize vert and aligned left horz)
		self.SetSizer(self.sizer)
		
	def OnEnterClick(self, evt):
		"""respond to the user clicking 'enter!' by pushing the local objects into the database 
		layer"""
		
		# it's critical to create a new expense object here to avoid overwriting
		# an existing expense object. However, we will *not* create user
		# or expenseType because calls below create a new expense
		localExpenseObject = Expense()
		
		#
		# NOTE: operator selects both User and ExpenseType by selecting a string.
		# This string is used to look up the existing database objects, which are
		# fed to the overall Expense object for creation. These calls also create
		# new User and ExpenseType objects as well as populate them.
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
		
		# consolidate objects into one expense type and push into database
		localExpenseObject.user 	   = localUserObject
		localExpenseObject.expenseType = localTypeObject
		self.database.CreateExpense(localExpenseObject)
		
		# update grid with new row, format new row
		self.parent.grid.tableBase.AddRow()
		self.parent.grid.FormatTableRow(self.parent.grid.tableBase.GetNumberRows()-1)
		
		self.Close()
		
	#***************************
	# NOT REQUIRED AT THIS TIME
	#***************************
	
	def OnUserSelect(self, evt):
		pass
		
	def OnTypeSelect(self, evt):
		pass
		
	def OnCalSelChanged(self, evt):
		pass
		
	def OnValueEntry(self, evt):
		pass
		
	def OnDescEntry(self, evt):
		pass

#********************************************************************
class GraphicsPage(wx.Panel):
	"""
	Class Name: 	GraphicsPage
	Extends: 		wx.Panel
	Description:	The Graphics page contains two things - a grid or table of entries, 
	and a button panel to perform some operations on the grid.
	"""
	
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
	
		self.SetBackgroundColour("GREY")
		
		# bind keyboard events
		self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

		# create wx.Grid object
		self.grid = GraphicsGrid(self)
		
		# create a userlist and type list for the menus
		# NOTE: this must be done after the Database creation above
		# define local Expense objects for population
		self.database       = Database()
		self.userList		= self.database.GetUserList()
		self.typeList		= self.database.GetTypeList()
		
		# create a panel for the buttons
		self.buttonPanel  = wx.Panel(self)
		
		# configure either a static button panel or a dialogue based on configuration settings
		if cfg.NEW_EXPENSE_PANEL == 1:		
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
		else:
			# create and bind a new expense button
			self.newExpenseButton = wx.Button(self.buttonPanel,
										      id = -1,
										      label = "New Expense",
											  pos = (0,0))
			self.Bind(wx.EVT_BUTTON, self.ShowNewExpenseDialogue, self.newExpenseButton)	
		
		# create a sizer for this Panel and add the buttons and the table
		self.sizer = wx.BoxSizer(wx.VERTICAL)      # define new box sizer	
		self.sizer.Add(self.grid, 1, wx.GROW)     # add grid (resize vert and horz)
		self.sizer.Add(self.buttonPanel, 0, wx.ALIGN_LEFT)    # add panel (no resize vert and aligned left horz)
		self.SetSizer(self.sizer)
	
	def ShowNewExpenseDialogue(self, event):
		dia = NewExpenseDialog(self, -1, 'New Expense Entry')
		dia.ShowModal()
		dia.Destroy()
		
	def OnKeyDown(self, event):
		# F1 = new expense
		if (event.GetKeyCode() == WXK_F1):
			dia = NewExpenseDialog(self, -1, 'New Expense Entry')
			dia.ShowModal()
			dia.Destroy()
		event.Skip()
		
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
		self.grid.tableBase.AddRow()
	
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
class AppMainFrame(wx.Frame):
	"""This class inherts wx.Frame methods, and is the top level window of our application."""
	
	size = (900,400)
	
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
		self.ePage = EditPage(self.notebook)
		self.notebook.AddPage(self.ePage, "Types + Users")

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
	version = "0.0.1"
	title   = "FINally v" + version
	
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
	
	# create highest level wx object (wxApp) instance
	launcher = AppLauncher(redirect=False) 
	launcher.Main()
