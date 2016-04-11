"""
Utilties for collecting system data.

Author: Jeff Kinnison (jkinniso@nd.edu)
"""

from threading import Thread, Lock


class DataCollector(object):
    """Collects data by running user-specified routines"""
    def __init__(self, name, callback, limit=250, postprocessor=None,
                 callback_args=[], postprocessor_args=[]):
        super(DataCollector, self).__init__()
        self.name = name if name else "Unknown Resource"
        self.limit = limit
        self._callback = callback
        self._callback_args = callback_args
        self._postprocessor = postprocessor
        self._postprocessor_args = postprocessor_args
        self._data = []
        self.data_lock = Lock()
        self._active = True

    def run(self):
        """Run the callback and postprocessing subroutines and record result."""
        try:
            result = self._callback(*self._callback_args) if len(self._callback_args) > 0 else self._callback()
            #result = self._postprocessor(result) if self._postprocessor else result
            print("Found the value ", result, " in ", self.name)
            self.data_lock.acquire()
            self._data.append(result)
            if len(self._data) > self.limit:
                self._data.pop(0)
            self.data_lock.release()

        except Exception as e:
            print("Error: ", e)

    def deactivate(self):
        self._active = False

    def __call__(self):
        """Run the data collection in parallel."""
        if self._active:
            self.run()

    @property
    def data(self, start=None, end=None):
        data = []
        if start is None and end is None:
            self.data_lock.acquire()
            data = self._data
            self.data_lock.release()
        else:
            self.data_lock.acquire()
            data = self._data[start:end]
            self.data_lock.release()
        return data

    @property
    def active(self):
        return self._active
