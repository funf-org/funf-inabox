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
#! /bin/bash
#Create a dependencies folder
mkdir dependencies

#Google-api-python-client for GAE
wget https://google-api-python-client.googlecode.com/files/google-api-python-client-gae-1.1.zip -P ./dependencies

#Django-nonrel and dependencies
pip install --download='./dependencies' --no-install -r requirements.txt

#Unzip all dependencies
cd dependencies
unzip google-api-python-client-gae-1.1.zip -d ../
unzip django-autoload-0.01.zip
unzip django-dbindexer-0.3.zip
unzip django-nonrel-1.4.8.zip
unzip djangoappengine-1.4.0.zip
unzip djangotoolbox-1.4.0.zip
unzip dropbox-client-python-1.3.zip
unzip huTools-0.64.zip

#Copy required folders
cp -r django-autoload/autoload ../autoload
cp -r django-dbindexer/dbindexer ../dbindexer
cp -r django-nonrel/django ../django
cp -r djangoappengine/djangoappengine ../djangoappengine
cp -r djangotoolbox/djangotoolbox ../djangotoolbox
cp -r dropbox-client-python/dropbox ../dropbox
cp -r huTools/huTools ../huTools

#Delete dependency packages
cd ..
rm -rf dependencies
rm -rf src

#Package the Android app-template
tar -pczf app_generator.tar.gz ../app_generator
