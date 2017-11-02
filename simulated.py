import signal


from lib.logger import Logger
from lib.simulator import Simulator
from lib.uartParser import UartParser
from lib.webSocketServer import WebSocketServer

# lets start all modules one by one.

logger = Logger()
parser = UartParser()
server = WebSocketServer()
simulator = Simulator()

# make sure everything is killed and cleaned up on abort.
def stopAll(signal, frame):
    server.stop()
    logger.stop()

# start listener for SIGINT kill command
signal.signal(signal.SIGINT, stopAll)


# start processes
logger.enable()
simulator.start()
server.start()
