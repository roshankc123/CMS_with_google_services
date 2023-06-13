# helper script contain all scripts or functions for running this app
#use a mapper to extract relevant data then compile the data and send
#lot of code here isn't changed so that one can understand it with use cases

from auth import get_service
from auth import _path as path
import consts
import json
import forms


# move file to shared folder, (:str, :dict)
# create a sub folder of shared folder and use its id here
# - /shared that folder with service account
# - - /form (to collect form data)
# - - - /form response images
# - other folder in service account

# get the working directory of code
def _path():
    return path()


def move_file(fileId):
    service = get_service(api_name='drive',api_version='v3',)
        
    file = service.files().get(fileId=fileId, fields='parents').execute()

    previous_parents = ",".join(file.get('parents'))

    return service.files().update(fileId=fileId, addParents=consts.folderId,removeParents=previous_parents,fields='id, parents').execute()

# to copy form to service account destination, (( :str, fileId:str), url:str)
def copy_file(type = '', srcFile = 'give_some_source_file'):
    service = get_service(api_name='drive',api_version='v3',)

    origin_file_id = srcFile  # example ID

    copied_file = {}#{'name': newname}

    results = service.files().copy(fileId=origin_file_id, body=copied_file).execute()  #replicate file in same folder

    move_file(results['id'])  #move the replicated one to shared folder
    
    # appending new form id 
    if type == 'committee':
        fileName = 'committee.json'
        data = json.load(open(_path() + fileName))
        data[str(int(list(data.keys())[-1]) + 1)] = results['id']
        json.dump(data, open(_path() + fileName, 'w'))

    # update_title_of_form(results['id'],results['name'])  #update title of file(no need)

    return forms.get_form_url(results['id'])  #get the responder url of file

# just to print the list of files of shared folder(shared folder is the one that is accessed by both service and main account)
# ( null , null)
def get_files():

    service = get_service(api_name='drive',api_version='v3',)

    results = service.files().list(
            ).execute()   #, fields="nextPageToken, files(id, name)"
    
    items = results.get('files', [])

    if not items:
        print('No files found.')
        return
    
    print('Files:')

    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))
