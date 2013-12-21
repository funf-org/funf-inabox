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
import httplib2
from google.appengine.api import memcache
from oauth2client.appengine import AppAssertionCredentials
from apiclient.discovery import build
from google.appengine.api.app_identity import get_application_id

import os
import datetime

#API Config
GCE_SCOPE = 'https://www.googleapis.com/auth/compute'
API_VERSION = 'v1'
GCE_URL = 'https://www.googleapis.com/compute/%s/projects/' % (API_VERSION)
PROJECT_ID = os.environ['GOOGLE_PROJECT_ID']
ZONE = 'us-central1-a'

#Instance Config
MACHINE_TYPE = 'n1-standard-1'
IMAGE = 'debian-7-wheezy-v20131120'
NETWORK = 'default'
INSTANCE_NAME_BASE = 'funfinabox'
DISK_NAME_BASE = 'funfdisk'
INSTANCE_DESCRIPTION = 'Funf In a Box App Generator'

#Instance Config URLs
project_url = GCE_URL + PROJECT_ID
network_url = '%s/global/networks/%s' % (project_url, NETWORK)
zone_url = '%s/zones/%s' % (project_url, ZONE)
image_url = '%s%s/global/images/%s' % (GCE_URL, 'debian-cloud', IMAGE)
machine_type_url = '%s/zones/%s/machineTypes/%s' % (project_url, ZONE, MACHINE_TYPE)
root_disk_url = '%s/zones/%s/disks/' % (project_url, ZONE)

#Metadata Config
startup_script = 'app-generator.sh'
generator_script = 'generate_app_remote.py'


def Authorize():
    credentials = AppAssertionCredentials(scope=GCE_SCOPE)
    return credentials.authorize(httplib2.Http(memcache))
                                 
                                 
def ListInstances(auth_http):
    #Get a service object
    gce_service = build('compute', API_VERSION, developerKey=os.environ['GOOGLE_API_KEY'])
    
    # List instances
    request = gce_service.instances().list(project=PROJECT_ID, filter=None, zone=ZONE)
    response = request.execute(http=auth_http)
    if response and 'items' in response:
        instances = response['items']
        return instances
    else:
        return None
    
    
def ListDisks(auth_http):
    #Get a service object
    gce_service = build('compute', API_VERSION, developerKey=os.environ['GOOGLE_API_KEY'])
    
    # List Disks
    request = gce_service.disks().list(project=PROJECT_ID, filter=None, zone=ZONE)
    response = request.execute(http=auth_http)
    if response and 'items' in response:
        disks = response['items']
        return disks
    else:
        return None
    
    
def NewDisk(auth_http, gce_service):
    
    disk_name = DISK_NAME_BASE+datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    disk = {
        'name': disk_name
    }

    #Create a new disk
    request = gce_service.disks().insert(project=PROJECT_ID, body=disk, zone=ZONE, sourceImage=image_url)
    response = request.execute(http=auth_http)
    _blocking_call(gce_service, auth_http, response)
    
    return disk_name
    

def NewInstance(auth_http, user_id, dropbox_token, dropbox_token_secret, name, description, contact_email, funf_conf):
    #Get a service object
    gce_service = build('compute', API_VERSION, developerKey=os.environ['GOOGLE_API_KEY'])
    
    #New Disk Creation
    DISK = NewDisk(auth_http, gce_service)
    
    #New Instance Specification
    instance = {
      "kind": "compute#instance",
      "disks": [{
       'source': root_disk_url+DISK,
       'boot': 'true',
       'type': 'PERSISTENT'
      }],
      "networkInterfaces": [
        {
          "kind": "compute#instanceNetworkInterface",
          "accessConfigs": [
            {
              "name": "External NAT",
              "type": "ONE_TO_ONE_NAT"
            }
          ],
          "network": network_url
        }
      ],
      "zone": zone_url,
      "metadata": {
        "items": []
      },
      "machineType": machine_type_url,
      "name": INSTANCE_NAME_BASE+datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"),
      "description": INSTANCE_DESCRIPTION,
      "tags": {
        "items": [
          "funf",
          "android",
          "debian"
        ]
      },
      'metadata': [{
         'items': [{
             'key': 'startup-script',
             'value': file(os.path.join(os.path.dirname(__file__), startup_script), 'r').read()
           }, {
             'key': 'user_id',
             'value': user_id
           }, {
             'key': 'dropbox_token',
             'value': dropbox_token
           }, {
             'key': 'dropbox_token_secret',
             'value': dropbox_token_secret
           }, {
             'key': 'name',
             'value': name
           }, {
             'key': 'description',
             'value': description
           }, {
             'key': 'contact_email',
             'value': contact_email
           }, {
             'key': 'funf_conf',
             'value': funf_conf
           }, {
             'key': 'DROPBOX_APP_KEY',
             'value': os.environ['DROPBOX_APP_KEY']
           }, {
             'key': 'DROPBOX_APP_SECRET',
             'value': os.environ['DROPBOX_APP_SECRET']
           }, {
             'key': 'GAE_PROJECT_NAME',
             'value': get_application_id()
           }]
      }]
    }
    
    #Instantiate a new instance
    request = gce_service.instances().insert(project=PROJECT_ID, body=instance, zone=ZONE)
    request.execute(http=auth_http)
    
    
def _blocking_call(gce_service, auth_http, response):
    """Blocks until the operation status is done for the given operation."""

    status = response['status']
    while status != 'DONE' and response:
      operation_id = response['name']

      # Identify if this is a per-zone resource
      if 'zone' in response:
        zone_name = response['zone'].split('/')[-1]
        request = gce_service.zoneOperations().get(project=PROJECT_ID, operation=operation_id, zone=zone_name)
      else:
        request = gce_service.globalOperations().get(project=PROJECT_ID, operation=operation_id)

      response = request.execute(http=auth_http)
      if response:
        status = response['status']
    
    return response