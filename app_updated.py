from flask import Flask,render_template,request, redirect, url_for, g, session, flash
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_session import Session
import jwt
import sys
import datetime
import bcrypt
import traceback
import pickle

from tools.eeg import get_headband_sensor_object


from db_con import get_db_instance, get_db


#from tools.token_required import token_required

#used if you want to store your secrets in the aws valut
#from tools.get_aws_secrets import get_secrets

from tools.logging import logger

ERROR_MSG = "Ooops.. Didn't work!"


#Create our app
app = Flask(__name__)
app.static_folder = '/templates'
#Session(app)
#add in flask json
app.secret_key = 'secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
FlaskJSON(app)

Session(app) 
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
    return render_template('/index_updated.html')

#https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/ this as reference

@app.route('/signedUp', methods=['POST'])
def signedUp():
        db, cur = get_db_instance()
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hb_data = ""
        #cur.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?);', (username, email, password))
        #command = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        email_check = cur.fetchone()
        if email_check is None:
            command = "INSERT INTO users (username, email, password, hb_data) VALUES (?, ?, ?, ?)"
            values = (username, email, password, hb_data)
            cur.execute(command, values)
            db.commit()
            db.close()
            flash("Registration successful")
            session['logged_in'] = True  # Store a session variable to indicate the user is logged in
            session['name'] = username
            return render_template('landingPage.html')
        flash("Account already exists!")
        return redirect("/signUp")
  

@app.route('/signUp', methods=['POST', 'GET'])
def signup():
        return render_template('signUp.html')




@app.route('/landingPage', methods=['POST', 'GET'])
def landing_page():
    if session['logged_in'] == False:
        flash("NOT LOGGED IN!")
        return redirect('/static/login.html')
    
    #return redirect('/static/landingPage.html')
    return render_template('landingPage.html')


@app.route('/matches', methods=['POST', 'GET'])
def matches():
    if session['logged_in'] == False:
        flash("NOT LOGGED IN!")
        return redirect('/static/login.html')
    #ADD MATCH SESSION TOKENS HERE
    #return redirect('/static/landingPage.html')
    db, cur = get_db_instance()
    cur.execute("SELECT username, email FROM users;") 
    users= cur.fetchall()
    #session['match'] = "" #Placeholder, probably not going to be used since we can just pass the matches through as parameters in render_template
    return render_template('matches.html', users = users)


@app.route('/watchVids', methods=['POST'])
def watchVids():
    if session['logged_in'] == False:
        flash("NOT LOGGED IN!")
        return render_template('/login.html')
    
    return render_template('watchVids.html')
    #return redirect('/static/landingPage.html')


@app.route('/loggedIn', methods=['POST'])
def loggedIn():
    db, cur = get_db_instance()
    username = request.form.get('username')
    password = request.form.get('password')
    #cur.execute("DROP TABLE friendslist")
    #cur.execute("CREATE TABLE friendslist(user TEXT, friend TEXT, PRIMARY KEY (user, friend), FOREIGN KEY(user) REFERENCES users(user), FOREIGN KEY(friend) REFERENCES users(user))")
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)) #check if username and passwords match
    user_data = cur.fetchone()
    if user_data is not None:
        session['logged_in'] = True  # Store a session variable to indicate the user is logged in
        session['name'] = username
        return redirect('/landingPage') 
    
    flash("Invalid login credentials")
    return render_template('/login.html')


@app.route('/login', methods = ['POST'])
def login():
    return render_template('login.html')



@app.route('/add_friend/<user>/<friend>', methods=['POST'])
def add_friend(user, friend):
    db, cur = get_db_instance()
    cur.execute('SELECT user FROM friendslist WHERE user = ? and friend = ?', (user, friend))
    friendcheck = cur.fetchone()
    if friendcheck is None:
        cur.execute('INSERT INTO friendslist (user, friend) VALUES (?, ?)', (user, friend))
        db.commit()
    cur.execute('SELECT * FROM messages WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)',(user, friend, friend, user))
    messages = cur.fetchall()
    db.close()
    return render_template('private_message.html', sender=user, receiver=friend, messages=messages) 


@app.route('/friends/<user>', methods=['POST'])
def display_friends(user):
    db, cur = get_db_instance()
    cur.execute('SELECT * FROM friendslist WHERE user = ?', (user,))
    friends = cur.fetchall()
    db.close()

    return render_template('friends_list.html', friends=friends)



@app.route('/logout', methods=['POST'])
def logout():
    session['logged_in'] = False
    session['name'] = None
    return render_template('index_updated.html')

def update_db():
    with open("hb_data.pickle", "rb") as file:
         
        loaded_data = pickle.load(file)
        db, cur = get_db_instance()
        username = request.form.get('username')
        session['name'] = username
        command = "UPDATE users SET hb_data = ? WHERE username = ?"
        value = (loaded_data, session['name'])
        cur.execute(command, value)
        db.commit()
        db.close()


@app.route('/send_message', methods=['POST'])
def send_message():
    sender_username = request.form['sender']
    receiver_username = request.form['receiver']
    message = request.form['message']
    db, cur = get_db_instance()
    
    cur.execute('INSERT INTO messages (sender_id, receiver_id, message) VALUES (?, ?, ?)',(sender_username, receiver_username, message))
    db.commit()
    db.close()

    return redirect(url_for('private_messages', sender=sender_username, receiver=receiver_username, action='post'))


@app.route('/private_messages/<sender>/<receiver>', methods=['POST', 'GET'])
def private_messages(sender, receiver):
    db, cur = get_db_instance()

    cur.execute('SELECT * FROM messages WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)',(sender, receiver, receiver, sender))
    messages = cur.fetchall()
    db.close()

    return render_template('private_message.html', sender=sender, receiver=receiver, messages=messages)


@app.route('/private_messages_from_friendslist/<sender>/<receiver>', methods=['POST', 'GET']) ##annoying, but idk how else to fix the back button issue
def private_messages_from_friendslist(sender, receiver):
    db, cur = get_db_instance()

    cur.execute('SELECT * FROM messages WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)',(sender, receiver, receiver, sender))
    messages = cur.fetchall()
    db.close()

    return render_template('private_messages_from_friendslist.html', sender=sender, receiver=receiver, messages=messages)


@app.route('/send_message_from_friendslist', methods=['POST'])
def send_message_from_friendslist():
    sender_username = request.form['sender']
    receiver_username = request.form['receiver']
    message = request.form['message']
    db, cur = get_db_instance()
    
    cur.execute('INSERT INTO messages (sender_id, receiver_id, message) VALUES (?, ?, ?)',(sender_username, receiver_username, message))
    db.commit()
    db.close()

    return redirect(url_for('private_messages_from_friendslist', sender=sender_username, receiver=receiver_username, action='post'))



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
    db, cur = get_db_instance()
    