import time

from lib.eventBus import Topics
from lib.eventBus import eventBus

import re

USE_DATA = "__DATA__"
match = {
    "Set name to ":           {"type": "getName",             "value": USE_DATA},
    "BLE Address: ":          {"type": "getMacAddress",       "value": USE_DATA},
    "Start advertising":      {"type": "setAdvertisements",   "value": True},
    "Advertising stopped":    {"type": "setAdvertisements",   "value": False},
    "Configure setup mode":   {"type": "setMode",             "value": 'SETUP'},
    "Configure normal mode":  {"type": "setMode",             "value": 'NORMAL'},
}

class UartParser:

    def __init__(self):
        eventBus.on(Topics.uartReadLine, self.parse)
        eventBus.on(Topics.simulatedUartReadLine, self.parseSimulator)


    def parseSimulator(self, simulatedLineData):
        """ this is invoked for every line received over the uart """
        messageType, payload, timestamp = self.decomposeSimulated(simulatedLineData)

        self.translateMessage(messageType, payload, timestamp)

    def parse(self, uartLineData):
        """ this is invoked for every line received over the uart """
        messageType, payload = self.decompose(uartLineData)
        timestamp = round(time.time() * 1000)  # millis since epoch

        self.translateMessage(messageType, payload, timestamp)


    def decomposeSimulated(self,dataStr):
        timestampLength = 13
        timestamp = int(dataStr[:timestampLength])
        # do some parsing to fill the type and payload with the appropriate content
        messageType, payload = self.decompose(bytes(dataStr[timestampLength:]))

        return messageType, payload, timestamp

    def decompose(self,data):
        """ this method will seperate the type from the payload """
        data = data.rstrip()
        print(data)
        # do some parsing to fill the type and payload with the appropriate content
        messageType = None
        payload = None

        # strip color codes
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        data = ansi_escape.sub('', data)

        readStart = 41

        for key in match:
            length = len(key)
            if data[readStart:readStart+length] == key:
                messageType = match[key]["type"]
                if match[key]["value"] == USE_DATA:
                    payload = data[readStart+length:len(data)]
                else:
                    payload = match[key]["value"]

        #print(data[41:-1])
        # if data[41:53] == "Set name to ":
        #     messageType = "getName"
        #     payload = data[54:-1]
        # elif data[41:54] == "BLE Address: ":
        #     messageType = "getMacAddress"
        #     payload = data[54:71]
        # elif data[41:58] == "Start advertising":
        #     messageType = "setAdvertisements"
        #     payload = True
        # elif data[41:57] == "Stop advertising":
        #     messageType = "setAdvertisements"
        #     payload = False



        #print(payload)




        return messageType, payload


    def translateMessage(self, messageType, payload, timestamp):
        translatedType = None
        data = None
        #print(messageType, payload, timestamp)

        translatedType = messageType
        data = {"value": payload}  # fill dictionary


        # ... and so on

        wsMessage = self.constructMessage(translatedType, data, timestamp)

        eventBus.emit(Topics.wsWriteMessage, wsMessage)


    def constructMessage(self, translatedType, data, timestamp):
        return {
            'timestamp': timestamp,
            'type': translatedType,
            'data': data,
        }

"""
case 'getName':
    store.dispatch({type:'STATE_UPDATE', data: {name: 'test' }}); // TODO: match messageObj.data to the value which is set to true.
break;
case 'getMacAddress':
    store.dispatch({type:'STATE_UPDATE', data: {macAddress: '12:32:43:ff' }}); // TODO: match messageObj.data to the value which is set to true.
break;
case 'setRelay':
    store.dispatch({type:'STATE_UPDATE', data: {relayEnabled: true }}); // TODO: match messageObj.data to the value which is set to true.
break;
case 'setAdvertisements':
    store.dispatch({type:'STATE_UPDATE', data: {advertisementsEnabled: true }}); // TODO: match messageObj.data to the value which is set to true.
break;
case 'setMesh':
    store.dispatch({type:'STATE_UPDATE', data: {meshEnabled: true }}); // TODO: match messageObj.data to the value which is set to true.
break;
case 'setIGBT':
    store.dispatch({type:'STATE_UPDATE', data: {igbtState: true }}); // TODO: match messageObj.data to the value which is set to true.
break;
case 'setVoltageRange':
    store.dispatch({type:'STATE_UPDATE', data: {voltageRange: true }}); // TODO: match messageObj.data to the value which is set to true.
break;
case 'setCurrentRange':
    store.dispatch({type:'STATE_UPDATE', data: {currentRange: true }}); // TODO: match messageObj.data to the value which is set to true.
break;
case 'setVoltageDifferential':
    store.dispatch({type:'STATE_UPDATE', data: {differentialVoltage: true }}); // TODO: match messageObj.data to the value which is set to true.
break;
case 'setCurrentDifferential':
    store.dispatch({type:'STATE_UPDATE', data: {differentialCurrent: true }}); // TODO: match messageObj.data to the value which is set to true.
break;
case 'toggleMeasurementChannel':
    store.dispatch({type:'STATE_UPDATE', data: {measureReference: true }}); // TODO: match messageObj.data to the value which is set to true.
break;
case 'currentData':
case 'voltageData':
case 'advertisementData':
"""