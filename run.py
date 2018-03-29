import signal

from BluenetLib import Bluenet, BluenetEventBus, Topics
from BluenetLib.lib.topics.DevTopics import DevTopics

from BluenetWebSocket import WebSocketServer
from BluenetWebSocket.lib.connector.BluenetConnector import BluenetConnector

from parser.WSParser import WSParser

# Create new bluenet instance
bluenet = Bluenet(catchSIGINT=False)

# Start up the USB bridge
bluenet.initializeUSB("/dev/tty.usbmodemFA1331", baudrate=230400)

# start the websocket server
server = WebSocketServer(9000)

# connect the websocket server to bluenet
server.connectToBluenet(bluenet, BluenetEventBus, Topics)

connector = BluenetConnector()
connector.connect(BluenetEventBus, DevTopics)

# add our custom parser
customParser = WSParser()
customParser.connectToBluenet(bluenet)
server.loadCustomParser(customParser.receiveWebSocketCommand)

# make sure everything is killed and cleaned up on abort.
def stopAll(signal, frame):
    server.stop()
    bluenet.stop()

# start listener for SIGINT kill command
signal.signal(signal.SIGINT, stopAll)

# start processes
print("Starting server...")
server.start() # <---- this is blocking
