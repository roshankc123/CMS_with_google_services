import flask
# import requests
# from OpenSSL import SSL
from flask_cors import CORS
from flask import session

import youtube
import drive
import forms
import sheets



app = flask.Flask(__name__)
app.secret_key = ''   #for debug toolbar(hex key)
CORS(app) #recommended to use specific origins

# home page 
@app.route('/', methods=['GET'])
def index():
    return 'success'
    
# 
@app.route('/form_data', methods=['GET'])  #return data of specific committee 
def form_data():
    formId = 'put form id here'
    return forms.retrieve_form_data(formId, 'committee'), 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.route('/sheet_data', methods=['GET'])  #return data of events
def sheet_data():
    sheetId = 'sheets id here'
    return sheets.retrieve_sheets_data(sheetId, formType='events'), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/youtube_data', methods=['GET'])  #return data of youtube
def youtubeg():
    return open('templates/youtube.html', 'r').read()

@app.route('/youtube_data/list', methods=['GET'])  #return data of youtube
def youtubelist():
    return youtube.fetch_playlist('PLbpi6ZahtOH6G_A4_RLzzqdVf4TG5ilzf', ), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/youtube_data/list/<token>', methods=['GET'])  #return data of youtube
def youtubelisttoken(token):
    return youtube.fetch_playlist('PLbpi6ZahtOH6G_A4_RLzzqdVf4TG5ilzf', token), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(port=8000)