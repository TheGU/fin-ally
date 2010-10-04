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
MENU_STYLE_XP       = wx.NewId()
MENU_STYLE_2007     = wx.NewId()
MENU_STYLE_MY       = wx.NewId()
MENU_USE_CUSTOM     = wx.NewId()
MENU_HELP           = wx.NewId()
MENU_TRANSPARENCY   = wx.NewId()
MENU_NEW_FILE       = 10005
MENU_SAVE           = 10006
MENU_OPEN_FILE      = 10007
MENU_NEW_FOLDER     = 10008
MENU_COPY           = 10009
MENU_CUT            = 10010
MENU_PASTE          = 10011
MENU_QUIT           = 10012

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
    styleMenu    = FM.FlatMenu()
    editMenu     = FM.FlatMenu()
    multipleMenu = FM.FlatMenu()
    subMenu      = FM.FlatMenu()
    helpMenu     = FM.FlatMenu()

    self.newMyTheme = ArtManager.Get().AddMenuTheme(FM_MyRenderer())
    ArtManager.Get().SetMenuTheme(self.newMyTheme)

    # Load toolbar icons (32x32)
    copy_bmp        = wx.Bitmap(os.path.join(bitmapDir, "editcopy.png"),        wx.BITMAP_TYPE_PNG)
    cut_bmp         = wx.Bitmap(os.path.join(bitmapDir, "editcut.png"),         wx.BITMAP_TYPE_PNG)
    open_folder_bmp = wx.Bitmap(os.path.join(bitmapDir, "fileopen.png"),        wx.BITMAP_TYPE_PNG)
    new_file_bmp    = wx.Bitmap(os.path.join(bitmapDir, "filenew.png"),         wx.BITMAP_TYPE_PNG)
    new_folder_bmp  = wx.Bitmap(os.path.join(bitmapDir, "folder_new.png"),      wx.BITMAP_TYPE_PNG)
    save_bmp        = wx.Bitmap(os.path.join(bitmapDir, "filesave.png"),        wx.BITMAP_TYPE_PNG)
    colBmp          = wx.Bitmap(os.path.join(bitmapDir, "month-16.png"),        wx.BITMAP_TYPE_PNG)
    helpImg         = wx.Bitmap(os.path.join(bitmapDir, "help-16.png"),         wx.BITMAP_TYPE_PNG)
    ghostBmp        = wx.Bitmap(os.path.join(bitmapDir, "field-16.png"),        wx.BITMAP_TYPE_PNG)

    # Create toolbar icons
    #                        ID              Help Text      image object
    self.menuBar.AddTool(MENU_NEW_FILE,     "New File",     new_file_bmp)
    self.menuBar.AddSeparator()
    self.menuBar.AddTool(MENU_SAVE,         "Save File",    save_bmp)
    self.menuBar.AddTool(MENU_OPEN_FILE,    "Open File",    open_folder_bmp)
    self.menuBar.AddTool(MENU_NEW_FOLDER,   "New Folder",   new_folder_bmp)
    self.menuBar.AddTool(MENU_COPY,         "Copy",         copy_bmp)
    self.menuBar.AddTool(MENU_CUT,          "Cut",          cut_bmp)
    self.menuBar.AddTool(MENU_QUIT,         "Quit",         cut_bmp)

    # 
    # Create File Menu
    #
    item = FM.FlatMenuItem(fileMenu, MENU_NEW_FILE, "&New File\tCtrl+N", "New File", wx.ITEM_NORMAL)
    fileMenu.AppendItem(item)

    item = FM.FlatMenuItem(fileMenu, MENU_SAVE, "&Save File\tCtrl+S", "Save File", wx.ITEM_NORMAL)
    fileMenu.AppendItem(item)
    
    item = FM.FlatMenuItem(fileMenu, MENU_OPEN_FILE, "&Open File\tCtrl+O", "Open File", wx.ITEM_NORMAL)
    fileMenu.AppendItem(item)
    
    item = FM.FlatMenuItem(fileMenu, MENU_NEW_FOLDER, "N&ew Folder\tCtrl+E", "New Folder", wx.ITEM_NORMAL)
    fileMenu.AppendItem(item)
    
    item = FM.FlatMenuItem(fileMenu, MENU_COPY, "&Copy\tCtrl+C", "Copy", wx.ITEM_NORMAL)
    fileMenu.AppendItem(item)
    
    item = FM.FlatMenuItem(fileMenu, MENU_CUT, "Cut\tCtrl+X", "Cut", wx.ITEM_NORMAL)
    fileMenu.AppendItem(item)
    
    item = FM.FlatMenuItem(fileMenu, MENU_QUIT, "Quit\tCtrl+Q", "Quit", wx.ITEM_NORMAL)
    fileMenu.AppendItem(item)

    # 
    # Create Style Menu
    #
    item = FM.FlatMenuItem(styleMenu, MENU_STYLE_MY, "Menu style Custom (Default)\tAlt+N", "Menu style Custom (Default)", wx.ITEM_RADIO)
    styleMenu.AppendItem(item)
    
    item = FM.FlatMenuItem(styleMenu, MENU_STYLE_XP, "Menu style XP\tAlt+P", "Menu style XP", wx.ITEM_RADIO)        
    styleMenu.AppendItem(item)

    item = FM.FlatMenuItem(styleMenu, MENU_STYLE_2007, "Menu style 2007\tAlt+V", "Menu style 2007", wx.ITEM_RADIO)
    styleMenu.AppendItem(item)
    
    item.Check(True) # applying check-mark

    item = FM.FlatMenuItem(styleMenu, MENU_USE_CUSTOM, "Show Customize DropDown", "Shows the customize drop down arrow", wx.ITEM_CHECK)
    styleMenu.AppendItem(item)
    
    # 
    # Create Edit Menu
    #

    # edit menu with icon
    item = FM.FlatMenuItem(editMenu, MENU_TRANSPARENCY, "Set FlatMenu transparency...", "Sets the FlatMenu transparency",
                           wx.ITEM_NORMAL, None, ghostBmp)
    editMenu.AppendItem(item)

    # Add some dummy entries to the sub menu
    # Add sub-menu to main menu
    item = FM.FlatMenuItem(editMenu, 9001, "Sub-&menu items", "", wx.ITEM_NORMAL, subMenu)
    editMenu.AppendItem(item)

    # Create the submenu items and add them 
    item = FM.FlatMenuItem(subMenu, 9002, "&Sub-menu Item 1", "", wx.ITEM_NORMAL)
    subMenu.AppendItem(item)

    item = FM.FlatMenuItem(subMenu, 9003, "Su&b-menu Item 2", "", wx.ITEM_NORMAL)
    subMenu.AppendItem(item)

    # 
    # Create Multiple Menu
    #
    maxItems = 17
    numCols = 2
    switch = int(math.ceil(maxItems/float(numCols)))
    
    for i in xrange(17):
        row, col = i%switch, i/switch
        bmp = (random.randint(0, 1) == 1 and [colBmp] or [wx.NullBitmap])[0]
        item = FM.FlatMenuItem(multipleMenu, wx.ID_ANY, "Row %d, Col %d"%((row+1, col+1)), "", wx.ITEM_NORMAL, None, bmp)
        multipleMenu.AppendItem(item)

    multipleMenu.SetNumberColumns(2)

    # 
    # Create Help Menu
    #
    item = FM.FlatMenuItem(helpMenu, MENU_HELP, "&About\tCtrl+A", "About...", wx.ITEM_NORMAL, None, helpImg)
    helpMenu.AppendItem(item)

    # Add menu to the menu bar
    self.menuBar.Append(fileMenu,       "&File")
    self.menuBar.Append(styleMenu,      "&Style")
    self.menuBar.Append(editMenu,       "&Edit")
    self.menuBar.Append(multipleMenu,   "&Multiple Columns")
    self.menuBar.Append(helpMenu,       "&Help")
    
    ConnectMenuBar(self)
    
