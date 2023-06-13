# contains method to retrieve form data

from auth import get_service


# update the title of form
def update_title_of_form(formId, title="new form"):

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


#extract answers from text response in forms, (:dict, :list)
def get_text_answers(textAnswer):

    result = []

    for temp in textAnswer['textAnswers']['answers']:
        # print(temp['value'])
        result.append(temp['value'])

    return result
        

#to create beautifully decorated json , (formType:enum, :list)
# define the fields of data expected in a specified order

def formMapper(formType = 'committee'):

    # formtype = commitee, achievement, event
    if formType == 'committee':
        return ['position','name','fb','insta', 'twitter', 'linkedin', 'image']
    
    elif formType == 'achievements':
        return ['id', 'timestamp','title','image','desc','date', 'fb', 'youtube', 'medium', 'insta']
    
    elif formType == 'events':
        return ['title','formLink', 'image','desc','date', 'type', 'fb', 'youtube', 'medium', 'insta', 'status']


# extract id of each question to create a accurate mapping, (:str, :list)
def get_form_question_id(formId):

    items = get_form_detail(formId)['items']

    result = []

    for temp in items:
        result.append(temp['questionItem']['question']['questionId'])

    return result


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

    responseMapper = formMapper(formType)

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

            result[formType].append(indivisual)

    return result




# ###############
#  below code is the live use case of a project
# #############


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
