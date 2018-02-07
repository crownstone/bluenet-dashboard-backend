import json

class WSParser:
    bluenetInstance = None
    
    def __init__(self):
        pass
    
    def connectToBluenet(self, bluenetInstance):
        self.bluenetInstance = bluenetInstance
    
    def receiveWebSocketCommand(self, stringifiedJson):
        print("Raw Data", stringifiedJson)
        
        try:
            data = json.loads(stringifiedJson)
        except:
            print("ERROR: couldn't parse", stringifiedJson)
            return
        
        if data["type"] == "command":
            self._handleCommand(data);
            
    def _handleCommand(self, data):
        if data["command"] == "setVoltageLogging":
            self.bluenetInstance._usbDev.setSendVoltageSamples(data["value"])
        elif data["command"] == "setCurrentLogging":
            self.bluenetInstance._usbDev.setSendCurrentSamples(data["value"])
        elif data["command"] == "setFilteredVoltageLogging":
            self.bluenetInstance._usbDev.setSendFilteredVoltageSamples(data["value"])
        elif data["command"] == "setFilteredCurrentLogging":
            self.bluenetInstance._usbDev.setSendFilteredCurrentSamples(data["value"])
        