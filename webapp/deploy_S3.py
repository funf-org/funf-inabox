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
import tarfile
import os

import boto
from boto.s3.key import Key


BUCKET_NAME = 'www.funf.org'
PACKAGE_NAME = 'app_generator.tar.gz'
APP_DIR = os.path.join('..','app_generator')


def Ignore(File):
    if os.path.basename(File) == '.gitignore':
        return True
    else: return False 

def CreateTarball():
    Package = tarfile.open(PACKAGE_NAME, "w:gz")
    Package.add(APP_DIR, arcname=os.path.basename(APP_DIR), exclude=Ignore)
    Package.close()
    
def DeleteTarball():
    os.remove(PACKAGE_NAME)


if __name__ == "__main__":
    
    CreateTarball()
    
    try:
        conn = boto.connect_s3()
    
        FunfBucket = conn.get_bucket(BUCKET_NAME)
        AppTemplate = Key(FunfBucket)
        AppTemplate.key = PACKAGE_NAME
        AppTemplate.set_contents_from_filename(PACKAGE_NAME)
        
    except:
        print "Package Upload to S3 Failed!!"
    
    finally:
        DeleteTarball()