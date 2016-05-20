import pika

from .pikaasynccon
from .datacollector import DataCollector
from .datareporter import DataReporter
from .eventhandler import EventHandler
from .eventmonitor import EventMonitor


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
        # TODO: Read in config
        # TODO: Set up temporary configuration dict
        # TODO: Return config dict
        pass

    def route_message(self, message):
        """
        Send a message to the correct reporter.
        """
        # TODO: Create new MessageParser
        # TODO: Run message through MessageParser
        # TODO: Route message to the correct DataReporter/EventMonitor
        pass

    def start_collecting(self):
        """
        Begin collecting data and monitoring for events.
        """
        pass

    def setup(self):
        """
        Set up the SimStream instance: create DataCollectors, create
        EventMonitors, configure AMQP consumer.
        """
        # TODO: Get config information
        # TODO: Create DataReporter and DataCollector instances
        # TODO: Create EventMonitor and EventHandler instances
        # TODO: Configure consumer
        pass

    def setup_data_collection(self, config):
        """
        Set up all DataReporters and DataCollectors.
        """
        # TODO: Create and configure all DataReporters
        # TODO: Create and configure all DataCollectors
        # TODO: Assign each DataCollector to the correct DataReporter
        pass

    def setup_event_monitoring(self, config):
        """
        Set up all EventMonitors and EventHandlers.
        """
        # TODO: Create and configure all EventMonitors
        # TODO: Create and configure all EventHandlers
        # TODO: Assign each EventMonitor to the correct EventHandler
        pass

    def setup_consumer(self, config):
        """
        Set up and configure the consumer.
        """
        # TODO: Create and configure the PikaAsyncConsumer for this run
        pass

    def start(self):
        """
        Configure and start SimStream.
        """
        # TODO: Perform setup operations
        # TODO: Start collecting data
        # TODO: Start monitoring for events
        # TODO: Start listening for messages
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
