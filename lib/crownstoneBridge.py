import io
import json
import threading

import serial

from lib.eventBus import eventBus, Topics


class CrownstoneBridge (threading.Thread):
    baudrate = 38400
    port = 'COM1'
    serialController = None
    running = True
    enabled = True

    def __init__(self):
        threading.Thread.__init__(self)
        self.readConfig()

        if self.enabled:
            self.startSerial()

        eventBus.on(Topics.uartWriteCommand, self.writeToUart)

    def run(self):
        print("RUNNING CrownstoneBridge THREAD", self.enabled)
        if self.enabled:
            self.startReading()

    def stop(self):
        print("Killing uart listener")
        self.running = False

    def readConfig(self):
        with open('config.json', 'r') as f:
            config = json.load(f)

        self.baudrate = config['serial']['baudrate']
        self.port = config['serial']['port']
        self.enabled = config['serial']['enabled']


    def startSerial(self):
        print("initializing serial with ", self.port, ' and ', self.baudrate)
        self.serialController = serial.Serial()
        self.serialController.port = self.port
        self.serialController.baudrate = int(self.baudrate)
        self.serialController.timeout = 1
        self.serialController.open()


    def startReading(self):
        print("Starting reading the uart")
        sio = io.TextIOWrapper(io.BufferedRWPair(self.serialController, self.serialController))
        while self.running:
            line = sio.readline()
            if line:
                eventBus.emit(Topics.uartReadLine, line)

        print("Cleaning up")
        self.serialController.close()

    def writeToUart(self, data):
        if self.enabled:
            print("SENDING TO UART")
            self.serialController.write(data)




if __name__ == '__main__':
    b = CrownstoneBridge()
    b.start()
