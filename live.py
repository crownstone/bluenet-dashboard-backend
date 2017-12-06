import signal
import time

from lib.logger import Logger
from lib.uartComposer import UartComposer
from lib.uartParser import UartParser
from lib.webSocketServer import WebSocketServer
from lib.crownstoneBridge import CrownstoneBridge

# lets start all modules one by one.

logger = Logger()
uartParser = UartParser()
uartListener = CrownstoneBridge()
uartComposer = UartComposer()
server = WebSocketServer()

# make sure everything is killed and cleaned up on abort.
def stopAll(signal, frame):
    uartListener.stop()
    server.stop()
    logger.stop()

# start listener for SIGINT kill command
signal.signal(signal.SIGINT, stopAll)

# start processes
logger.enable()
uartListener.start()
server.start() # <---- this is blocking
