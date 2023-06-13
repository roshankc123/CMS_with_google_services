# google-service-api

This repository contains the example code for google servces api of google forms, google sheets, google drive and youtube using a google service api with service account. service account allows us to access google api with no repetative oauth verification. it is best for backend which needs to use google api.

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

read the official project documents at;

1. <https://docs.google.com/document/d/1An5IxVYPGuZ3EnQVkvWWrwB_2N1DP-ZkxBRla-6vS9k/edit?usp=sharing>
2. <https://docs.google.com/document/d/15kduoQwEFnPjY2m9nJ5oX9FrJniCWXIdCeYNNzaVBFw/edit?usp=sharing>

Base form id: in order to make a form replication possible a base form is needed from which a copy is made , this form is there for yearly recurring events like robo-rookies, committee form, member intake.
