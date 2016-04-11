"""
Utilties for collecting system data.

Author: Jeff Kinnison (jkinniso@nd.edu)
"""

from threading import Thread, Event

from .datacollector import DataCollector


class CollectorExistsException(Exception):
    """Thrown when attempting to add a collector with a conflicting name."""
    pass


class CollectorDoesNotExistException(Exception):
    """Thrown when attempting to access a collector that does not exist."""
    pass


class DataReporter(Thread):
    """Manages collecting specified data.

    Subclass of threading.Thread that modifies Thread.join() and Thread.run()

    Instance variables:
    interval -- the time interval in seconds between data collection
    collectors -- a dict of DataCollectors that are run at interval

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

    def run(self):
        """Collect data in parallel at the specified interval.

        Call self.join() to stop collecting.
        """
        print("Running the collectors")
        self._collection_event = Event()
        while not self._collection_event.wait(timeout=self.interval):
            print("Collecting")
            self._record_resources()

    def join(self):
        """Stop the data collection process."""
        try:
            self._collection_event.set()
            self._collection_event = 0
        except AttributeError:
            print("No collection event in ", self.name)

    def __getitem__(self, name):
        """Return the data from the collector specified by name.

        Arguments:
        name -- the name of the collector from which to pull data

        Raises:
        CollectorDoesNotExistException if no collector named name exists
        """
        if name not in self.collectors:
            raise CollectorDoesNotExistException
        return self.collectors[name].data

    def _record_resources(self):
        """Run all collectors."""
        for key in self.collectors:
            if callable(self.collectors[key]):
                print("Running collector %s" % key)
                self.collectors[key]()
