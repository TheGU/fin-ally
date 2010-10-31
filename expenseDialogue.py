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
import wx.calendar as callib
import cfg
import os
from datetime import date, datetime
from database import *
    
class NewExpenseDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: NewExpenseDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.CalSizer_staticbox = wx.StaticBox(self, -1, "Expense Date")
        self.ExpenseStaticSizer_staticbox = wx.StaticBox(self, -1, "Expense Info")
        self.UserSizer_staticbox = wx.StaticBox(self, -1, "User")
        self.userControl = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN)
        self.calendarControl = callib.CalendarCtrl(self, -1)
        self.amountText = wx.StaticText(self, -1, "amount")
        self.amountControl = wx.TextCtrl(self, -1, "")
        self.expenseTypeText = wx.StaticText(self, -1, "expense type")
        self.expenseTypeControl = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN)
        self.descriptionText = wx.StaticText(self, -1, "description")
        self.descriptionControl = wx.TextCtrl(self, -1, "")
        self.okButton = wx.Button(self, wx.ID_OK, "")
        self.cancelButton = wx.Button(self, wx.ID_CANCEL, "")
    
        self.__set_properties()
        self.__do_layout()
    
        self.Bind(wx.EVT_COMBOBOX, self.OnUserSelect, self.userControl)
        self.Bind(wx.EVT_TEXT, self.OnValueEntry, self.amountControl)
        self.Bind(wx.EVT_COMBOBOX, self.OnTypeSelect, self.expenseTypeControl)
        self.Bind(wx.EVT_TEXT, self.OnDescEntry, self.descriptionControl)
        self.Bind(wx.EVT_BUTTON, self.OnOkButton, self.okButton)
        self.Bind(wx.EVT_BUTTON, self.onCancelButton, self.cancelButton)
        # end wxGlade
    
    def __set_properties(self):
        # begin wxGlade: NewExpenseDialog.__set_properties
        self.SetTitle("dialog_2")
        self.amountText.SetMinSize((50, -1))
        self.amountControl.SetMinSize((150, -1))
        self.expenseTypeText.SetMinSize((50, -1))
        self.expenseTypeControl.SetMinSize((150, -1))
        self.descriptionText.SetMinSize((50, -1))
        self.descriptionControl.SetMinSize((150, -1))
        self.okButton.SetDefault()
        # end wxGlade
    
    def __do_layout(self):
        # begin wxGlade: NewExpenseDialog.__do_layout
        VerticalSizer = wx.BoxSizer(wx.VERTICAL)
        ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        ExpenseSizer = wx.BoxSizer(wx.HORIZONTAL)
        ExpenseStaticSizer = wx.StaticBoxSizer(self.ExpenseStaticSizer_staticbox, wx.HORIZONTAL)
        ExpenseGridSizer = wx.GridSizer(3, 2, 0, 0)
        CalSizer = wx.StaticBoxSizer(self.CalSizer_staticbox, wx.HORIZONTAL)
        UserSizer = wx.StaticBoxSizer(self.UserSizer_staticbox, wx.HORIZONTAL)
        UserSizer.Add(self.userControl, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        VerticalSizer.Add(UserSizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        CalSizer.Add(self.calendarControl, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        VerticalSizer.Add(CalSizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        ExpenseGridSizer.Add(self.amountText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        ExpenseGridSizer.Add(self.amountControl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        ExpenseGridSizer.Add(self.expenseTypeText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        ExpenseGridSizer.Add(self.expenseTypeControl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        ExpenseGridSizer.Add(self.descriptionText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        ExpenseGridSizer.Add(self.descriptionControl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        ExpenseStaticSizer.Add(ExpenseGridSizer, 0, wx.EXPAND, 0)
        ExpenseSizer.Add(ExpenseStaticSizer, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        VerticalSizer.Add(ExpenseSizer, 0, wx.TOP|wx.EXPAND, 5)
        sizer_1.Add(self.okButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_1.Add(self.cancelButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        ButtonSizer.Add(sizer_1, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        VerticalSizer.Add(ButtonSizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(VerticalSizer)
        VerticalSizer.Fit(self)
        self.Layout()
        # end wxGlade
    
    def OnUserSelect(self, event): # wxGlade: NewExpenseDialog.<event_handler>
        print "Event handler `OnUserSelect' not implemented"
        event.Skip()
    
    def OnCalSelChanged(self, event): # wxGlade: NewExpenseDialog.<event_handler>
        print "Event handler `OnCalSelChanged' not implemented"
        event.Skip()
    
    def OnValueEntry(self, event): # wxGlade: NewExpenseDialog.<event_handler>
        print "Event handler `OnValueEntry' not implemented"
        event.Skip()
    
    def OnTypeSelect(self, event): # wxGlade: NewExpenseDialog.<event_handler>
        print "Event handler `OnTypeSelect' not implemented"
        event.Skip()
    
    def OnDescEntry(self, event): # wxGlade: NewExpenseDialog.<event_handler>
        print "Event handler `OnDescEntry' not implemented"
        event.Skip()
    
    def OnOkButton(self, event): # wxGlade: NewExpenseDialog.<event_handler>
        print "Event handler `OnOkButton' not implemented"
        event.Skip()
    
    def onCancelButton(self, event): # wxGlade: NewExpenseDialog.<event_handler>
        print "Event handler `onCancelButton' not implemented"
        event.Skip()