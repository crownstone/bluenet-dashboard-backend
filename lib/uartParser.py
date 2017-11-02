import time

from lib.eventBus import Topics
from lib.eventBus import eventBus


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
        # do some parsing to fill the type and payload with the appropraite content
        messageType, payload = self.decompose(bytes(dataStr[timestampLength:]))

        return messageType, payload, timestamp

    def decompose(self,data):
        """ this method will seperate the type from the payload """

        # do some parsing to fill the type and payload with the appropraite content
        messageType = b'typeByte(s)'
        payload = b'dataBytes'

        return messageType, payload


    def translateMessage(self, messageType, payload, timestamp):
        translatedType = None
        data = None

        if messageType == 'dataByte1':
            translatedType = 'advertisement'
            data = {} # fill dictionary
        elif messageType =='dataByte2':
            translatedType = 'powerData'
            data = {} # fill dictionary
        # ... and so on

        wsMessage = self.constructMessage(translatedType, data, timestamp)

        eventBus.emit(Topics.wsWriteMessage, wsMessage)


    def constuctMessage(self, translatedType, data, timestamp):
        return {
            'timestamp': timestamp,
            'type': translatedType,
            'data': data,
        }
