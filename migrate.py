#!/usr/bin/env python

#********************************************************************
# Filename:            migrate.py
# Authors:             Daniel Sisco
# Date Created:        8-24-2010
# 
# Abstract: This is the Model/Controller component of the FINally SQLite finance tool.
# This file provides driver level functions for data manipulation that can be called
# by the FINally View component (Model-functionality). This file is also responsible
# for post processing and manipulating data before passing it back to the View
# (Controller-functionality).
#
# Version History:  See repository
#
# Copyright 2010 Daniel Sisco
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

from database import *

def versionCheck():
    """checks compatibility between the FINally version and the database version"""
    # read database version into a tuple
    storedDbVersion = (Version.query.all()[0].version_major, Version.query.all()[0].version_minor)
    
    # check compatibility
    if(dbVer != storedDbVersion):
        # perform migration
        print "mismatch - please upgrade from version ", storedDbVersion, "to version ", dbVer, "!"      