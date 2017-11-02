from lib.eventBus import eventBus, Topics
import threading

class Simulator(threading.Thread):
    filename = 'dashboard.log'
    content = None

    def __init__(self):
        threading.Thread.__init__(self)
        eventBus.on(Topics.websocketConnectionInitialized, self.start)

    def run(self):
        self.startRunningLog()


    def readLog(self):
        with open(self.filename) as f:
            self.content = f.readlines()


    def startRunningLog(self):
        self.readLog()
        for line in self.content:
            eventBus.emit(Topics.simulatedUartReadLine, line)

