"""
Utilties for collecting system data.

Author: Jeff Kinnison (jkinniso@nd.edu)
"""

import threading

from . import datacollector


class DataReporter(object):
    """Manages data collection at a specified interval"""

    def __init__(self, interval=1000, **kwargs):
        self.interval = interval
        self.collectors = {}
        for key, value in kwargs:
            self.collectors[key] = datacollector.DataCollector(
                key,
                value.callback,
                value.postprocessor,
                value.args
            )

    def run(self):
        self._collection_event = threading.Event()
        while not self._collection_event.wait(timeout=self.interval):
            self._record_resources()



    def stop(self):
        self._collection_event.set()

    def __getitem__(self, name):
        """Return the data from the collector specified by name"""
        return self.resources[name].data

    def _record_resources(self):
        """Run all collectors"""
        for key, value in self.resources:
            value()
