# 
# Funf: Open Sensing Framework
# Copyright (C) 2010-2011 Nadav Aharony, Wei Pan, Alex Pentland.
# Acknowledgments: Alan Gardner
# Contact: nadav@media.mit.edu
#
# Author(s): Swetank Kumar Saha (swetank.saha@gmail.com)
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
import tempfile
import urllib2
import shutil
import os
import fnmatch
import time

from dropbox import client, rest, session

import genfunfapp


METADATA_URL = 'http://metadata/computeMetadata/v1beta1/instance/attributes/'

def getAttribute(attr):
    return urllib2.urlopen(METADATA_URL+attr).read()

APP_KEY = os.environ['DROPBOX_APP_KEY']
APP_SECRET = os.environ['DROPBOX_APP_SECRET']
ACCESS_TYPE = 'app_folder'

class CopyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def copy_to_dropbox(db_client, root_path, dropbox_folder_name, abort_count = 0):
    root_length = len(root_path)
    pattern = '*'

    try:
        for root, dirs, files in os.walk(root_path):
            #Strip everything up until our root directory
            short_root = '/' + dropbox_folder_name + '/' + root[root_length+1:]
            if not '/.' in short_root:
                folder_success = copy_folder_to_dropbox(db_client, short_root)
                if folder_success == False:
                    raise CopyError

                #Copy files to dropbox
                for filename in fnmatch.filter(files, pattern):
                    if not filename.startswith('.'):
                        f = open(os.path.join(root, filename))
                        file_success = copy_file_to_dropbox(db_client, short_root, filename, f)
                        if file_success == False:
                            raise CopyError

    except CopyError:
        if abort_count < 5:
            time.sleep(300)
            copy_to_dropbox(db_client, root_path, dropbox_folder_name, abort_count = abort_count + 1)

def copy_file_to_dropbox(db_client, short_root, filename, f):
    copy_success = True

    try:
        response = db_client.put_file(os.path.join(short_root, filename), f, overwrite=True)
    except rest.ErrorResponse as inst:
        time.sleep(30)
        try:
            response = db_client.put_file(os.path.join(short_root, filename), f, overwrite=True)
        except:
            copy_success = False

    return copy_success

def copy_folder_to_dropbox(db_client, short_root):
    copy_success = True

    try:
        response = db_client.file_create_folder(short_root)
    except rest.ErrorResponse as inst:
        if not str(inst).startswith('[403]'): #folder already exists
            time.sleep(30)
            try:
                response = db_client.file_create_folder(short_root)
            except:
                copy_success = False

    return copy_success


if __name__ == "__main__":
    temp_dir = tempfile.mkdtemp(prefix="funfinabox")
    
    user_id = getAttribute('user_id')
    dropbox_token = getAttribute('dropbox_token')
    dropbox_token_secret = getAttribute('dropbox_token_secret')
    name = getAttribute('name')
    description = getAttribute('description')
    contact_email = getAttribute('contact_email')
    funf_conf = getAttribute('funf_conf')
    
    app_dir = genfunfapp.generate(temp_dir, user_id, dropbox_token, dropbox_token_secret, name, description, contact_email, funf_conf)
    
    sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
    sess.set_token(dropbox_token, dropbox_token_secret)
    db_client = client.DropboxClient(sess)
    
    copy_to_dropbox(db_client, app_dir, os.path.basename(app_dir))
    shutil.rmtree(temp_dir)