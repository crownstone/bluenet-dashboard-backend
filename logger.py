from eventBus import eventBus

class Logger:
    subscriptionId = None
    fileHandle = None

    def __init__(self):
        pass

    def enable(self):
        # disable just in case we have an active subscription
        self.disable()
        self.fileHandle = open("dataLog.log", "a")
        self.subscriptionId = eventBus.on("uartReadLine", self.toFile)

    def disable(self):
        if self.subscriptionId:
            eventBus.off(self.subscriptionId)
            self.subscriptionId = None

        self.close()
        self.fileHandle = None

    def stop(self):
        if self.fileHandle:
            self.fileHandle.close()

    def toFile(self, line):
        self.fileHandle.write(line)
