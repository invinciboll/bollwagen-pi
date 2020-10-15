# Import all the libraries

from pubnub import Pubnub

import time


# Initialize the Pubnub Keys
# Replace them with your keysets
pub_key = "pub-c-aa6dbb2f-dac1-4ca3-8246-4280f1f577ba"
sub_key = "sub-c-1bdc21b0-07fb-11eb-ac24-4e38869d876d"


def init():  # initalize the pubnub keys and start subscribing

    global pubnub  # Pubnub Initialization

    pubnub = Pubnub(publish_key=pub_key, subscribe_key=sub_key)
    pubnub.subscribe(channels='paymentTrigger', callback=callback, error=callback, reconnect=reconnect,
                     disconnect=disconnect)


def get_message(controlCommand):
    if (controlCommand.has_key("trigger")):
        if (controlCommand["trigger"] == "anything" and controlCommand["status"] == 1):

            print("payment recieved")

        else:

            pass

    else:
        pass


def callback(message, channel):  # this function waits for the message from the aleatrigger channel
    print(message)
    if (message.has_key("requester")):
        get_message(message)
    else:
        pass


def error(message):  # if there is error in the channel,print the  error
    print("ERROR : " + str(message))


def reconnect(message):  # responds if server connects with pubnub
    print("RECONNECTED")


def disconnect(message):  # responds if server disconnects with pubnub
    print("DISCONNECTED")


if __name__ == '__main__':
    init()  # Initialize the Script
