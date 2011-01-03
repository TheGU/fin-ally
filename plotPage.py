#!/usr/bin/env python

#********************************************************************
# Filename:        plotPage.py
# Authors:         Daniel Sisco
# Date Created:    12-27-2010
# 
# Abstract: This file contains classes to compose the plotting portion of the FINally tool.
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
import wx.grid     as gridlib
from database import *
from decimal import *
from threads import ExpenseThread

# The recommended way to use wx with mpl is with the WXAgg
# backend. 
#
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.pyplot import legend as Legend
from matplotlib.font_manager import fontManager, FontProperties
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
    
def dump(obj):
  for attr in dir(obj):
    print "obj.%s = %s" % (attr, getattr(obj, attr))

#********************************************************************
class SimplePlotGrid(gridlib.Grid):
    """This is a simple grid class - which means most of the methods are automatically
    defined by the wx library"""
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)
        self.CreateGrid(100,2)
        
        self.SetColLabelValue(0,"expense")       
        self.SetColLabelValue(1,"amount")
        self.EnableEditing(False)
        
        self.data = []
        
    def SetData(self, localData):
        """Clears the grid before re-loading data and refreshing to ensure a repaint"""
        self.ClearGrid()
        self.data = localData
        self.RefreshData()
        
    def RefreshData(self):
        """iterates through local list self.data and loads grid with the data"""
        for i in range(len(self.data)):
            self.SetCellValue(i,0,str(self.data[i][0]))
            self.SetCellValue(i,1,str(self.data[i][1]))
        
#********************************************************************    
class PlotPage(wx.Panel):
    """
    Class Name:     GraphicsPage
    Extends:         wx.Panel
    Description:    The Graphics page contains two things - a grid or table of entries, 
    and a button panel to perform some operations on the grid.
    """
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.database = Database()
        self.data = []    
        self.labels = []
        self.wedges = []
        self.sum = 0
        self.explode = (0, 0.05, 0, 0)  
    
        self.database = Database()
        self.plotGrid = SimplePlotGrid(self)
        
        # store thread refresh function 
        # NOTE: we don't even need to create an ExpenseThread member here
        ExpenseThread().StoreRefreshFunc(self.draw_figure)
        
        self.create_main_panel()
        self.draw_figure()
        
    def on_pick(self, event):
        """Triggered when a section of the plot is clicked. matplotlib.backend_bases.PickEvent"""
        wedge = event.artist
        label = wedge.get_label()
        
        # iterate through all data and grab pertinent expenses
        tempData = self.database.GetAllExpenses()
        # for each expense pull out expense description and amount when type matches
        gridData = [(i[4], i[2]) for i in tempData if i[1]== label]
        # set data into grid
        self.plotGrid.SetData(gridData)
        
    def create_main_panel(self):
        """Create and configure the 'Figure', which is the top level Artist in mplotlib."""
        # create 5x4 inch Figure (top level Artist)with 100dpi
        self.fig = Figure((5.0, 5.0), dpi=100)
        
        # the canvas contains the Figure and performs event handling on the Figure
        self.canvas = FigCanvas(self, -1, self.fig)
        
        # create the main axis so that it is a sub-rectangle of the parent window.
        self.rect = 0, 0, .9, .9
        self.axes = self.fig.add_axes(self.rect)
        
        # Bind the 'pick' event for clicking on one of the bars
        self.canvas.mpl_connect('pick_event', self.on_pick)
        #self.fig.canvas.mpl_connect('pick_event', self.on_pick)

        # Create the navigation toolbar, tied to the canvas
        self.toolbar = NavigationToolbar(self.canvas)
        
        # create sizers
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, wx.ALIGN_LEFT)
        self.vbox.Add(self.toolbar, 0, wx.EXPAND)
        
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox.Add(self.vbox, 0)
        self.hbox.Add(self.plotGrid, 1, wx.EXPAND)
        
        self.SetSizer(self.hbox)

    def PieSliceValue(self, value):
        """called by the matplotlib plot function to generate numeric labels
        for the pie slices. 'value' is passed in as a number between 0 and 100."""
        return "%.2f" % (self.sum * Decimal(str(value/100)))

    def draw_figure(self):
        """redraw the figure!"""
        
        # clear and re-load self.data with summations of all like
        # expense-type expenses
        self.data = [] # clear self.data
        self.labels = [] # clear self.labels
        self.sum = Decimal(0)
        tempData = self.database.GetAllExpenses()
        tempDict = {}
        
        # create the expenseType/amount dictionary
        # TODO: there has got to be a better way to do this - something more
        # (groan) Pythonic
        for i in tempData:
            if tempDict.has_key(i[1]):
                tempDict[i[1]] += Decimal(i[2])
            else: 
                tempDict[i[1]]  = Decimal(i[2])
        
        # iterate through created dictionary and add values to self.data and self.labels
        for key, value in tempDict.iteritems():
            self.data.append(value)
            self.sum = self.sum + value
            self.labels.append(key)
        
        # skip this and you'll see pie chart ghosts...
        self.axes.clear()        

        # create the pie chart
        self.wedges, self.temp_labels, self.temp_crap = self.axes.pie(self.data, labels = self.labels, autopct=self.PieSliceValue, labeldistance=10.1)
        
        # remove legend elements that are below some threshold and feed the remaining elements to the legend
#        tempWedges = [] 
#        tempLabels = []
#        legend = False
#        for i in range(len(self.wedges)):
#            #print self.labels[i], abs(self.wedges[i].theta1 - self.wedges[i].theta2)
#            if abs(self.wedges[i].theta1 - self.wedges[i].theta2) < 10:
#                tempWedges.append(self.wedges[i])
#                tempLabels.append(self.labels[i])
#                legend= True
#        
#        if legend == True:
#            self.fig.legend(tempWedges, tempLabels)
        if self.wedges:
            font = FontProperties(size='x-small');
            self.fig.legend(self.wedges, self.labels, fancybox = True, prop=font)
        
        # set picker status for each new wedge
        for wedge in self.wedges:
            wedge.set_picker(True)
            
        # draw the pie chart
        self.canvas.draw()