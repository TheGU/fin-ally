#!/usr/bin/env python

#********************************************************************
# Filename:            cfg.py
# Authors:             Daniel Sisco
# Date Created:        7-20-2010
# 
# Abstract: Global variables for the Fin-ally project, hopefully just configuration variables
#
# Copyright 2008 Daniel Sisco
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

# activates certain debug messages, especially in dPrint()
#    0 = no print
#    1 = print
DEBUG = 1       

# activates either a pop-up dialogue for new expenses, or uses a static button panel
#     1 = static button panel 
#     0 = pop-up dialogue
NEW_EXPENSE_PANEL = 0

# activates a grid-based context menu in which a user can delete a row
#    1 = grid-based context menu active
#    0 = menu inactive
GRID_CONTEXT_MENU = 0

# FINally version - used for database migration and version checking
VERSION = (1,5,0)