def ConnectMenuBar(self):
    # Attach menu events to some handlers
    #            event                     function               menu item ID               seocndary menu item ID
    self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnQuit,           id=MENU_QUIT)
    self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnStyle,          id=MENU_STYLE_XP,           id2=MENU_STYLE_2007)
    self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnAbout,          id=MENU_HELP)
    self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnStyle,          id=MENU_STYLE_MY)
    self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnTransparency,   id=MENU_TRANSPARENCY)
    self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnFlatMenuCmd,    id=MENU_NEW_FILE,           id2=20013)
    
    if "__WXMAC__" in wx.Platform:
        self.Bind(wx.EVT_SIZE, self.OnSize)
    
#***********************************
#         Event Handlers
#***********************************

#def OnSize(event):
#    print "MenuBar OnSize"
#    self._mgr.Update()
#    self.Layout()
#    
#def OnQuit(self, event):
#    print "MenuBar OnQuit"
#    self._mgr.UnInit()
#    self.Destroy()
#    
#def OnStyle(self, event):
#
#    eventId = event.GetId()
#    
#    if eventId == MENU_STYLE_2007:
#        ArtManager.Get().SetMenuTheme(FM.Style2007)
#    elif eventId == MENU_STYLE_XP:
#        ArtManager.Get().SetMenuTheme(FM.StyleXP)
#    elif eventId == MENU_STYLE_MY:
#        ArtManager.Get().SetMenuTheme(self.newMyTheme)
#
#    self.menuBar.Refresh()
#    self.Update()        
#
#def OnTransparency(self, event):
#
#    transparency = ArtManager.Get().GetTransparency()
#    dlg = wx.TextEntryDialog(self, 'Please enter a value for menu transparency',
#                             'FlatMenu Transparency', str(transparency))
#
#    if dlg.ShowModal() != wx.ID_OK:
#        dlg.Destroy()
#        return
#
#    value = dlg.GetValue()
#    dlg.Destroy()
#    
#    try:
#        value = int(value)
#    except:
#        dlg = wx.MessageDialog(self, "Invalid transparency value!", "Error",
#                               wx.OK | wx.ICON_ERROR)
#        dlg.ShowModal()
#        dlg.Destroy()
#
#    if value < 0 or value > 255:
#        dlg = wx.MessageDialog(self, "Invalid transparency value!", "Error",
#                               wx.OK | wx.ICON_ERROR)
#        dlg.ShowModal()
#        dlg.Destroy()
#        
#    ArtManager.Get().SetTransparency(value)
#
#def OnFlatMenuCmd(self, event):
#
#    self.log.write("Received Flat menu command event ID: %d\n"%(event.GetId()))
#
#def OnAbout(self, event):
#
#    msg = "This is the About Dialog of the FlatMenu demo.\n\n" + \
#          "Author: Andrea Gavana @ 03 Nov 2006\n\n" + \
#          "Please report any bug/requests or improvements\n" + \
#          "to Andrea Gavana at the following email addresses:\n\n" + \
#          "andrea.gavana@gmail.com\ngavana@kpo.kz\n\n" + \
#          "Welcome to wxPython " + wx.VERSION_STRING + "!!"
#          
#    dlg = wx.MessageDialog(self, msg, "FlatMenu wxPython Demo",
#                           wx.OK | wx.ICON_INFORMATION)
#    dlg.ShowModal()
#    dlg.Destroy()