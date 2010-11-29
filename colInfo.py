import wx.grid     as gridlib

#********************************************************************    
class columnInfo:
    """This class defines the information required to create and modify columns in
    a grid. This keeps all columns definition data together, but adding information here
    does complete the addition of a new column."""
    
    # TODO: consolidate these into a dict or some other structure
    colLabels = ('user', 'type', 'amount', 'date', 'desc', 'id', 'del')
    defColWidth = "100,50,50,200,300,50,50"
    # col widths are now stored in the database - only defaults are stored here
    #colWidth  = [100, 50, 50, 200, 300, 50, 50]
    colRO     = [0,0,0,0,0,1,0] # 0 = R/W, 1 = R
    colType   = [gridlib.GRID_VALUE_CHOICE,
                  gridlib.GRID_VALUE_CHOICE,
                  gridlib.GRID_VALUE_NUMBER,
                  gridlib.GRID_VALUE_STRING, # should be GRID_VALUE_DATETIME
                  gridlib.GRID_VALUE_STRING,
                  gridlib.GRID_VALUE_NUMBER,
                  gridlib.GRID_VALUE_STRING]
    
    rowHeight = 20
    
# create global instances of classes
colInfo = columnInfo()