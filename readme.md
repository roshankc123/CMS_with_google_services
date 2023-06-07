# google-service-api

you will need service account credentials as a json file and a folder id to store all data, 

first create a service account of your google account

1. go to https://console.cloud.google.com/ and create project
2. goto crediantials section and create service account, you will get service account email address
3. do as it says
4. download credentials.json form it
5. not get back and go to OAuth consent screen
6. fill the form
7. under scope section,  add https://www.googleapis.com/auth/drive to scope manually
8. specify users who can access to the  app

then enable the api by following:

1. goto library section
2. enable forms, sheets, drive api

make neccessary folders in drive

1. create a new folder in drive 'datas' lets say
2. share a folder with your service account mail
3. get a folder id, click on copy folder-sharing link, there you can find a folder id
4. implement a folder id in code

find out more on:

1. https://docs.google.com/document/d/1An5IxVYPGuZ3EnQVkvWWrwB_2N1DP-ZkxBRla-6vS9k/edit?usp=sharing
2. https://docs.google.com/document/d/15kduoQwEFnPjY2m9nJ5oX9FrJniCWXIdCeYNNzaVBFw/edit?usp=sharing

Directory structure:
    –/mysite/
    —-/templates/
    —-—-/.html files
    —-/app.py    - main server entry point
    —-/consts.py   - contain constant variables such as base form id(base form id look below)
    —-/helpers.py  - backbone of the system, contain all custom made modules needed
    —-/auth.py   - contain code related to authentication and authorization
    —-/credentials.json   -  contain google service account credentials
    —-/committee.json  - has form id of all committee registered so that one can get data of all committee as per requirement
    —-/sessions  -  only one user can login at a time

Base form id: in order to make a form replication possible a base form is needed from which a copy is made , this form is there for yearly recurring events like robo-rookies, committee form, member intake.
