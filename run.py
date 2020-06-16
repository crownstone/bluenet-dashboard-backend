#!/usr/bin/env python3

import signal

from crownstone_uart import CrownstoneUart, UartEventBus, UartTopics
from crownstone_uart.topics.DevTopics import DevTopics

from BluenetWebSocket import WebSocketServer
from BluenetWebSocket.lib.connector.BluenetConnector import BluenetConnector

from parser.WSParser import WSParser

# Create new bluenet instance
bluenet = CrownstoneUart()

# Start up the USB bridge
bluenet.initialize_usb_sync("/dev/ttyACM0")

# start the websocket server
server = WebSocketServer(9000)

# connect the websocket server to bluenet lib
server.connectToBluenet(bluenet, UartEventBus, UartTopics)

connector = BluenetConnector()
connector.connect(UartEventBus, DevTopics)

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
