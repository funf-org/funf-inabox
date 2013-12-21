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
import webapp2
import logging
from apiclient.discovery import build
from datetime import datetime, timedelta
import os

import ComputeEngine


class InstanceCleaner(webapp2.RequestHandler):

    def get(self):
        AuthHTTP = ComputeEngine.Authorize()
        
        Instances = ComputeEngine.ListInstances(AuthHTTP)
        if not(Instances):
            logging.info('No Instances running!')
        else:
            gce_service = build('compute', ComputeEngine.API_VERSION, developerKey=os.environ['GOOGLE_API_KEY'])
            count = 0
            for instance in Instances:
                if instance['status'] == 'TERMINATED':
                    Request = gce_service.instances().delete(project=ComputeEngine.PROJECT_ID, 
                                                             instance=instance['name'], 
                                                             zone=ComputeEngine.ZONE)
                    response = Request.execute(http=AuthHTTP)
                    count += 1
                    
                if instance['status'] == 'RUNNING':
                    CreationTS = instance['creationTimestamp']
                    TimeStamp = CreationTS[:-6]
                    TimeZone = CreationTS[-6:]
                    TZHour = int(TimeZone.split(':')[0])
                    if TZHour > 0 : TZHMin = int(TimeZone.split(':')[1])
                    else: TZMin = int(TimeZone.split(':')[1]) * (-1)
                    
                    Created = datetime.strptime(TimeStamp, "%Y-%m-%dT%H:%M:%S.%f")
                    CurrentUTC = datetime.utcnow() + timedelta(hours=TZHour,minutes=TZMin)
                    
                    if( CurrentUTC - Created > timedelta(minutes=30) ):
                        Request = gce_service.instances().delete(project=ComputeEngine.PROJECT_ID, 
                                                                 instance=instance['name'], 
                                                                 zone=ComputeEngine.ZONE)
                        response = Request.execute(http=AuthHTTP)
                        count += 1
                        
            if count > 0 :logging.info(str(count)+' instances deleted!')
            
        return None
    
    
class DiskCleaner(webapp2.RequestHandler):

    def get(self):
        AuthHTTP = ComputeEngine.Authorize()
        
        Disks = ComputeEngine.ListDisks(AuthHTTP)
        if not(Disks):
            logging.info('No Disks!')
        else:
            gce_service = build('compute', ComputeEngine.API_VERSION, developerKey=os.environ['GOOGLE_API_KEY'])
            count = 0
            for disk in Disks:
                if disk['status'] == 'FAILED':
                    Request = gce_service.disks().delete(project=ComputeEngine.PROJECT_ID, 
                                                             disk=disk['name'],
                                                             zone=ComputeEngine.ZONE)
                    response = Request.execute(http=AuthHTTP)
                    count += 1
                    
                if disk['status'] == 'READY':
                    CreationTS = disk['creationTimestamp']
                    TimeStamp = CreationTS[:-6]
                    TimeZone = CreationTS[-6:]
                    TZHour = int(TimeZone.split(':')[0])
                    if TZHour > 0 : TZHMin = int(TimeZone.split(':')[1])
                    else: TZMin = int(TimeZone.split(':')[1]) * (-1)
                    
                    Created = datetime.strptime(TimeStamp, "%Y-%m-%dT%H:%M:%S.%f")
                    CurrentUTC = datetime.utcnow() + timedelta(hours=TZHour,minutes=TZMin)
                    
                    if( CurrentUTC - Created > timedelta(minutes=20) ):
                        Request = gce_service.disks().delete(project=ComputeEngine.PROJECT_ID, 
                                                                 disk=disk['name'],
                                                                 zone=ComputeEngine.ZONE)
                        response = Request.execute(http=AuthHTTP)
                        count += 1
                        
            if count > 0 :logging.info(str(count)+' disks deleted!')
            
        return None


application = webapp2.WSGIApplication([
    ('/cron/cleanup/instances', InstanceCleaner),
    ('/cron/cleanup/disks', DiskCleaner),
], debug=True)

if __name__ == '__main__':
    main()