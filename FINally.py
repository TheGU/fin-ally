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
import cfg
import os
from datetime import date, datetime
from database import *
from wx._core import WXK_F1, WXK_F2
from grid import GraphicsGrid
from statusBar import CustomStatusBar
from menuBar import CreateMenu
from prefs import EditPreferences, SaveWindowPreferences
from filterControl import CustomFilterPanel
from expenseDialogue import NewExpenseDialog
from expenseTypeDialog import expenseTypeDialog
from userDialog import userDialog

try:
	from agw import flatmenu as FM
	from agw.artmanager import ArtManager, RendererBase, DCSaver
	from agw.fmresources import ControlFocus, ControlPressed
	from agw.fmresources import FM_OPT_SHOW_CUSTOMIZE, FM_OPT_SHOW_TOOLBAR, FM_OPT_MINIBAR
except ImportError: # if it's not there locally, try the wxPython lib.
	import wx.lib.agw.flatmenu as FM
	from wx.lib.agw.artmanager import ArtManager, RendererBase, DCSaver
	from wx.lib.agw.fmresources import ControlFocus, ControlPressed
	from wx.lib.agw.fmresources import FM_OPT_SHOW_CUSTOMIZE, FM_OPT_SHOW_TOOLBAR, FM_OPT_MINIBAR

import wx.aui as AUI
AuiPaneInfo = AUI.AuiPaneInfo
AuiManager  = AUI.AuiManager

# The recommended way to use wx with mpl is with the WXAgg
# backend. 
#
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

