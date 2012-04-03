# Create your views here.
from dropbox import client, rest, session
import os
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from models import Stats
from forms import CreateAppForm
import time, datetime
import json
import fnmatch
import threading
import genfunfapp
import tempfile
import shutil

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


class CreateAppThread(threading.Thread):
    
    def __init__(self, db_client, user_id, dropbox_token, dropbox_token_secret, name, description, contact_email, funf_conf):
        super(CreateAppThread, self).__init__()
        self.db_client = db_client
        self.user_id = user_id
        self.dropbox_token = dropbox_token
        self.dropbox_token_secret = dropbox_token_secret
        self.name = name
        self.description = description
        self.contact_email = contact_email
        self.funf_conf = funf_conf
            
    def run(self):
        temp_dir = tempfile.mkdtemp(prefix="funfinabox") 
        app_dir = genfunfapp.generate(temp_dir, self.user_id, self.dropbox_token, self.dropbox_token_secret, self.name, self.description, self.contact_email, self.funf_conf)
        copy_to_dropbox(self.db_client, app_dir, os.path.basename(app_dir))
        shutil.rmtree(temp_dir)


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
                #General app info
                elif not field_name.endswith('Probe') and not field_name.endswith('freq') and not field_name.endswith('duration'):
                    app_form_vars[field_name] = form.cleaned_data[field_name]
                #Probe info
                elif not field_name.endswith('freq') and not field_name.endswith('duration') and not form.cleaned_data[field_name] == False:
                    try:
                        app_probe_vars[field_name] = {}
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
            
            t = CreateAppThread(client, dropbox_account_info["uid"], access_token, access_token_secret, app_form_vars["app_name"], app_form_vars["description"], app_form_vars["contact_email"], config_json)
            t.start()

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
    config_dict = {}
    config_dict['name'] = app_form_vars['app_name']
    config_dict['version'] = 1
    config_dict['dataUploadOnWifiOnly'] = True if app_form_vars['dataUploadStrategy'] == 'WIFI'else False
    config_dict['dataUploadPeriod'] = 0 if app_form_vars['dataUploadStrategy'] == 'NONE' else 10800
    
    config_dict['dataRequests'] = {}

    for key in app_probe_vars.keys():
        period_duration = {}
        try:
            period_duration['PERIOD'] = app_probe_vars[key]['PERIOD']
            period_duration['DURATION'] = app_probe_vars[key]['DURATION']
        except:
            pass
        config_dict['dataRequests']['edu.mit.media.funf.probe.builtin.' + key] = [period_duration]

    return config_dict


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



def test(request):
    pass
    
