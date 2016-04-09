"""
Utilties for collecting system data.

Author: Jeff Kinnison (jkinniso@nd.edu)
"""

from threading import Thread, Lock


class DataCollector(Thread):
    """Collects data by running user-specified routines"""
    def __init__(self, name, limit=250, callback, postprocessor=None,
                 callback_args=[], postprocessor_args=[]):
        super(DataCollector, self).__init__()
        self.name = name if name else "Unknown Resource"
        self.limit = limit
        self._callback = callback
        self._callback_args = args
        self._postprocessor = postprocessor
        self._data = []
        self.data_lock = Lock()

    def run(self):
        """Run the callback and postprocessing subroutines and record result."""
        try:
            result = _callback(*self._callback_args)
            result = self._postprocessor(result) if self._postprocessor else result

            self.data_lock.acquire()
            self.data.append(result)
            self.data_lock.release()

            if len(data) > self.limit:
                data.pop(0)

        except Exception as e:
            print("Error: ", e)

    def __call__(self):
        """Run the data collection in parallel."""
        self.start()

    @property
    def data(self, start=0, end=-1):
        Lock.acquire()
        data = self._data[start:end]
        Lock.release()
        return data
