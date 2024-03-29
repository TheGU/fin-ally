#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Sat Oct 30 20:01:31 2010

import wx
import wx.calendar

# begin wxGlade: extracode
# end wxGlade



class NewExpenseDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: NewExpenseDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.CalSizer_staticbox = wx.StaticBox(self, -1, "Expense Date")
        self.ExpenseStaticSizer_staticbox = wx.StaticBox(self, -1, "Expense Info")
        self.UserSizer_staticbox = wx.StaticBox(self, -1, "User")
        self.userControl = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN)
        self.calendarControl = wx.calendar.CalendarCtrl(self, -1)
        self.amountText = wx.StaticText(self, -1, "Amount:")
        self.expenseTypeText = wx.StaticText(self, -1, "Expense Type:")
        self.descriptionText = wx.StaticText(self, -1, "Description:")
        self.amountControl = wx.TextCtrl(self, -1, "")
        self.expenseTypeControl = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN)
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
        self.SetTitle("New Expense Dialog")
        self.amountText.SetMinSize((80, 23))
        self.expenseTypeText.SetMinSize((80, 23))
        self.descriptionText.SetMinSize((80, 23))
        self.amountControl.SetMinSize((150, -1))
        self.expenseTypeControl.SetMinSize((150, -1))
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
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        CalSizer = wx.StaticBoxSizer(self.CalSizer_staticbox, wx.HORIZONTAL)
        UserSizer = wx.StaticBoxSizer(self.UserSizer_staticbox, wx.HORIZONTAL)
        UserSizer.Add(self.userControl, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        VerticalSizer.Add(UserSizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        CalSizer.Add(self.calendarControl, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        VerticalSizer.Add(CalSizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_3.Add(self.amountText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_3.Add(self.expenseTypeText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_3.Add(self.descriptionText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        ExpenseStaticSizer.Add(sizer_3, 0, 0, 0)
        sizer_2.Add(self.amountControl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_2.Add(self.expenseTypeControl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_2.Add(self.descriptionControl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        ExpenseStaticSizer.Add(sizer_2, 0, wx.EXPAND, 0)
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

# end of class NewExpenseDialog


class NewExpense(wx.Dialog):
    def __init__(self, *args, **kwds):
        # content of this block not found: did you rename this class?
        pass

    def __set_properties(self):
        # content of this block not found: did you rename this class?
        pass

    def __do_layout(self):
        # content of this block not found: did you rename this class?
        pass

# end of class NewExpense


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    dialog_2 = NewExpense(None, -1, "")
    app.SetTopWindow(dialog_2)
    dialog_2.Show()
    app.MainLoop()
