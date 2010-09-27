#!/usr/bin/env python

#********************************************************************
# Filename:        prefPage.py
# Authors:         Daniel Sisco
# Date Created:    9-25-2010
# 
# Abstract: This page is responsible for allowing the operator to modify
# preference values for the FINally app. 
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

#********************************************************************
class PrefPage(wx.Panel):
    """The Preference Page allows the operator to select preferences for several
    common things: default User, ExpenseType, etc... """
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.SetBackgroundColour("BLUE")
        
        self.database       = Database()
        self.userList        = self.database.GetSimpleUserList()
        self.typeList        = self.database.GetExpenseTypeList()
        
        self.sizer        = wx.BoxSizer(wx.VERTICAL)  # define new box sizer    
        self.buttonPanel  = wx.Panel(self)            # create a panel for the buttons
        
        # create and bind a user selection box
        self.userSelect   = wx.ComboBox(self.buttonPanel, 
                                        id=-1,
                                        value=self.userList[0],
                                        choices=self.userList,
                                          pos=(100,0), 
                                          style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.OnUserSelect, self.userSelect)
        
        # create and bind a type selection box
        self.typeSelect      = wx.ComboBox(self.buttonPanel, 
                                        id=-1,
                                        value=self.typeList[0],
                                        choices=self.typeList,
                                          pos=(200,0), 
                                          style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.OnTypeSelect, self.typeSelect)
        
        # create and bind a calendar box
        self.cal           = callib.CalendarCtrl(self.buttonPanel, 
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