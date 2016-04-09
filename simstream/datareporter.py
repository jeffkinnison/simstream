"""
Utilties for collecting system data.

Author: Jeff Kinnison (jkinniso@nd.edu)
"""

import threading
from exception import Exception

from .datacollector import DataCollector


class CollectorExistsException(Exception):
    pass


class CollectorDoesNotExistException(Exception):
    pass


class DataReporter(object):
    """Manages data collection at a specified interval"""

    def __init__(self, interval=1000, collectors={}):
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

    def add_collector(self, name, limit, callback, postprocessor=None,
                      callback_args=[], postprocessor_args=[]):
        """Add a new collector, raise an exception if a name conflict occurs."""
        if name in self.collectors:
            raise CollectorExistsException

        self.collectors[name] = datacollector.DataCollector(
            name,
            limit,
            callback,
            postprocessor,
            callback_args,
            postprocessor_args
        )

    def stop_collector(self, name):
        """Deactivate the specified collector."""
        if name not in self.collectors:
            raise CollectorDoesNotExistException

        self.collectors[name].deactivate()

    def run(self):
        """Collect data asynchronously at the specified interval."""
        self._collection_event = threading.Event()
        while not self._collection_event.wait(timeout=self.interval):
            self._record_resources()

    def stop(self):
        """Stop the data collection process"""
        self._collection_event.set()

    def __getitem__(self, name):
        """Return the data from the collector specified by name"""
        return self.resources[name].data

    def _record_resources(self):
        """Run all collectors"""
        for key, value in self.resources:
            value()
