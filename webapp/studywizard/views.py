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
# Create your views here.
from dropbox import client, rest, session
import os
import re
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from models import Stats
from forms import CreateAppForm
import time, datetime
import json

from external import ComputeEngine

APP_KEY = os.environ['DROPBOX_APP_KEY']
APP_SECRET = os.environ['DROPBOX_APP_SECRET']
ACCESS_TYPE = 'app_folder'

# Redirect stdout to stderr to print to apache error logs
import sys
sys.stdout = sys.stderr


def db_session(access_token=None, access_token_secret=None):
    sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
    if access_token and access_token_secret:
        sess.set_token(access_token, access_token_secret)
    return sess

def db_client(request):
    access_token = request.session.get("dropbox_access_token")
    access_token_secret = request.session.get("dropbox_access_token_secret")
    return client.DropboxClient(db_session(access_token, access_token_secret)) if (access_token and access_token_secret) else None
    


def dropbox_auth(request):
    sess = db_session()
    request_token = sess.obtain_request_token()
    request.session["dropbox_request_token"] = request_token
    callback_url = request.build_absolute_uri(reverse(post_dropbox_auth))
    url = sess.build_authorize_url(request_token, oauth_callback=callback_url)
    return redirect(url)

def post_dropbox_auth(request):
    sess = db_session()
    request_token = request.session.get("dropbox_request_token")
    access_token = sess.obtain_access_token(request_token)
    if access_token:
        request.session["dropbox_access_token"] = access_token.key
        request.session["dropbox_access_token_secret"] = access_token.secret
        #return redirect(app_list)
        return redirect(app_create)
    else:
        return redirect('failed_dropbox_auth')

def app_list(request):
    client = db_client(request)
    if not client:
        return redirect(dropbox_auth)
    folder_metadata = client.metadata('/')
    folder_names = [metadata["path"][1:] for metadata in folder_metadata["contents"] if metadata["is_dir"]]
    return render(request, "app_list.html", {"apps": folder_names})

def app_create(request):
    #Dropbox auth
    client = db_client(request)
    if not client:
        return redirect(dropbox_auth)
    #Make sure tokens are valid
    try:
        client.account_info()
    except:
        try:
            del request.session["dropbox_access_token"]
            del request.session["dropbox_access_token_secret"]
            return redirect(dropbox_auth)
        except:
            return redirect('home')
    
    #If form submitted
    if request.method == 'POST':
        form = CreateAppForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            # Process the data in form.cleaned_data
            app_form_vars = {}
            app_registration_vars = {}
            app_probe_vars = {}
            for field_name in form.cleaned_data.keys():
                #Registration info
                if field_name.endswith('REG_INFO'):
                    app_registration_vars[field_name] = form.cleaned_data[field_name]
                #Configuration update/Upload data info
                if field_name == 'configUpdate_freq' or field_name == 'dataUpload_freq':
                    if form.cleaned_data[field_name] != None:
                        app_form_vars[field_name] = int(form.cleaned_data[field_name])
                #General app info
                elif not field_name.endswith('Probe') and not field_name.endswith('freq') and not field_name.endswith('duration'):
                    #Clean if app name
                    if field_name == 'app_name':
                        app_form_vars[field_name] = re.sub(r'([^\s\w]|_)+', '', form.cleaned_data[field_name])
                    else:
                        app_form_vars[field_name] = form.cleaned_data[field_name]
                #Probe info
                elif not field_name.endswith('freq') and not field_name.endswith('duration') and not form.cleaned_data[field_name] == False:
                    try:
                        app_probe_vars[field_name] = {}
                        #Extra parameters for UserStudyNotificationProbe
                        if field_name == 'UserStudyNotificationProbe':
                            app_probe_vars[field_name]['URL'] = form.cleaned_data[field_name + '_url']
                            app_probe_vars[field_name]['TITLE'] = form.cleaned_data[field_name + '_notifyTitle']
                            app_probe_vars[field_name]['MESSAGE'] = form.cleaned_data[field_name + '_notifyMessage']
                        app_probe_vars[field_name]['PERIOD'] = int(form.cleaned_data[field_name + '_freq'])
                        app_probe_vars[field_name]['DURATION'] = int(form.cleaned_data[field_name + '_duration'])
                    except:
                        pass

            #Create json config for app creation
            config_dict = create_app_config(app_form_vars, app_probe_vars)
            config_json = json.dumps(config_dict)

            #Save stats
            app_creation = Stats(create_time=datetime.datetime.now(), app_name=app_form_vars['app_name'], description=app_form_vars['description'], contact_email=app_form_vars['contact_email'], creator_name=app_registration_vars['creator_name_REG_INFO'], creator_email=app_registration_vars['creator_email_REG_INFO'], org_name=app_registration_vars['org_name_REG_INFO'], location=app_registration_vars['location_REG_INFO'], probe_config=str(config_dict))
            app_creation.save()
            
            dropbox_account_info = client.account_info()
            access_token = request.session.get("dropbox_access_token")
            access_token_secret = request.session.get("dropbox_access_token_secret")
            
            AuthHTTP = ComputeEngine.Authorize()
            ComputeEngine.NewInstance(AuthHTTP, dropbox_account_info["uid"], access_token, access_token_secret, app_form_vars["app_name"], app_form_vars["description"], app_form_vars["contact_email"], config_json)
            
            return redirect(app_thanks) # Redirect after POST
    else:
        form = CreateAppForm() # An unbound form

    return render(request, 'app_create.html', {'form': form})


    #folder_metadata = client.metadata('/')
    #folder_names = [metadata["path"][1:] for metadata in folder_metadata["contents"] if metadata["is_dir"]]
    #return render(request, "app_create.html", {"apps": folder_names})

