from flask import request, g
from neurosdk.cmn_types import *
from tools.logging import logger
import pickle


def handle_req():
    if g.hb == None:
        return ["No Headband, No Data"]
    
    g.hb.exec_command(SensorCommand.CommandStartSignal)
    return ["Data Flowing"]
