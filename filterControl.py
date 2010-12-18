#!/usr/bin/env python

#********************************************************************
# Filename:            filterControl.py
# Authors:             Daniel Sisco
# Date Created:        10-3-2010
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

import wx
import wx.calendar as callib
import wx.grid     as gridlib
from utils import monthDict, BLANK_TERM
from grid import CustomDataTable
from database import FilterTerms, Database
from datetime import datetime

class CustomFilterPanel(wx.Frame):
    def __init__(self, parent, *args, **kwds):
        # begin wxGlade: CustomFilterPanel.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, parent, *args, **kwds)
        self.searchSizer_staticbox = wx.StaticBox(self, -1, "search")
        self.reservedSizer_staticbox = wx.StaticBox(self, -1, " reserved")
        self.filterSizer_staticbox = wx.StaticBox(self, -1, "date filter")
        self.startMonthText = wx.StaticText(self, -1, "start date", style=wx.ALIGN_CENTRE)
        self.startDateCombo = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN)
        self.dateRangeText = wx.StaticText(self, -1, "date range", style=wx.ALIGN_CENTRE)
        self.searchText = wx.StaticText(self, -1, "search expenses", style=wx.ALIGN_CENTRE)
        self.searchTypeText = wx.StaticText(self, -1, "search type", style=wx.ALIGN_CENTRE)
        
        #**** ADDED ****
        self.database = Database()
        self.bufferSize = (15,15)
        self.parent = parent
        self.dataTable = CustomDataTable(gridlib.Grid)
        
        # values populated by controls in this panel - consumed by the application
        self.startMonth = "January"
        self.monthRange = 1
        self.searchTerm = ""
        
        self.filterTerms = FilterTerms()
        #**** END ADD ****

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: CustomFilterPanel.__set_properties
        self.SetTitle("frame_1")
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: CustomFilterPanel.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        filterPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        reservedSizer = wx.StaticBoxSizer(self.reservedSizer_staticbox, wx.HORIZONTAL)
        searchSizer = wx.StaticBoxSizer(self.searchSizer_staticbox, wx.HORIZONTAL)
        searchSizerRight = wx.BoxSizer(wx.VERTICAL)
        searchSizerLeft = wx.BoxSizer(wx.VERTICAL)
        filterSizer = wx.StaticBoxSizer(self.filterSizer_staticbox, wx.HORIZONTAL)
        filterSizerRight = wx.BoxSizer(wx.VERTICAL)
        filterSizerLeft = wx.BoxSizer(wx.VERTICAL)
        filterSizerLeft.Add(self.startMonthText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        filterSizerLeft.Add(self.startDateCombo, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        filterSizer.Add(filterSizerLeft, 1, wx.EXPAND, 0)
        filterSizerRight.Add(self.dateRangeText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        filterSizer.Add(filterSizerRight, 1, wx.EXPAND, 0)
        filterPanelSizer.Add(filterSizer, 1, wx.RIGHT|wx.EXPAND, 5)
        searchSizerLeft.Add(self.searchText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        searchSizer.Add(searchSizerLeft, 1, wx.EXPAND, 0)
        searchSizerRight.Add(self.searchTypeText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        searchSizer.Add(searchSizerRight, 1, wx.EXPAND, 0)
        filterPanelSizer.Add(searchSizer, 1, wx.EXPAND, 0)
        filterPanelSizer.Add(reservedSizer, 1, wx.LEFT|wx.EXPAND, 5)
        sizer_1.Add(filterPanelSizer, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade


class CustomFilterPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        
        self.database = Database()
        self.bufferSize = (15,15)
        self.parent = parent
        self.dataTable = CustomDataTable(gridlib.Grid)
        
        # values populated by controls in this panel - consumed by the application
        self.startMonth = "January"
        self.monthRange = 1
        self.searchTerm = ""
        
        self.filterTerms = FilterTerms()
        
        # create the month range static text
        self.monthRangeTextPanel = wx.Panel(self, -1)
        self.text1 = wx.StaticText(self.monthRangeTextPanel, -1, "number of months to display", (0, 0))
        
        # create the month range control
        self.monthRangePanel = wx.Panel(self, -1)
        self.slider = wx.Slider(self.monthRangePanel, 
                           100, # id
                           1,  # default
                           1,   # min
                           12,  # max
                           (0,10), # pos
                           (250, -1),# size
                           wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS )
        self.slider.SetTickFreq(1, 1)
        self.Bind(wx.EVT_SLIDER, self.OnMonthRange, self.slider)
        
        # populate the first sub-panel: month range selection
        self.vSizer1 = wx.BoxSizer(wx.VERTICAL)
        self.vSizer1.Add(self.monthRangeTextPanel, 0, wx.CENTER)
        self.vSizer1.Add(self.monthRangePanel, 0)
        
        # create the starting month static text
        self.startMonthTextPanel = wx.Panel(self, -1)
        self.text2 = wx.StaticText(self.startMonthTextPanel, -1, "starting month", (0,0))
        
        # create the start month control
        self.startMonthPanel = wx.Panel(self, -1)
        
        # this comboBox is based on monthDict, so find the current month key
        # in monthDict and use as default
        now = datetime.now()
        for key in monthDict:
            if(now.month == monthDict[key]):
                defaultMonth = key
        
        self.startMonthControl = wx.ComboBox(self.startMonthPanel, 
                                             -1, 
                                             defaultMonth,     # default
                                             (0, 30),   # pos 
                                             (160, -1), # size
                                             list(monthDict.keys()),
                                             wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.OnMonthStart, self.startMonthControl)
        
        # populate the second sub-panel: start month selection
        self.vSizer2 = wx.BoxSizer(wx.VERTICAL)
        self.vSizer2.Add(self.startMonthTextPanel, 0, wx.CENTER)
        self.vSizer2.Add(self.startMonthPanel, 0)
        
        # create the search static text
        self.searchTextPanel = wx.Panel(self, -1)
        self.text3 = wx.StaticText(self.searchTextPanel, -1, "search expenses", (0,0))
        
        # create the search control
        # NOTE: for some reason the search control doesn't take a panel as the parent, just 'self'
        self.search = wx.SearchCtrl(self, size=(200,-1), style=wx.TE_PROCESS_ENTER)
        self.search.ShowCancelButton(1)
        self.search.ShowSearchButton(1)
        
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch, self.search)
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancel, self.search)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSearch, self.search)
        
        # populate the third sub-panel: search control
        self.vSizer3 = wx.BoxSizer(wx.VERTICAL)
        self.vSizer3.Add(self.searchTextPanel, 0, wx.CENTER)
        self.vSizer3.Add(wx.Panel(self, -1, size = (self.bufferSize[0], self.bufferSize[1]*2)))
        self.vSizer3.Add(self.search, 0)
        
        # populate the overall horizontal panel
        self.hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizer.Add(wx.Panel(self, -1, size = self.bufferSize))
        self.hSizer.Add(self.vSizer2, 0)
        self.hSizer.Add(wx.Panel(self, -1, size = self.bufferSize))
        self.hSizer.Add(self.vSizer1, 0)
        self.hSizer.Add(wx.Panel(self, -1, size = self.bufferSize))
        self.hSizer.Add(self.vSizer3, 0, wx.ALIGN_RIGHT)
        
        self.SetSizer(self.hSizer)
        
    def OnSearch(self, event):
        localSearch = self.search.GetValue()
        
        # replace null match with "match anything"
        if(localSearch == ""):
            localSearch = BLANK_TERM
            
        self.filterTerms.SetSearchTerms(localSearch)
        self.dataTable.UpdateData()
        event.Skip()
        
    def OnCancel(self, event):
        self.search.SetValue("")
        self.filterTerms.SetSearchTerms(BLANK_TERM)
        self.dataTable.UpdateData()
        event.Skip()
        
    def OnMonthStart(self, event):
        self.filterTerms.SetStartMonth(monthDict[self.startMonthControl.GetValue()])
        self.dataTable.UpdateData()
        event.Skip()
        
    def OnMonthRange(self, event):
        self.filterTerms.SetMonthRange(self.slider.GetValue())
        self.dataTable.UpdateData()
        event.Skip()