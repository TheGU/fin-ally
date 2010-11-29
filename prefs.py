import wx
from database import Database

def EditPreferences(self, event):
    """fires when the new user button is clicked, this method creates a new user object"""
    dia = PreferenceDialog(self, -1, 'Edit Preferences')
    dia.ShowModal()
    dia.Destroy()
    event.Skip()
    
#********************************************************************
def SaveWindowPreferences(frameWidth, frameHeight):
    """called when we want to write window-based preferences into the database"""
    #print "size of the main frame is: %s by %s" % (frameWidth, frameHeight)

#********************************************************************    
def SaveColumnPreferences(colId, colWidth):
    """called when we want to write column preferences into the database"""
    print "size of column %s changed to %s" % (colId, colWidth)
    
    # pull current column widths out of database - split into array
    database = Database()
    locColWidths = database.GetPrefs().colWidths.split(',')
    locColWidths[colId] = str(colWidth)
    
    # re-load string with desired col width
    locString = ""
    for i in locColWidths:
        locString += i
        locString +=","
    locString = locString.rstrip(",")
    
    # push back into database
    database.SetColWidthPref(locString)
    
#********************************************************************
class PreferenceDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(350,300))
        
        self.database = Database()
        self.userList = self.database.GetSimpleUserList()
        self.typeList = self.database.GetExpenseTypeList()
        self.prefs    = self.database.GetPrefs()
        
        self.parent   = parent
        
        self.sizer        = wx.BoxSizer(wx.VERTICAL)  # define new box sizer    
        self.buttonPanel  = wx.Panel(self)              # create a panel for the buttons
    
        # SAVE BUTTON    
        self.saveButton = wx.Button(self.buttonPanel,
                                    id = -1,
                                    label = "Save",
                                    pos = (0,0))
        self.Bind(wx.EVT_BUTTON, self.OnSaveClick, self.saveButton)
    
        # DEFAULT USER
        self.userSelect   = wx.ComboBox(self.buttonPanel, 
                                        id=-1,
                                        value=str(self.prefs.defUser_id),
                                        choices=self.userList,
                                        pos=(100,0), 
                                         style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.OnUserSelect, self.userSelect)
        
        # DEFAULT EXPENSE TYPE
        self.expenseTypeSelect   = wx.ComboBox(self.buttonPanel, 
                                        id=-1,
                                        value=str(self.prefs.defExpenseType_id),
                                        choices=self.typeList,
                                        pos=(100,100), 
                                         style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.OnExpenseTypeSelect, self.expenseTypeSelect)
        
        # create and bind a value entry box
        self.valueEntry   = wx.TextCtrl(self.buttonPanel, 
                                        -1, 
                                        str(self.prefs.defAmount), 
                                        pos = (0,25), 
                                        size = (90, 21))
        self.Bind(wx.EVT_TEXT, self.OnValueEntry, self.valueEntry)
    
        
        self.sizer.Add(self.buttonPanel, 0, wx.ALIGN_LEFT)    # add panel (no resize vert and aligned left horz)
        self.SetSizer(self.sizer)
    
    def OnSaveClick(self, evt):
        """respond to the user clicking 'save' by pushing the local objects into the database 
        layer"""
        self.database.EditPrefs(self.userSelect.GetValue(), 
                                self.expenseTypeSelect.GetValue(), 
                                self.valueEntry.GetValue())

        self.Close()
        
    #***************************
    # NOT REQUIRED AT THIS TIME
    #***************************    
    def OnUserSelect(self, evt):
        evt.Skip()
        
    def OnExpenseTypeSelect(self, evt):
        evt.Skip()
        
    def OnValueEntry(self, evt):
        evt.Skip()
        