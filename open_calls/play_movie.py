from flask import request, g
from neurosdk.cmn_types import *
from tools.logging import logger

def handle_req():
    if g.hb == None:
        return ["Data Flowing"]
    
    g.hb.exec_command(SensorCommand.CommandStartSignal)
    return ["Data Flowing"]