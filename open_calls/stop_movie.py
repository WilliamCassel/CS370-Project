from flask import request, g
from neurosdk.cmn_types import *

def handle_req():
    if g.hb == None:
        return ["Sensor stopped"]
    
    g.hb.exec_command(SensorCommand.CommandStopSignal)
    return ["Sensor Stopped"]