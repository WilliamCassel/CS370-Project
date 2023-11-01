from flask import Flask,render_template,request, redirect, url_for, g, session
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_session import Session
import jwt

import sys
import datetime
import bcrypt
import traceback

from tools.eeg import get_headband_sensor_object


from db_con import get_db_instance, get_db

#from tools.token_required import token_required

#used if you want to store your secrets in the aws valut
#from tools.get_aws_secrets import get_secrets

from tools.logging import logger

ERROR_MSG = "Ooops.. Didn't work!"


#Create our app
app = Flask(__name__)
app.secret_key = 'secret_key'
Session(app)
#add in flask json
FlaskJSON(app)

#g is flask for a global var storage 
def init_new_env():
    #To connect to DB
    if 'db' not in g:
        g.db = get_db()

    if 'hb' not in g:
        g.hb = get_headband_sensor_object()

    #g.secrets = get_secrets()
    #g.sms_client = get_sms_client()

#This gets executed by default by the browser if no page is specified
#So.. we redirect to the endpoint we want to load the base page
@app.route('/') #endpoint
def index():
    return redirect('/static/index_updated.html')

#https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/ this as reference

@app.route('/signup', methods=['POST'])
def signup():
        db, cur = get_db_instance()
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        cur.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        db.commit()
        db.close()
        flash("Registration successful")
        session['logged_in'] = True  # Store a session variable to indicate the user is logged in
        session['name'] = username
        return redirect('/landingPage')
  


@app.route('/landingPage')
def landing_page():
    if not session.get('logged_in'):
        flash("NOT LOGGED IN!")
        return render_template('login.html')
    
    return render_template('/static/landingPage.html')


@app.route('/login', methods=['POST'])
def login():
    db, cur = get_db_instance()
    username = request.form.get('username')
    password = request.form.get('password')

    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)) #check if username and passwords match
    user_data = cur.fetchone()
    if user_data is not None:
        session['logged_in'] = True  # Store a session variable to indicate the user is logged in
        session['name'] = username
        return redirect('/landingPage') 
    
    flash("Invalid login credentials")
    return render_template('/static/login.html')



@app.route("/secure_api/<proc_name>",methods=['GET', 'POST'])
#@token_required
def exec_secure_proc(proc_name):
    logger.debug(f"Secure Call to {proc_name}")

    #setup the env
    init_new_env()

    #see if we can execute it..
    resp = ""
    try:
        fn = getattr(__import__('secure_calls.'+proc_name), proc_name)
        resp = fn.handle_req()
    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        return json_response(status_=500 ,data=ERROR_MSG)

    return resp



@app.route("/open_api/<proc_name>",methods=['GET', 'POST'])
def exec_proc(proc_name):
    logger.debug(f"Call to {proc_name}")

    #setup the env
    init_new_env()

    #see if we can execute it..
    resp = ""
    try:
        fn = getattr(__import__('open_calls.'+proc_name), proc_name)
        resp = fn.handle_req()
    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        return json_response(status_=500 ,data=ERROR_MSG)

    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)