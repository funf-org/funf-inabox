# Create your views here.
from dropbox import client, rest, session
import os
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse

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
        return redirect(app_list)
    else:
        return redirect('failed_dropbox_auth')

def app_list(request):
    client = db_client(request)
    if not client:
        return redirect(dropbox_auth)
    folder_metadata = client.metadata('/')
    folder_names = [metadata["path"][1:] for metadata in folder_metadata["contents"] if metadata["is_dir"]]
    return render(request, "app_list.html", {"apps": folder_names})


def test(request):
    pass
    