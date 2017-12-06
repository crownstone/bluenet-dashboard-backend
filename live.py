import signal
import time

from lib.logger import Logger
from lib.uartParser import UartParser
from lib.webSocketServer import WebSocketServer
from lib.crownstoneBridge import CrownstoneBridge

# lets start all modules one by one.

logger = Logger()
parser = UartParser()
uart = CrownstoneBridge()
server = WebSocketServer()

# make sure everything is killed and cleaned up on abort.
def stopAll(signal, frame):
    uart.stop()
    server.stop()
    logger.stop()

# start listener for SIGINT kill command
signal.signal(signal.SIGINT, stopAll)

# start processes
logger.enable()
uart.start()


#time.sleep(1)
#print("SENDING")
#from lib.eventBus import eventBus, Topics
#eventBus.emit(Topics.uartWriteCommand, b"a")

server.start() # <---- this is blocking
