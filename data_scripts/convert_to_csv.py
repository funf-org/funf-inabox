#!/usr/bin/env python
#
# Funf: Open Sensing Framework
# Copyright (C) 2010-2011 Nadav Aharony, Wei Pan, Alex Pentland.
# Acknowledgments: Alan Gardner
# Contact: nadav@media.mit.edu
# 
# This file is part of Funf.
# 
# Funf is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
# 
# Funf is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with Funf. If not, see <http://www.gnu.org/licenses/>.
# 
import os.path
import inspect
import sys

script_dir = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
#Check if this is in a mac app.
if script_dir.endswith('.app/Contents/Resources'):
    root_app_dir = os.path.abspath(os.path.join(script_dir, '../../../..'))
else:
    root_app_dir = os.path.abspath(os.path.join(script_dir, '..'))
    
data_processing_scripts_dir = os.path.join(script_dir, 'scripts', 'data_processing')
sys.path.append(data_processing_scripts_dir)
import db2csv

data_dir = os.path.join(root_app_dir,"data")
merged_data_file = os.path.join(data_dir, 'all_data.db')

def convert():
    # Check that merged data exists
    if os.path.isfile(merged_data_file):
        db2csv.convert(merged_data_file, data_dir)


if __name__ == "__main__":
    convert()