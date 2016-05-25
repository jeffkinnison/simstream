import pika

from .pikaasyncconsumer import PikaAsyncConsumer
from .datacollector import DataCollector
from .datareporter import DataReporter
from .eventhandler import EventHandler
from .eventmonitor import EventMonitor


class ReporterExistsException(Exception):
    """Thrown when attempting to add a DataReporter with a conflicting name"""
    pass


class SimStream(object):
    """
    Manager for routing messages to their correct reporter.
    """

    DEFAULT_CONFIG_PATH="simstream.cnf"

    def __init__(self, reporters={}, config={}):
        self.reporters = reporters
        self.consumer = None
        self.config = config

    def add_data_reporter(self, reporter):
        """
        Add a new DataReporter object.

        Arguments:
        reporter -- the DataReporter to add
        """
        if reporter.name in self.reporters:
            throw ReporterExistsException
        self.reporters[reporter.name] = reporter

    def parse_config(self):
        """
        Read the config file and set up the specified, data collection and
        event handling resources.
        """
        # TODO: Read in config
        # TODO: Set up configuration dict
        pass

    def route_message(self, message):
        """
        Send a message to the correct reporter.
        """
        # TODO: Create new MessageParser
        # TODO: Run message through MessageParser
        # TODO: Route message to the correct DataReporter/EventMonitor
        parser = MessageParser()
        parser(message)
        if parser.reporter_name in self.reporters:
            self.reporters[parser.reporter_name].start_streaming(
                    parser.collector_name,
                    parser.exchange,
                    parser.queue,
                    parser.routing_key
                )

    def start_collecting(self):
        """
        Begin collecting data and monitoring for events.
        """
        for reporter in self.reporters:
            reporter.start_collecting()

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

    def setup_consumer(self, config):
        """
        Set up and configure the consumer.
        """
        # TODO: Create and configure the PikaAsyncConsumer for this run
        if len(self.config) > 0:
            self.consumer = PikaAsyncConsumer(self.config.rabbitmq_url,
                                              self.config.exchange_name,
                                              self.config.queue_name,
                                              self.route_message
                                             )

    def start(self):
        """
        Configure and start SimStream.
        """
        # TODO: Perform setup operations
        # TODO: Start collecting data
        # TODO: Start monitoring for events
        # TODO: Start listening for messages
        self.consumer.start()

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
