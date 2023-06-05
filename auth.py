# this file handles authentication and returns service
# take reference from docs.google.com

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from flask import session
import pathlib

# main function to get authentication from service api
def get_service(api_name, api_version, scopes=['https://www.googleapis.com/auth/drive'], key_file_location=''):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """
    # print(scopes)
    if key_file_location == '':
        key_file_location = _path() + 'credentials.json'
    credentials = service_account.Credentials.from_service_account_file(
    key_file_location)
    

    scoped_credentials = credentials.with_scopes(scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=scoped_credentials)

    return service

def auth_check():
    if 'id' in session:
        if session['id'] == open(_path() + 'session', 'r').read():
            return 1
    return 0

def _path():
    path = str(open(str(pathlib.Path().parent.resolve()) + '/path').read())
    if path:
        path += '/'
    return path