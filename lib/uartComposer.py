import time

from lib.eventBus import Topics
from lib.eventBus import eventBus
import json






class UartComposer:

    def __init__(self):
        eventBus.on(Topics.wsReceivedMessage, self.parseDashboardMessage)


    def parseDashboardMessage(self, stringifiedJson):
        """ this is invoked for every line received over the uart """
        dict = json.loads(stringifiedJson)

        if dict["type"] == "setRelay":
            pass # not implemented yet, eventBus.emit(Topics.uartWriteCommand, b"x" if dict["data"]["value"] else b"y")
        elif dict["type"] == "setAdvertisements":
            eventBus.emit(Topics.uartWriteCommand, b"a")
        elif dict["type"] == "setMesh":
            eventBus.emit(Topics.uartWriteCommand, b"m")
        elif dict["type"] == "setIGBT":
            pass
        elif dict["type"] == "setVoltageRange":
            pass
        elif dict["type"] == "setCurrentRange":
            pass
        elif dict["type"] == "setVoltageDifferential":
            pass
        elif dict["type"] == "setCurrentDifferential":
            pass
        elif dict["type"] == "toggleMeasurementChannel":
            pass
        elif dict["type"] == "reset":
            eventBus.emit(Topics.uartWriteCommand, b"r")




