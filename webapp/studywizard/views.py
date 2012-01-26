# Create your views here.
from dropbox import client, rest, session
import os
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from forms import CreateAppForm
import datetime
import json
import fnmatch

APP_KEY = os.environ['DROPBOX_APP_KEY']
APP_SECRET = os.environ['DROPBOX_APP_SECRET']
ACCESS_TYPE = 'app_folder'

def db_session(access_token=None, access_token_secret=None):
    sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
    if access_token and access_token_secret:
        sess.set_token(access_token, access_token_secret)
    return sess

def db_client(request):
    access_token = request.session.get("dropbox_access_token")
    access_token_secret = request.session.get("dropbox_access_token_secret")
    print str(access_token) + " " + str(access_token_secret)
    return client.DropboxClient(db_session(access_token, access_token_secret)) if (access_token and access_token_secret) else None
    


def dropbox_auth(request):
    sess = db_session()
    request_token = sess.obtain_request_token()
    request.session["dropbox_request_token"] = request_token
    callback_url = request.build_absolute_uri(reverse(post_dropbox_auth))
    print callback_url
    url = sess.build_authorize_url(request_token, oauth_callback=callback_url)
    return redirect(url)

def post_dropbox_auth(request):
    sess = db_session()
    request_token = request.session.get("dropbox_request_token")
    access_token = sess.obtain_access_token(request_token)
    print dir(access_token)
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
    
    #If form submitted
    if request.method == 'POST':
        form = CreateAppForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            # Process the data in form.cleaned_data
            app_form_vars = {}
            app_probe_vars = {}
            for field_name in form.cleaned_data.keys():
                #General app info
                if not field_name.endswith('Probe') and not field_name.endswith('freq') and not field_name.endswith('duration'):
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
            print config_json

            return redirect('/thanks/') # Redirect after POST
    else:
        form = CreateAppForm() # An unbound form

    return render(request, 'app_create.html', {'form': form})


    folder_metadata = client.metadata('/')
    folder_names = [metadata["path"][1:] for metadata in folder_metadata["contents"] if metadata["is_dir"]]
    return render(request, "app_create.html", {"apps": folder_names})

def app_thanks(request):
    now = datetime.datetime.now()
    return render(request, "thanks.html", {"current_time": now})


def create_app_config(app_form_vars, app_probe_vars):
    config_dict = {}
    config_dict['name'] = app_form_vars['app_name']
    config_dict['version'] = 1
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


def copy_to_dropbox(root_path, dropbox_folder_name):
    root_length = len(root_path)
    pattern = '*'

    for root, dirs, files in os.walk(root_path):
        #Strip everything up until our root directory
        short_root = '/' + dropbox_folder_name + '/' + root[root_length+1:]
        if not '.' in short_root:
            response = client.file_create_folder(short_root)

            #Copy files to dropbox
            for filename in fnmatch.filter(files, pattern):
                print short_root + filename
                f = open(filename)
                response = client.put_file(os.path.join(short_root, filename), f)


def test(request):
    pass
    