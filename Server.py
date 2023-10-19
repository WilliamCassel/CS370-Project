from flask import Flask, render_template, request, redirect, url_for, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

from Scanner import get_headband_sensor_object
from database import get_instance, get_db

import webbrowser
import os



#creates app
app = Flask(__name__)
#add to flask json 
FlaskJSON(app)
 
@app.route("/")
def init_new():
   if 'db' not in g:
      g.db = get_db()
    
   if 'hb' not in g:
      g.hb = get_headband_sensor_object()


@app.route('/')
def index():
   return redirect('/static/index.html')


@app.route("/open_calls/<proc_name>", methods=['GET', 'POST'])
def exex_proc(proc_name):
   init_new()

   resp = ""

   fn = getattr(__import__('open_calls.'+proc_name), proc_name)
   resp = fn.handle_request()

   return resp
      

webbrowser.open_new_tab('index.html')
   
   
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")