#********************************************************************
# FINally class definitions
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
		self.userList		= self.database.GetSimpleUserList()
		self.typeList		= self.database.GetExpenseTypeList()
		
		# create a sizer for this Panel and add the buttons and the table
		self.sizer = wx.BoxSizer(wx.VERTICAL)      # define new box sizer	
		self.sizer.Add(self.grid, 1, wx.GROW)     # add grid (resize vert and horz)
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
class PlotPage(wx.Panel):
	"""
	Class Name: 	GraphicsPage
	Extends: 		wx.Panel
	Description:	The Graphics page contains two things - a grid or table of entries, 
	and a button panel to perform some operations on the grid.
	"""
	
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		
		self.data = [5, 6, 9, 14]		
		self.create_main_panel()
		self.draw_figure()
		
	def create_main_panel(self):
		
		# Create the mpl Figure and FigCanvas objects. 
		# 5x4 inches, 100 dots-per-inch
		#
		self.dpi = 100
		self.fig = Figure((5.0, 4.0), dpi=self.dpi)
		self.canvas = FigCanvas(self, -1, self.fig)
		
		# Since we have only one plot, we can use add_axes 
		# instead of add_subplot, but then the subplot
		# configuration tool in the navigation toolbar wouldn't
		# work.
		self.axes = self.fig.add_subplot(111)
		
		# Bind the 'pick' event for clicking on one of the bars
		self.canvas.mpl_connect('pick_event', self.on_pick)
		
		self.textbox = wx.TextCtrl(
			self, 
			size=(200,-1),
			style=wx.TE_PROCESS_ENTER)
		self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter, self.textbox)
		
		self.drawbutton = wx.Button(self, -1, "Draw!")
		self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton)

		self.cb_grid = wx.CheckBox(self, -1, 
			"Show Grid",
			style=wx.ALIGN_RIGHT)
		self.Bind(wx.EVT_CHECKBOX, self.on_cb_grid, self.cb_grid)

		self.slider_label = wx.StaticText(self, -1, 
			"Bar width (%): ")
		self.slider_width = wx.Slider(self, -1, 
			value=20, 
			minValue=1,
			maxValue=100,
			style=wx.SL_AUTOTICKS | wx.SL_LABELS)
		self.slider_width.SetTickFreq(10, 1)
		self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.on_slider_width, self.slider_width)

		# Create the navigation toolbar, tied to the canvas
		#
		self.toolbar = NavigationToolbar(self.canvas)
		
		#
		# Layout with box sizers
		#
		
		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
		self.vbox.Add(self.toolbar, 0, wx.EXPAND)
		self.vbox.AddSpacer(10)
		
		self.hbox = wx.BoxSizer(wx.HORIZONTAL)
		flags = wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL
		self.hbox.Add(self.textbox, 0, border=3, flag=flags)
		self.hbox.Add(self.drawbutton, 0, border=3, flag=flags)
		self.hbox.Add(self.cb_grid, 0, border=3, flag=flags)
		self.hbox.AddSpacer(30)
		self.hbox.Add(self.slider_label, 0, flag=flags)
		self.hbox.Add(self.slider_width, 0, border=3, flag=flags)
		
		self.vbox.Add(self.hbox, 0, flag = wx.ALIGN_LEFT | wx.TOP)
		
		self.SetSizer(self.vbox)
		self.vbox.Fit(self)

	def draw_figure(self):
		""" Redraws the figure
		"""
		str = self.textbox.GetValue()
		self.data = map(int, str.split())
		x = range(len(self.data))

		# clear the axes and redraw the plot anew
		#
		self.axes.clear()		
		self.axes.grid(self.cb_grid.IsChecked())
		
		self.axes.bar(
			left=x, 
			height=self.data, 
			width=self.slider_width.GetValue() / 100.0, 
			align='center', 
			alpha=0.44,
			picker=5)
		
		self.canvas.draw()
	
	def on_cb_grid(self, event):
		self.draw_figure()
	
	def on_slider_width(self, event):
		self.draw_figure()
	
	def on_draw_button(self, event):
		self.draw_figure()
	
	def on_pick(self, event):
		# The event received here is of the type
		# matplotlib.backend_bases.PickEvent
		#
		# It carries lots of information, of which we're using
		# only a small amount here.
		# 
		box_points = event.artist.get_bbox().get_points()
		msg = "You've clicked on a bar with coords:\n %s" % box_points
		
		dlg = wx.MessageDialog(
			self, 
			msg, 
			"Click!",
			wx.OK | wx.ICON_INFORMATION)

		dlg.ShowModal() 
		dlg.Destroy()		
	
	def on_text_enter(self, event):
		self.draw_figure()

	def on_save_plot(self, event):
		file_choices = "PNG (*.png)|*.png"
		
		dlg = wx.FileDialog(
			self, 
			message="Save plot as...",
			defaultDir=os.getcwd(),
			defaultFile="plot.png",
			wildcard=file_choices,
			style=wx.SAVE)
		
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			self.canvas.print_figure(path, dpi=self.dpi)
			self.flash_status_message("Saved to %s" % path)
		
	def on_exit(self, event):
		self.Destroy()
		
	def on_about(self, event):
		msg = """ A demo using wxPython with matplotlib:
		
		 * Use the matplotlib navigation bar
		 * Add values to the text box and press Enter (or click "Draw!")
		 * Show or hide the grid
		 * Drag the slider to modify the width of the bars
		 * Save the plot to a file using the File menu
		 * Click on a bar to receive an informative message
		"""
		dlg = wx.MessageDialog(self, msg, "About", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()
	
	def flash_status_message(self, msg, flash_len_ms=1500):
		self.statusbar.SetStatusText(msg)
		self.timeroff = wx.Timer(self)
		self.Bind(
			wx.EVT_TIMER, 
			self.on_flash_status_off, 
			self.timeroff)
		self.timeroff.Start(flash_len_ms, oneShot=True)
	
	def on_flash_status_off(self, event):
		self.statusbar.SetStatusText('')

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

		# define AUI manager
		self._mgr = AuiManager()
		self._mgr.SetManagedWindow(self)
		
		self.database = Database()
		
		# add an icon!
		self.icon = wx.Icon("img/FINally.png", wx.BITMAP_TYPE_PNG)
		self.SetIcon(self.icon)
		
		self.sb = CustomStatusBar(self)
		self.SetStatusBar(self.sb)
		
		self.panel    = wx.Panel(self) # basically just a container for the notebook
		self.notebook = wx.Notebook(self.panel, size=AppMainFrame.size)

		self.gPage = GraphicsPage(self.notebook)
		self.notebook.AddPage(self.gPage, "Grid")
		self.pPage = PlotPage(self.notebook)
		self.notebook.AddPage(self.pPage, "Plot")

		# populate and connect the menuBar
		CreateMenu(self)
		
		# Create the filter panel
		self.filterPanel = CustomFilterPanel(self.panel)

		# arrange notebook windows in a simple box sizer
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.notebook, 1, wx.EXPAND)
		self.sizer.Add(self.filterPanel, 0, wx.ALIGN_BOTTOM)
		self.panel.SetSizer(self.sizer)
		
		# support for AUI content
		self._mgr.AddPane(self.panel, AuiPaneInfo().Name("main_panel").CenterPane())
		self.menuBar.PositionAUI(self._mgr)
		self._mgr.Update()
		
		ArtManager.Get().SetMBVerticalGradient(True)
		ArtManager.Get().SetRaiseToolbar(False)

		self.menuBar.Refresh()

	def SetBackgroundColor(self, colorString):
		self.SetBackgroundColour(colorString)
		
	def OnQuit(self, event):
		localSize = self.GetSize()
		SaveWindowPreferences(localSize[0], localSize[1])
		self._mgr.UnInit()
		self.Destroy()  
		
	def OnPrefs(self, event):
		EditPreferences(self, event)  

	def OnAbout(self, event):
		msg = "Welcome to FINally!\n\n" + \
		      "Author: Daniel LaBeau Sisco @ 10/10/2010\n\n" + \
		      "Please report any bug/requests or improvements\n" + \
		      "to Daniel Sisco at the following email address:\n\n" + \
		      "daniel.sisco@gmail.com\n\n" + \
		      "Please visit FINally at http://code.google.com/p/fin-ally/ for more information\n"

		dlg = wx.MessageDialog(self, msg, "About FINally",
		                       wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
		
	def OnUnsupported(self, event):
		msg = "...this feature is unsupported!\n You should complain to Daniel Sisco at the following email address:\n\n" + \
			  "daniel.sisco@gmail.com\n\n"
		dlg = wx.MessageDialog(self, msg, "Sorry...",
							wx.OK)
		dlg.ShowModal()
		dlg.Destroy()
		
	def OnEditExpenseType(self, event):
		dlg = expenseTypeDialog(self, -1, 'Edit Expense Types')
		dlg.ShowModal()
		dlg.Destroy()
		
	def OnEditUser(self, event):
		dlg = userDialog(self, -1, 'Edit Users')
		dlg.ShowModal()
		dlg.Destroy()

#********************************************************************
class AppLauncher(wx.App):
	"""This class inherits wx.App methods, and should be the first object created during FINally
	operation. This will be the only instance of an application class and will contain the primary
	Frame (top level window)."""
	
	# static variables go here
	title   = "FINally v%s.%s.%s" % (cfg.VERSION[0], cfg.VERSION[1], cfg.VERSION[2])

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
	
	# perform database migrations if necessary - passing the version the application 
	# will be working with to the migration script (ie: schemaVersion)
	schemaVersion = "%s_%s" % (dbVer[0], dbVer[1]) # reformatting needed for passing via CLI
	string = "python migrate.py %s" % (schemaVersion)
	print "executing command: \n>", string
	os.system(string)
	
	# create an instance of the Database class and then perform the initial database ID
	db = Database();
	db.Create() #TODO: move this into a database __init__ function?
	
	# create highest level wx object (wxApp) instance
	launcher = AppLauncher(redirect=False) 
	launcher.Main()
