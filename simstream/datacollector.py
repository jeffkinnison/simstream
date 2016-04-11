"""
Utilties for collecting system data.

Author: Jeff Kinnison (jkinniso@nd.edu)
"""

from threading import Thread, Lock


class DataCollector(object):
    """Collects data by running user-specified routines.

    Instance variables:
    name -- the name of the collector
    limit -- the maximum number of maintained data points

    Public methods:
    run -- collect data if active
    deactivate -- stop further data collection
    """
    def __init__(self, name, callback, limit=250, postprocessor=None,
                 callback_args=[], postprocessor_args=[]):
        """
        Arguments:
        name -- the name of the collector
        callback -- the data collection function to run

        Keyword arguments:
        limit -- the maximum number of maintained data points (default 250)
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
        self._callback = callback
        self._callback_args = callback_args
        self._postprocessor = postprocessor
        self._postprocessor_args = postprocessor_args
        self._data = []
        self._data_lock = Lock()
        self._active = True

    def run(self):
        """Run the callback and postprocessing subroutines and record result.

           Catches generic exceptions because the function being run is not
           known.
        """
        try:
            result = self._callback(*self._callback_args)# if len(self._callback_args) > 0 else self._callback()
            result = self._postprocessor(result) if self._postprocessor else result
            print("Found the value ", result, " in ", self.name)
            self._data_lock.acquire()
            self._data.append(result)
            if len(self._data) > self.limit:
                self._data.pop(0)
            self._data_lock.release()

        except Exception as e:
            print("Error: ", e)

    def deactivate(self):
        """Stop collecting data when run."""
        self._active = False

    def __call__(self):
        """Collect data."""
        if self._active:
            self.run()

    @property
    def data(self, start=None, end=None):
        """Retrieve a slice of the collected data."""
        data = []
        if start is None and end is None:
            self._data_lock.acquire()
            data = self._data
            self._data_lock.release()
        else:
            self._data_lock.acquire()
            data = self._data[start:end]
            self._data_lock.release()
        return data

    @property
    def active(self):
        """Return the active status of the collector."""
        return self._active
