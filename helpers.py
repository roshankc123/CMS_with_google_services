# helper script contain all scripts or functions for running this app
#use a mapper to extract relevant data then compile the data and send
#lot of code here isn't changed so that one can understand it with use cases

from auth import get_service
from auth import _path as path
import consts
import json
import pathlib


# move file to shared folder, (:str, :dict)
# create a sub folder of shared folder and use its id here
# - /shared that folder with service account
# - - /form (to collect form data)
# - - - /form response images
# - other folder in service account
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

    return get_form_url(results['id'])  #get the responder url of file

# just to list out the files of shared folder(shared folder is the one that is accessed by both service and main account)
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


# update title of the form , ((formId:str, :str, :str), :dict)
def update_title_of_form(formId, title="new form", description=''):

    service = get_service(api_name='forms',api_version='v1',)

    update = {
        "requests": [{
            "updateFormInfo": {
                "info": {
                    "title": title,
                    "documentTitle" : title
                },
                "updateMask": "*"
            }
        }]
    }

    return service.forms().batchUpdate(formId=formId, body=update).execute() # Update the form with a description

#get description of form, (:str, :dict)
def get_form_detail(formId):

    service = get_service(api_name='forms',api_version='v1',)

    result = service.forms().get(formId=formId).execute()

    return result
# print(get_form())

#extract url of form, (formId:str, url:str)
def get_form_url(formId):
    return get_form_detail(formId)['responderUri']


#extract and create image link , (:dict, :list)
def create_image_url(link):   
    if not link.count('='):
        return ''
    return  'https://drive.google.com/uc?id=' + link.split('=')[1]


# using thumbnail for low resolution images(like in committee page)
# reduce bandwidth usage and improve speed
def convert_link_to_public_thumbnail(link):
    # print(link)
    if not link.count('='):
        return ''
    return 'https://drive.google.com/thumbnail?id=' + link.split('=')[1]  #use thumbnails, small size and load faster


#extract answers from text response, (:dict, :list)
def get_text_answers(textAnswer):
    result = []
    for temp in textAnswer['textAnswers']['answers']:
        # print(temp['value'])
        result.append(temp['value'])
    return result
        

#to create beautifully decorated json , (formType:enum, :list)
def formMapper(formType = 'committee'):
    # formtype = commitee, achievement, event
    if formType == 'committee':
        return ['position','name','fb','insta', 'twitter', 'linkedin', 'image']
    elif formType == 'achievements':
        return ['id', 'timestamp','title','image','desc','date', 'fb', 'youtube', 'medium', 'insta']
    elif formType == 'events':
        return ['title','formLink', 'image','desc','date', 'type', 'fb', 'youtube', 'medium', 'insta', 'status']

# extarct from data, ((formId:str, formType:enum), :dict)
# simply form name as a formType , only committee,achievements and events are defined for now 
def retrieve_form_data(formId, formType='committee'):  
    service = get_service(api_name='forms',api_version='v1',)
    formData = service.forms().responses().list(formId=formId).execute()

    #check if there is any data or not, if not return empty dict
    if not formData.get('responses'):
        return {}

    questionId = get_form_question_id(formId)
    result = {}
    responseMapper = formMapper(formType)      #to beautify the json
    for temp in formData['responses']:
        # print(temp)
        indivisual = {}
        i = 0
        for id in questionId:
            if dict.get(temp['answers'],id):  #skip if no answer id found, so response with no data will not have key
                # print(temp['answers'][id])
                if temp['answers'][id].get('textAnswers'):
                    indivisual[responseMapper[i]] = get_text_answers(temp['answers'][id])
                elif temp['answers'][id].get('fileUploadAnswers'):
                    indivisual[responseMapper[i]] = convert_link_to_public_thumbnail(temp['answers'][id])
            i += 1
        if formType == 'committee':                         ##construct a data of committee
            if result.get(indivisual['position'][0]):
                result[indivisual['position'][0]].append(indivisual)
            else:
                result[indivisual['position'][0]] = [indivisual]
        elif formType == 'achievements':                    ##construct a data of achievements
            if result.get('achievements'):
                result['achievements'].append(indivisual)
            else:
                result['achievements'] = [indivisual]
        elif formType == 'events':                          #construct a data of events
            if result.get('events'):
                result['events'].append(indivisual)
            else:
                result['events'] = [indivisual]
    return result


# extract id of each question to create a accurate mapping, (:str, :list)
def get_form_question_id(formId):
    items = get_form_detail(formId)['items']
    result = []
    for temp in items:
        result.append(temp['questionItem']['question']['questionId'])
    return result


def _path():
    return path()



# retrieve sheet data by sheet id
def retrieve_sheets_data(sheetId, formType = 'committee'):
    service = get_service(api_name='sheets',api_version='v4',)
    if formType == 'committee':
        tempResult = {}
        ranges = 'r2c1:r100c15'  #specify the fields range
    response = service.spreadsheets().values().batchGet(
            spreadsheetId=sheetId, ranges=ranges, majorDimension='ROWS').execute()

    
    result = {}

    for temp in response['valueRanges']:
        if 'values' not in temp:
            return {}

    result['data'] = temp
    return result

