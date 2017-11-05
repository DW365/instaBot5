# -*- coding: utf-8 -*-
from flask import Flask, request
from flask import render_template, send_from_directory, redirect
import flask
import json
import locale
import io
from werkzeug.contrib.fixers import ProxyFix
import flask_login
import subprocess
import gspread
from oauth2client.service_account import ServiceAccountCredentials


#locale.setlocale(locale.LC_ALL, 'ru_RU.UTF8')
#locale.setlocale(locale.LC_ALL, 'russian')



app = Flask(__name__, static_url_path='/templates')
app.secret_key = 'super secret string'


@app.route('/parser5/panel/', methods=['POST', 'GET'])
@flask_login.login_required
def main():
    filedata = None
    with open('../data') as data_file:
        filedata = json.load(data_file)
    return render_template('main.html', insta_login = filedata['insta_login'], insta_password=filedata['insta_password'],
                           delay = filedata['delay'],
                           main_table = filedata['main_table'],
                           proxy = filedata['proxy'],
                           log=io.open('../bot.log', 'r', encoding='utf-8').read())
    # log=io.open('parser.log', 'r', encoding='utf-8').read(),
    #                        bloggers = filedata['bloggers'],
    #                        ypassword=filedata['ypassword'],
    #                        ylogin=filedata['ylogin'],
    #                        delay = filedata['delay'],
    #                        proxy = filedata['proxy'])


@app.route('/parser5/save', methods=['POST'])
@flask_login.login_required
def save():
    js = json.dumps(request.form, ensure_ascii=False)
    with open("../data", "w") as text_file:
        text_file.write(js)
    return redirect("/parser5/panel", code=302)


def createTable(name):
    scope = ['https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('../test-92ef740f572c.json', scope)
    gc = gspread.authorize(credentials)
    sheet = gc.create(name)
    sheet.share(None, perm_type='anyone', role='reader')
    link = "https://docs.google.com/spreadsheets/d/" + sheet.id
    return link

@app.route('/parser5/new', methods=['POST'])
@flask_login.login_required
def new():
    with open('../data') as data_file:
        filedata = json.load(data_file)
    sid = filedata['main_table']
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('../test-92ef740f572c.json', scope)
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/" + sid)
    link = createTable(request.form['name'])
    worksheet = sheet.sheet1
    worksheet.append_row([link,"","","","","","","",""])
    return redirect("/parser5/panel", code=302)

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route('/parser5/', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='/parser5/' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    email = flask.request.form['email']
    if flask.request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect("/parser5/panel/", code=302)

    return 'Bad login'



users = {'admin': {'pw': '1qiVRfZtc1mw'}}

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=80)