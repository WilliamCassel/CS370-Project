#neuroSDK imports
from neurosdk.scanner import Scanner
from neurosdk.sensor import Sensor 
from neurosdk.brainbit_sensor import BrainBitSensor, SensorFamily
from neurosdk.cmn_types import BrainBitSignalData
from neurosdk.__cmn_types import *

#standard library imports
import pickle
import sqlite3
import csv

#local imports
from tools.logging import logger
from db_con import get_db_instance, get_db

#flask imports
from flask import Flask,render_template,request, redirect, url_for, g, session, flash





hb_data = []

db_connection = sqlite3.connect('db.sqlite')

cursor = db_connection.cursor()


def on_sensor_state_changed(sensor, state):
    logger.debug("Sensor {0} is {1}".format(sensor.Name, state))

def on_brainbit_signal_received(sensor, data):
    global hb_data
    logger.debug(data)
    logger.debug('\n')
    #hb_data.append(data)
    
    sensor_value = [(item.O1, item.O2, item.T3, item.T4) for item in data]

    hb_data.extend(sensor_value)

    hb_data_pickle = pickle.dumps(hb_data)

    username = "t2"
    cursor.execute("UPDATE users SET hb_data = ? WHERE username = ?", (hb_data_pickle, username))
    db_connection.commit()
    db_connection.close()


logger.debug("Create Headband scanner")
# Create Scanner
g_scanner = Scanner([SensorFamily.SensorLEBrainBit])
g_sensor = None
logger.debug("Sensor found call back")
def sensorFound(scanner, sensors):
    global g_scanner
    global g_sensor
    for i in range(len(sensors)):
        logger.debug('Sensor %s' % sensors[i])
        logger.debug('connecting to sensor')
        g_sensor = g_scanner.create_sensor(sensors[i])
        g_sensor.sensorStateChanged = on_sensor_state_changed
        g_sensor.connect()
        g_sensor.signalDataReceived = on_brainbit_signal_received
        g_scanner.stop()
        del g_scanner

g_scanner.sensorsChanged = sensorFound


logger.debug("Starting scan")
# Start Search
g_scanner.start()


def get_headband_sensor_object():
    #print("Headband asenor has been found")
    return g_sensor



if __name__ == "__main__":
    print("Testig receiving data", "\n")