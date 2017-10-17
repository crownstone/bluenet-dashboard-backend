import uuid

###############
#
#   Used Topics
#
#
#   uartReadLine        data: string line of data
#   uartWriteCommand    data: string to write to uart
#
#
#
#
#
#
###############


class EventBus:
    topics = {}
    subscriberIds = {}

    def __init__(self):
        pass

    def on(self, topic, callback):
        print("subscribing", topic)
        if topic not in self.topics:
            self.topics[topic] = {}

        subscriptionId = str(uuid.uuid4())
        print("got uuid", subscriptionId)
        self.subscriberIds[subscriptionId] = topic
        self.topics[topic][subscriptionId] = callback

        return subscriptionId

    def emit(self, topic, data):
        if topic in self.topics:
            for subscriptionId in self.topics[topic]:
                self.topics[topic][subscriptionId](data)


    def off(self, subscriptionId):
        if subscriptionId in self.subscriberIds:
            topic = self.subscriberIds[subscriptionId]
            if topic in self.topics:
                self.topics[topic].pop(subscriptionId)

            self.subscriberIds.pop(subscriptionId)
        else:
            print("Subscription ID cannot be found.")


eventBus = EventBus()
