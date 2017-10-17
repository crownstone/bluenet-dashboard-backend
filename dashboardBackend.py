import signal

from webSocketServer import WebSocketServer
from crownstoneBridge import CrownstoneBridge
from logger import Logger



# lets start all modules one by one.
logger = Logger()
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
server.start()
