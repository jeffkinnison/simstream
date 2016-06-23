"""
Utilties for collecting system data.

Author: Jeff Kinnison (jkinniso@nd.edu)
"""

from .pikaproducer import PikaProducer

from threading import Thread, Lock, Event

import copy

class DataCollector(Thread):
    """Collects data by running user-specified routines.

    Inherits from: threading.Thread

    Instance variables:
    name -- the name of the collector
    limit -- the maximum number of maintained data points
    interval -- the interval (in seconds) at which data collection is performed

    Public methods:
    activate -- start collecting data
    add_routing_key -- add a new streaming endpoint
    deactivate -- stop further data collection
    remove_routing_key -- remove a streaming endpoint
    run -- collect data if active
    """
    def __init__(self, name, callback, rabbitmq_url, exchange, exchange_type="direct", limit=250, interval=10,
                 postprocessor=None, callback_args=[], postprocessor_args=[]):
        """
        Arguments:
        name -- the name of the collector
        callback -- the data collection function to run

        Keyword arguments:
        limit -- the maximum number of maintained data points (default 250)
        interval -- the time interval in seconds at which to collect data
                    (default: 10)
        postprocessor -- a function to run on the return value of callback
                         (default None)
        callback_args -- the list of arguments to pass to the callback
                         (default [])
        postprocessor_args -- the list of arguments to pass to the
                              postprocessor (default [])
        """
        super(DataCollector, self).__init__()
        self.name = name if name else "Unknown Resource"
        self.limit = limit
        self.interval = interval
        self._callback = callback
        self._callback_args = callback_args
        self._postprocessor = postprocessor
        self._postprocessor_args = postprocessor_args
        self._data = []
        self._active = False

    def activate(self):
        """
        Start collecting data.
        """
        self._active = True

    def deactivate(self):
        """
        Stop collecting data.
        """
        self._active = False

    def run(self):
        """
        Run the callback and postprocessing subroutines and record result.

        Catches generic exceptions because the function being run is not
        known beforehand.
        """
        self._collection_event = Event()
        while self._active and not self._collection_event.wait(timeout=self.interval):
            try:
                result = self._callback(*self._callback_args)
                result = self._postprocessor(result, *self._postprocessor_args) if self._postprocessor else result
                #print("Found the value ", result, " in ", self.name)
                self._data.append(result)
                if len(self._data) > self.limit:
                    self._data.pop(0)

            except Exception as e:
                print("[ERROR] %s" % (e))

    def stop(self):
        self.deactivate()
