import pika

from . import EventReporter

class SimStream(object):
    """
    Manager for routing messages to their correct reporter.
    """

    DEFAULT_CONFIG_PATH="simstream.cnf"

    def __init__(self):
        pass

    def parse_config(self):
        """
        Read the config file and set up the specified, data collection and
        event handling resources.
        """
        pass

    def route_message(self, message):
        """
        Send a message to the correct reporter.
        """
        pass

    def start_collecting(self):
        """
        Begin collecting data and monitoring for events.
        """
        pass

    class MessageParser(object):
        """
        Internal message parsing facilities.
        """

        def __init__(self):
            pass

        def __call__(self, message):
            pass

if __name__ == "__main__":
    print(SimStream.DEFAULT_CONFIG_PATH)
