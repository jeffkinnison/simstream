"""
Utilties for collecting system data.

Author: Jeff Kinnison (jkinniso@nd.edu)
"""

# TODO: Refactor to iterate over producers, not collectors. Collectors should
#       execute concurrently.
# TODO: Add method to deactivate reporter

from threading import Thread, Event

from .datacollector import DataCollector


class CollectorExistsException(Exception):
    """Thrown when attempting to add a collector with a conflicting name."""
    pass


class CollectorDoesNotExistException(Exception):
    """Thrown when attempting to access a collector that does not exist."""
    pass


class ProducerExistsException(Exception):
    """Thrown when attempting to add a producer with a conflicting name."""
    pass


class ProducerDoesNotExistException(Exception):
    """Thrown when attempting to work with a producer that does not exist."""
    pass


class DataReporter(Thread):
    """Manages collecting specified data.

    Subclass of threading.Thread that modifies Thread.join() and Thread.run()

    Instance variables:
    interval -- the time interval in seconds between data collection
    collectors -- a dict of DataCollectors that are run at interval
    producers -- a dict of active PikaProducers corresponding to user requests
                for streaming collector data

    Public methods:
    add_collector -- add a new DataCollector to the list
    run -- start the data collection loop
    join -- end data collection and return control to main thread
    stop_collector -- stop a running DataCollector
    """

    def __init__(self, interval=10, collectors={}):
        super(DataReporter, self).__init__()
        self.interval = interval
        self.collectors = {}
        self.producers = {}
        for key, value in collectors:
            self.add_collector(
                key,
                value.limit,
                value.callback,
                value.postprocessor,
                value.callback_args,
                value.postprocessor_args
            )

    def add_collector(self, name, callback, limit=250, postprocessor=None,
                      callback_args=[], postprocessor_args=[]):
        """Add a new collector.

        Arguments:
        name -- name of the new DataCollector
        callback -- the data collection callback to run

        Keyword arguments:
        limit -- the number of data points to store (default 100)
        postprocessor -- a postprocessing function to run on each data point
                         (default None)
        callback_args -- a list of arguments to pass to the callback
                         (default [])
        postprocessor_args -- a list of arguments to pass to the postprocessor
                              (default [])

        Raises:
        CollectorExistsException if a collector named name already exists
        """
        if name in self.collectors:
            raise CollectorExistsException

        self.collectors[name] = DataCollector(
            name,
            callback,
            limit,
            postprocessor,
            callback_args,
            postprocessor_args
        )

    def start_collecting(self):
        """
        Start data collection for all associated collectors.
        """
        for collector in self.collectors:
            if not self.collectors[collector].active:
                self.start_collector(collector)

    def start_collector(self, name):
        """
        Activate the specified collector.

        Arguments:
        name -- the name of the collector to start

        Raises:
        RuntimeError if the collector has already been started.
        """
        try:
            self.collectors[name].activate()
            self.collectors[name].start()
        except RuntimeError as e:
            print("Error starting collector ", name)
            print(e)

    def stop_collecting(self):
        """
        Stop all collectors.
        """
        for collector in self.collectors:
            try:
                self.collectors[collector].join()
            except RuntimeError as e: # Catch unintentional dealock
                print("Despite all odds, this seems to be causing deadlock. Crazy!")

    def stop_collector(self, name):
        """Deactivate the specified collector.

        Arguments:
        name -- the name of the collector to stop

        Raises:
        CollectorDoesNotExistException if no collector named name exists
        """
        if name not in self.collectors:
            raise CollectorDoesNotExistException

        self.collectors[name].deactivate()

    def start_streaming(self, collector_name, routing_key):
        """
        Begin streaming data from a collector to a particular recipient.

        Arguments:
        routing_key -- the routing key to reach the intended recipient
        """
        if collector_name not in self.collectors: # Make sure collector exists
            raise CollectorDoesNotExistException
        self.collectors[collector_name].add_routing_key(routing_key)

    def stop_streaming(self, collector_name, routing_key):
        """
        Stop a particular stream.

        Arguments:
        collector_name -- the collector associated with the producer to stop
        routing_key -- the routing key to reach the intended recipient

        Raises:
        ProducerDoesNotExistException if no producer named name exists
        ValueError if the producer is removed by another call to this method
                   after the for loop begins
        """
