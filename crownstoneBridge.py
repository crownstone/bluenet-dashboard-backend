import threading

import serial
import json
import io
from eventBus import eventBus


class CrownstoneBridge (threading.Thread):
    baudrate = 38400
    port = 'COM1'
    serialController = None
    running = True

    def __init__(self):
        threading.Thread.__init__(self)
        self.readConfig()
        self.startSerial()

        eventBus.on("uartWriteCommand", self.writeToUart)

    def run(self):
        print("RUNNING CrownstoneBridge THREAD")
        self.startReading()

    def stop(self):
        print("Killing uart listener")
        self.running = False

    def readConfig(self):
        with open('config.json', 'r') as f:
            config = json.load(f)

        self.baudrate = config['serial']['baudrate']
        self.port = config['serial']['port']


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
                eventBus.emit('uartReadLine', line)

        print("Cleaning up")
        self.serialController.close()

    def writeToUart(self, data):
        pass




if __name__ == '__main__':
    b = CrownstoneBridge()
    b.start()
    b.startReading()
