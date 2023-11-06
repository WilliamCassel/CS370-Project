from flask import request, g
from neurosdk.cmn_types import *
from tools.eeg import *
from app_updated import update_db
import pickle


def handle_req():
    if g.hb == None:
        return ["Sensor stopped"]
    
    g.hb.exec_command(SensorCommand.CommandStopSignal)
    with open("hb_data.pickle", "wb") as file:
        pickle.dump(hb_data, file)

    update_db()
    return ["Sensor Stopped"]

