#!/usr/bin/env python

#********************************************************************
# Filename:            menuBar.py
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
import math
import random
import os
import sys

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


bitmapDir = 'img/'

#********************************************************************
# menu IDs
#********************************************************************
MENU_HELP           = wx.NewId()
MENU_PREFS          = wx.NewId()
MENU_NEW_DB         = wx.NewId()
MENU_OPEN_DB        = wx.NewId()
MENU_QUIT           = wx.NewId()
MENU_NEW_EXPENSE    = wx.NewId()

#********************************************************************
def switchRGBtoBGR(colour):
    return wx.Colour(colour.Blue(), colour.Green(), colour.Red())

#********************************************************************
class FM_MyRenderer(RendererBase):
    """ My custom style. """
    
    def __init__(self):
        RendererBase.__init__(self)

    def DrawButton(self, dc, rect, state, useLightColours=True):

        if state == ControlFocus:
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().BackgroundColour())
        elif state == ControlPressed:
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().HighlightBackgroundColour())
        else:   # ControlNormal, ControlDisabled, default
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().BackgroundColour())

        # Draw the button borders
        dc.SetPen(wx.Pen(penColour))
        dc.SetBrush(wx.Brush(brushColour))
        dc.DrawRoundedRectangle(rect.x, rect.y, rect.width, rect.height,4)

    def DrawMenuBarBg(self, dc, rect):

        # For office style, we simple draw a rectangle with a gradient colouring
        vertical = ArtManager.Get().GetMBVerticalGradient()

        dcsaver = DCSaver(dc)

        # fill with gradient
        startColour = ArtManager.Get().GetMenuBarFaceColour()
        endColour   = ArtManager.Get().LightColour(startColour, 90)

        dc.SetPen(wx.Pen(endColour))
        dc.SetBrush(wx.Brush(endColour))
        dc.DrawRectangleRect(rect)

    def DrawToolBarBg(self, dc, rect):
        if not ArtManager.Get().GetRaiseToolbar():
            return

        # fill with gradient
        startColour = ArtManager.Get().GetMenuBarFaceColour()
        dc.SetPen(wx.Pen(startColour))
        dc.SetBrush(wx.Brush(startColour))
        dc.DrawRectangle(0, 0, rect.GetWidth(), rect.GetHeight())
        
def CreateMenu(self):
    # define the menuBar object
    self.menuBar = FM.FlatMenuBar(self, 
                                wx.ID_ANY, 
                                32, 
                                5, 
                                options = FM_OPT_SHOW_TOOLBAR | FM_OPT_SHOW_CUSTOMIZE)
    
    fileMenu     = FM.FlatMenu()
    optionMenu   = FM.FlatMenu()
    helpMenu     = FM.FlatMenu()

    self.newMyTheme = ArtManager.Get().AddMenuTheme(FM_MyRenderer())
    
    # Set the menubar theme - refer to the wxPython demo for more options
    ArtManager.Get().SetMenuTheme(FM.Style2007)

    # Load toolbar icons (32x32)
    new_expense     = wx.Bitmap(os.path.join(bitmapDir, "new_expense.png"),     wx.BITMAP_TYPE_PNG)
    help_blue       = wx.Bitmap(os.path.join(bitmapDir, "blueHelp_16.png"),     wx.BITMAP_TYPE_PNG)
    exit_red        = wx.Bitmap(os.path.join(bitmapDir, "exit.png"),            wx.BITMAP_TYPE_PNG)

    # Create toolbar icons
    #                        ID              Help Text      image object
    self.menuBar.AddTool(MENU_NEW_EXPENSE,  "New Expense",     new_expense)
    self.menuBar.AddSeparator()
    self.menuBar.AddTool(MENU_QUIT,         "Quit",            exit_red)

    # 
    # Create File Menu
    #
    item = FM.FlatMenuItem(fileMenu, MENU_NEW_DB, "&New Database\tCtrl+N", "New Database", wx.ITEM_NORMAL)
    fileMenu.AppendItem(item)
    
    item = FM.FlatMenuItem(fileMenu, MENU_OPEN_DB, "&Open Database\tCtrl+O", "Open Database", wx.ITEM_NORMAL)
    fileMenu.AppendItem(item)
    
    item = FM.FlatMenuItem(fileMenu, MENU_QUIT, "Quit\tCtrl+Q", "Quit", wx.ITEM_NORMAL)
    fileMenu.AppendItem(item)
    
    #
    # Create Options Menu
    #
    item = FM.FlatMenuItem(optionMenu, MENU_PREFS, "&Preferences\tCtrl+P", "Preferences", wx.ITEM_NORMAL)
    optionMenu.AppendItem(item)
    
    # 
    # Create Help Menu
    #
    item = FM.FlatMenuItem(helpMenu, MENU_HELP, "&About\tCtrl+A", "About...", wx.ITEM_NORMAL, None, help_blue)
    helpMenu.AppendItem(item)

    # Add menu to the menu bar
    self.menuBar.Append(fileMenu,       "&File")
    self.menuBar.Append(optionMenu,     "&Options")
    self.menuBar.Append(helpMenu,       "&Help")
    
    ConnectMenuBar(self)
    
def ConnectMenuBar(self):
    # Attach menu events to some handlers
    #            event                     function               menu item ID
    self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnAbout,          id=MENU_HELP)
    self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.gPage.ShowNewExpenseDialogue, id=MENU_NEW_EXPENSE) 
    self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnQuit,           id=MENU_QUIT)
    
    # unsupported as of right now 
    self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnPrefs,          id=MENU_PREFS)      # TODO
    self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnUnsupported,    id=MENU_NEW_DB)     # TODO
    self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnUnsupported,    id=MENU_OPEN_DB)    # TODO
    
    
    
    
    
    
    
    