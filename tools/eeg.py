from neurosdk.scanner import Scanner
from neurosdk.sensor import Sensor
from neurosdk.brainbit_sensor import BrainBitSensor, SensorFamily
from neurosdk.__cmn_types import *

from tools.logging import logger
from db_con import get_db_instance, get_db


def on_sensor_state_changed(sensor, state):
    logger.debug("Sensor {0} is {1}".format(sensor.Name, state))

def on_brainbit_signal_received(sensor, data):
    logger.debug(data)
    #db, cur = get_db_instance()
    #command = ("INSERT INTO USERS (data) VALUES (?)")
    #value = (data)
    #cur.execute(command, value)
    #db.commit()
    #db.close()


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



