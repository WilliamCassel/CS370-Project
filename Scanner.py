from neurosdk.scanner import Scanner
from neurosdk.sensor import Sensor
from neurosdk.brainbit_sensor import BrainBitSensor, SensorFamily
from neurosdk.__cmn_types import *


def on_sensor_state_changed(sensor, state):
    print("Sensor {0} is {1}".format(sensor.Name, state))

def on_brainbit_signal_received(sensor, data):
    print(data)



# Create Scanner
g_scanner = Scanner([SensorFamily.SensorLEBrainBit])
g_sensor = None
def sensorFound(scanner, sensors):
    global g_scanner
    global g_sensor
    for i in range(len(sensors)):
        print('Sensor %s' % sensors[i])
        print('connecting to sensor')
        g_sensor = g_scanner.create_sensor(sensors[i])
        g_sensor.sensorStateChanged = on_sensor_state_changed
        g_sensor.connect()
        g_sensor.signalDataReceived = on_brainbit_signal_received
        g_scanner.stop()

g_scanner.sensorsChanged = sensorFound


print("Starting scan")
# Start Search
g_scanner.start()

def get_headband_sensor_object():
    return g_sensor



