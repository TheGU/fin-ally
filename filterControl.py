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

class CustomFilterPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, size=(900,100))

        wx.StaticText(self, -1, "This is a wx.Slider.", (0,0))

        slider = wx.Slider(self, 
                           100, # id
                           25,  # default
                           1,   # min
                           100,# max
                           (1,100), # pos
                           (250, -1),# size
                           wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)

        slider.SetTickFreq(5, 5)