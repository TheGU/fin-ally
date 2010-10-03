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
import cfg
from datetime import date, datetime
from database import *

class CustomStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)

        self.database = Database()
        
        # This status bar has three fields
        self.SetFieldsCount(3)
        # Sets the three fields to be relative widths to each other.
        self.SetStatusWidths([-2, -2, -1])

        self.SetStatusText("ONE", 0)
        self.SetStatusText("TWO", 1)
        self.versionString = "FINally v%s.%s | database v%s.%s" % (cfg.VERSION[0], 
                                                                                cfg.VERSION[1],
                                                                                self.database.GetVersion()[0],
                                                                                self.database.GetVersion()[1])
        self.SetStatusText(self.versionString, 2)    