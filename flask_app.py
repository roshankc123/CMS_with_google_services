import flask
# import requests
import helpers
# from OpenSSL import SSL
from flask_cors import CORS
from flask import session
import time
import auth
import consts
import json



app = flask.Flask(__name__)
app.secret_key = ''   #for debug toolbar(hex key)
CORS(app) #recommended to use specific origins

# home page 
@app.route('/', methods=['GET'])
def index():
    if auth.auth_check() == 1:
        return flask.render_template('index.html', forms = consts.basEventFormId)
    else:
        return flask.redirect(flask.url_for('login'))
    

# create a new form with defined type
@app.route('/create', methods=['GET', 'POST'])
def create():
    if auth.auth_check() == 0:  #redirect to login if not logged in
        return flask.redirect(flask.url_for('login'))

    if flask.request.args.get('type') == 'committee':
        return helpers.copy_file(type = 'committee',srcFile=consts.baseCommitteeFormId)

    else:
        # replicate_other()
        pass
    return ''    


# open the content management form of site
@app.route('/goto/<name>', methods=['GET'])
def goto(name):
    if auth.auth_check() == 0:  #redirect to login if not logged in
        return flask.redirect(flask.url_for('login'))
    if name == 'committee':
        # below one line gets recent form url and redirect there
        temp = list(dict.values(json.load(open(helpers._path() + 'committee.json'))))
        formId = temp[-1]
    elif name == 'achievement':
        formId = consts.achievementFormId
        # return flask.redirect(helpers.get_form_url(consts.achievementFormId))
    elif name == 'event':
        formId = consts.eventsFormId
    elif name == 'committeelist':   #list of all committee forms
        data = json.load(open(helpers._path() + 'committee.json'))
        return flask.render_template('committee.html', data = data)
    else:
        return ''
    return flask.redirect(helpers.get_form_url(formId))

@app.route('/delete/committee/<cn>', methods=['GET'])  #committee number
def delete_committee(cn):
    fp = open(helpers._path() + 'committee.json', 'r')
    json_data = json.load(fp)
    # initial = fp.read()
    dict.pop(json_data,cn)          #popped data is discarded
    open(helpers._path() + 'committee.json', 'w').write(json.dumps(json_data))  #data was not flushing in r+ mode
    return flask.redirect('/goto/committeelist')

@app.route('/committee', methods=['GET'])  #return data of latest committee 
def committee():
    temp = json.load(open(helpers._path() + 'committee.json'))
    formId = list(temp.values())[-1]
    if list(temp.keys())[-1] == '17':
        return helpers.retrieve_sheets_data('1Msw5c1WfO-iU-tpJDl07k1uVKbVKKo7DbqdRbLFB_Ow','committee'), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif list(temp.keys())[-1] == '18':
        return helpers.retrieve_sheets_data('1D2b6VqXTelM3KKlpRXaJ8aHEJdBAg9PCJbzBQCtlOUI','committee'), 200, {'Content-Type': 'application/json; charset=utf-8'}
    return helpers.retrieve_form_data(formId, 'committee'), 200, {'Content-Type': 'application/json; charset=utf-8'}

# ''
@app.route('/committee/<sn>', methods=['GET'])  #return data of specific committee 
def committee_sn(sn):
    if sn == '17':
        return helpers.retrieve_sheets_data('1Msw5c1WfO-iU-tpJDl07k1uVKbVKKo7DbqdRbLFB_Ow','committee'), 200, {'Content-Type': 'application/json; charset=utf-8'}
    # else below
    temp = json.load(open(helpers._path() + 'committee.json'))
    formId = temp.get(sn)
    if not formId:
        return {}
    return helpers.retrieve_form_data(formId, 'committee'), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/achievements', methods=['GET'])  #return data of achievements
def achievements():
    return helpers.retrieve_sheets_data(consts.achievementSheetId,'achievements'), 200, {'Content-Type': 'application/json; charset=utf-8'}
    # return helpers.retrieve_form_data('14R-yg03cE54dNtN_7FHSBjDndc1co_ZsIQcDntLnoxc', 'achievements'), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/achievements/<sn>', methods=['GET'])  #return data of specific achievements(in development)
def achievements_sn(sn):
    return {"data":[{"date":[""],"desc":["in development"],"fb":["https://www.facebook.com/wrcrobo/photos/pcb.6466038650077149/6466016593412688"],"image":["https://drive.google.com/uc?id=15Y4rkjCwlLfcePwQrp_gTxvZf3C90INb"],"insta":[""],"medium":[""],"title":[""],"youtube":[""]}]}, 200, {'Content-Type': 'application/json; charset=utf-8'}

# 
@app.route('/events', methods=['GET'])  #return data of events
def events():
    return helpers.retrieve_sheets_data(consts.eventsSheetId, formType='events'), 200, {'Content-Type': 'application/json; charset=utf-8'}

# simple authentication added (non functional requirements)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if auth.auth_check() == 1:
        return flask.redirect(flask.url_for('index'))
    if flask.request.method == 'POST':
        if flask.request.form['name'] == 'admin' and flask.request.form['password'] == 'hellow' :
            session['id'] = str(hash(time.time()))
            open(helpers._path() + 'session', 'w').write(str(session['id']))
            return flask.redirect(flask.url_for('index'))
        return {}
    else:
        return flask.render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'id' in session:
        session.pop('id')
        open(helpers._path() + 'session', 'w').close()
    return flask.redirect(flask.url_for('login'))


if __name__ == '__main__':
    app.run(port=8000)