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
import wx.calendar as callib

# The recommended way to use wx with mpl is with the WXAgg
# backend. 
#
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

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
        
        self.data = [5, 6, 9, 14]        
        self.create_main_panel()
        self.draw_figure()
        
    def create_main_panel(self):
        """Create and configure the 'Figure', which is the top level Artist in mplotlib."""
        # create 5x4 inch Figure (top level Artist)with 100dpi
        self.fig = Figure((5.0, 4.0), dpi=100)
        # the canvas contains the Figure and performs event handling on the Figure
        self.canvas = FigCanvas(self, -1, self.fig)
        
        # create the main axis so that it is a sub-rectangle of the parent window.
        self.rect = .1,.1,.8,.8 #(left,bottom,width,height)
        self.axes = self.fig.add_axes(self.rect)
        
        # Bind the 'pick' event for clicking on one of the bars
        self.canvas.mpl_connect('pick_event', self.on_pick)

        # Create the navigation toolbar, tied to the canvas
        self.toolbar = NavigationToolbar(self.canvas)
        
        # create sizers
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.vbox.Add(self.toolbar, 0, wx.EXPAND)
        self.vbox.AddSpacer(10)
        self.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def draw_figure(self):
        """redraw the figure!"""
        x = range(len(self.data))

        self.axes.clear()        
        
        self.axes.bar(
            left=x, 
            height=self.data, 
            width=1, 
            align='center', 
            alpha=0.44,
            picker=5)
        
        self.canvas.draw()
    
    def on_pick(self, event):
        """Triggered when a section of the plot is clicked. matplotlib.backend_bases.PickEvent"""
        
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coords:\n %s" % box_points
        print msg