def app_thanks(request):
    now = datetime.datetime.now()
    return render(request, "thanks.html", {"current_time": now})

def app_info(request):
    return render(request, "info.html")

def app_legal(request):
    return render(request, "legal.html")


def create_app_config(app_form_vars, app_probe_vars):
    config_dict = {
        'name': app_form_vars['app_name'],
        'version': 1,
        'upload': None if app_form_vars['dataUploadStrategy'] == 'NONE' else {
            '@type': 'funfinabox.app.DropboxArchive',
            '@schedule': {'interval': app_form_vars['dataUpload_freq'] if 'dataUpload_freq' in app_form_vars else 10800},
            'wifiOnly': True if app_form_vars['dataUploadStrategy'] == 'WIFI' else False
        },
        'update': {
            '@type': 'funfinabox.app.DropboxConfigUpdater'
        },
        'data': []
    }
    
    #Add update schedule, if user has checked the corresponding box
    if app_form_vars['configUpdate']:
        config_dict['update']['@schedule'] = { 'interval': app_form_vars.get('configUpdate_freq', 10800) }
    
    
    for key in app_probe_vars.keys():
        if key == 'UserStudyNotificationProbe': 
            probe_config = {'@type': 'edu.mit.media.funf.probe.external.' + key}
        else: 
            probe_config = {'@type': 'edu.mit.media.funf.probe.builtin.' + key}
        schedule = {}
        try:
            schedule['interval'] = app_probe_vars[key]['PERIOD']
            schedule['duration'] = app_probe_vars[key]['DURATION']
        except:
            pass

        if schedule:
            probe_config['@schedule'] = schedule

        # Custom defaults for FIAB (specifically the LightSensor since it goes crazy otherwise)
        if key == 'LightSensorProbe':
            probe_config['sensorDelay'] = "NORMAL"
            
        # Add the extra parameters for UserStudyNotificationProbe
        if key == 'UserStudyNotificationProbe':
            if app_probe_vars[key]['URL']: probe_config['url'] = app_probe_vars[key]['URL']
            if app_probe_vars[key]['TITLE']: probe_config['notifyTitle'] = app_probe_vars[key]['TITLE']
            if app_probe_vars[key]['MESSAGE']: probe_config['notifyMessage'] = app_probe_vars[key]['MESSAGE']
            
        config_dict['data'].append(probe_config)

    return config_dict

def test(request):
    pass