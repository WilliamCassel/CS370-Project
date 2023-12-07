class BrainBitSignalData:
    def __init__(self, PackNum, Marker, O1, O2, T3, T4):
        self.PackNum = PackNum
        self.Marker = Marker
        self.O1 = O1
        self.O2 = O2
        self.T3 = T3
        self.T4 = T4

mock_data = [
    BrainBitSignalData(PackNum=0, Marker=0, O1=0.1843168109100446, O2=0.15992370598192787, T3=0.1408032806427771, T4=0.15643287318503685), 
    BrainBitSignalData(PackNum=0, Marker=0, O1=0.17181679898910426, O2=0.14742369406098754, T3=0.12830326872183678, T4=0.14393286126409652),
    BrainBitSignalData(PackNum=1, Marker=0, O1=0.18336160980378133, O2=0.1591016379372005, T3=0.14009489068497724, T4=0.15563254893546002),
    BrainBitSignalData(PackNum=1, Marker=0, O1=0.18247087714278903, O2=0.15833373864530434, T3=0.13940404835133396, T4=0.15486731993419642), 
    BrainBitSignalData(PackNum=2, Marker=0, O1=0.18154886393438716, O2=0.1575414252676251, T3=0.1387013804448895, T4=0.15411315356555325), 
    BrainBitSignalData(PackNum=2, Marker=0, O1=0.1806665236153828, O2=0.15680175476241567, T3=0.13801435281214983, T4=0.15338759745368716), 
    BrainBitSignalData(PackNum=3, Marker=0, O1=0.1798631476050831, O2=0.1560933648046158, T3=0.1374104856591088, T4=0.15267386691462223), 
    BrainBitSignalData(PackNum=3, Marker=0, O1=0.17905290513315691, O2=0.15538344896645448, T3=0.13680394821543523, T4=0.15197463223899102)
]

sensor_values = sensor_value = [(item.O1, item.O2, item.T3, item.T4) for item in mock_data]

for i in sensor_value:
    print(i)