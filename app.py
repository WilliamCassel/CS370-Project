from flask import Flask, render_template, request, redirect, url_for, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import sys 
import datetime
import bcrypt
import traceback

from tools.eeg import get_headband_sensor_object

from db_config import get_instance, get_db

import webbrowser
import os

from tools.logging import logger

ERROR_MSG = "Didn't work!"

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
   try:
      fn = getattr(__import__('open_calls.'+proc_name), proc_name)
      resp = fn.handle_request()
   except Exception as err:
      ex_data = str(Exception) + '\n'
      ex_data = ex_data + str(err) + '\n'
      ex_data = ex_data + traceback.format_exc()
      logger.error(ex_data)
      return json_response(status_=500 ,data=ERROR_MSG)
   
   return resp
      

webbrowser.open_new_tab('index.html')
   
   
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")

