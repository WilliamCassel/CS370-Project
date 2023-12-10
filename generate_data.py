import random
import time

#class to hold data
class BrainBitSignalData:
    def __init__(self, PackNum, Marker, O1, O2, T3, T4):
        self.PackNum = PackNum
        self.Marker = Marker
        self.O1 = O1
        self.O2 = O2
        self.T3 = T3
        self.T4 = T4

#to simulate data flow
def generate_data_flow(num_samples, delay, init_values, variation_range=0.05):
    rep_hb_data = []

    current_values = init_values
    
    #iterating to simulate brain data flow
    for i in range(num_samples):
        pack_num = i // 2
        marker = 0

        current_values = [value + random.uniform(-variation_range, variation_range) for value in current_values]

        signal_data = BrainBitSignalData(pack_num, marker, *current_values)
        rep_hb_data.append(signal_data)

        time.sleep(delay)
    return rep_hb_data #returns list of generated brain signals


init_values = [random.uniform(0,1) for _ in range(4)]

variable_data = generate_data_flow(25, 0.25, init_values)

#prints out all the attributes of teh class object
for data in variable_data:
    print(f"BrainBitSignalData(PackNum={data.PackNum}, Marker={data.Marker}, O1={data.O1}, O2={data.O2}, T3={data.T3}, T4={data.T4})")


    