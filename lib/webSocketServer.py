import sys

from autobahn.twisted.websocket import WebSocketServerFactory
from twisted.internet import reactor
from twisted.python import log

from lib.webSocketProtocol import BluenetDashboardProtocol

log.startLogging(sys.stdout)

class WebSocketServer ():

    def __init__(self):
        pass

    def start(self):
        factory = WebSocketServerFactory()
        factory.protocol = BluenetDashboardProtocol

        reactor.listenTCP(9000, factory)
        reactor.run()

    def stop(self):
        reactor.stop()
