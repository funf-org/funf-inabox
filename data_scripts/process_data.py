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
import glob

script_dir = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
#Check if this is in a mac app.
if script_dir.endswith('.app/Contents/Resources'):
    root_app_dir = os.path.abspath(os.path.join(script_dir, '../../../..'))
else:
    root_app_dir = os.path.abspath(os.path.join(script_dir, '..'))
data_dir = os.path.join(root_app_dir,"data")
processing_file = os.path.join(data_dir, 'PROCESSING_DATA')
processing_failed_file = os.path.join(data_dir, 'PROCESSING_FAILED')
merged_data_file = os.path.join(data_dir, 'all_data.db')
raw_data_dir = os.path.join(data_dir, "raw")
config_dir = os.path.join(root_app_dir, "config")
password_file = os.path.join(config_dir,"encryption_password.txt")
data_processing_scripts_dir = os.path.join(script_dir, 'scripts', 'data_processing')

sys.path.append(data_processing_scripts_dir)
import dbdecrypt
import dbmerge
import decrypt
import shutil

def process_data():
    
    # load decrypt password
    with open(password_file, 'r') as file:
        encryption_password = file.read()
    encryption_key = decrypt.key_from_password(encryption_password)
    
    # dbDecrypt all files in raw
    db_files = glob.glob(os.path.join(raw_data_dir, '*.db'))
    failed_files = []
    for db_file in db_files:
        successful = dbdecrypt.decrypt_if_not_db_file(db_file, encryption_key)
        if not successful:
            failed_files.append(db_file)


    # merge all files in raw
    decrypted_files = list(set(db_files) - set(failed_files))
    dbmerge.merge(db_files=decrypted_files, out_file=processing_file, overwrite=True, attempt_salvage=True)
    
    
    # replace current file
    shutil.move(processing_file, merged_data_file)
    
    # TODO: add data report

if __name__ == "__main__":
    process_data()
