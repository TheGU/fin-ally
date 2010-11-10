#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Fri Nov 05 18:46:37 2010

import wx
import wx.grid

# begin wxGlade: extracode
# end wxGlade



class userDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: userDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        #**** BEGIN ADD ****
        self.database = Database()
        self.userChoices = self.database.GetSimpleUserList()
        self.newUserText = "new user full name..."
        
        self.deleteSizer_staticbox = wx.StaticBox(self, -1, "Delete Existing Users")
        self.newTypeSizer_staticbox = wx.StaticBox(self, -1, "Add New Users")
        self.editSizer_staticbox = wx.StaticBox(self, -1, "Edit Existing Users")
        
        #**** MOD ****
        self.userGrid = SimpleUserGrid(self)
        self.userEditToggle = wx.ToggleButton(self, -1, "edit users...")
        
        #*** MOD ***
        self.deleteComboBox = wx.ComboBox(self, 
                                          -1, 
                                          self.userChoices[0], #default
                                          choices=self.userChoices, 
                                          style=wx.CB_DROPDOWN)
        self.deleteButton = wx.Button(self, -1, "delete")
        self.shortNameEntry = wx.TextCtrl(self, -1, "new user short name...")
        self.addButton = wx.Button(self, -1, "add")
        self.nameEntry = wx.TextCtrl(self, -1, "new user full name...")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: userDialog.__set_properties
        self.SetTitle("User Dialog")
        #**** MOD ****

        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: userDialog.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        newTypeSizer = wx.StaticBoxSizer(self.newTypeSizer_staticbox, wx.VERTICAL)
        innerNameSizer = wx.BoxSizer(wx.HORIZONTAL)
        innerShortNameSizer = wx.BoxSizer(wx.HORIZONTAL)
        deleteSizer = wx.StaticBoxSizer(self.deleteSizer_staticbox, wx.VERTICAL)
        innerDeleteSizer = wx.BoxSizer(wx.HORIZONTAL)
        editSizer = wx.StaticBoxSizer(self.editSizer_staticbox, wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        sizer_8.Add(self.userGrid, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_8.Add(self.userEditToggle, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        editSizer.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_2.Add(editSizer, 1, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5)
        innerDeleteSizer.Add(self.deleteComboBox, 1, wx.RIGHT|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        innerDeleteSizer.Add(self.deleteButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        deleteSizer.Add(innerDeleteSizer, 1, wx.EXPAND, 0)
        sizer_2.Add(deleteSizer, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5)
        innerShortNameSizer.Add(self.shortNameEntry, 1, wx.RIGHT|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        innerShortNameSizer.Add(self.addButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        newTypeSizer.Add(innerShortNameSizer, 1, wx.EXPAND, 0)
        innerNameSizer.Add(self.nameEntry, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        newTypeSizer.Add(innerNameSizer, 1, wx.TOP|wx.EXPAND, 3)
        sizer_2.Add(newTypeSizer, 0, wx.ALL|wx.EXPAND, 5)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

# end of class userDialog


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = (None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()