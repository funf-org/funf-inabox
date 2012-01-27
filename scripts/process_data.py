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

script_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
data_dir = os.path.abspath(os.path.join(script_dir, "..", "data"))
raw_data_dir = os.path.join(data_dir, "raw")

def process_data():
    # dbDecrypt all files in raw
    # merge all files in raw
    # replace current file
    pass

if __name__ == "__main__":
    process_data()