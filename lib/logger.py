import time

from lib.eventBus import eventBus, Topics


class Logger:
    subscriptionId = None
    fileHandle = None

    def __init__(self):
        pass

    def enable(self):
        # disable just in case we have an active subscription
        self.disable()
        self.fileHandle = open("dataLog.log", "a")
        self.subscriptionId = eventBus.on(Topics.uartReadLine, self.toFile)

    def disable(self):
        if self.subscriptionId:
            eventBus.off(self.subscriptionId)
            self.subscriptionId = None

        self.stop()
        self.fileHandle = None

    def stop(self):
        if self.fileHandle:
            self.fileHandle.close()

    def toFile(self, line):
        timestampStr = str(round(time.time() * 1000))

        lineStr = None
        if type(line) is bytes:
            lineStr = str(line,'ascii')
        elif type(line) is str:
            lineStr = line
        else:
            lineStr = str(line)

        self.fileHandle.write(timestampStr + lineStr)
