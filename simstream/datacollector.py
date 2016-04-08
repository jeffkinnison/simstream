"""
Utilties for collecting system data.

Author: Jeff Kinnison (jkinniso@nd.edu)
"""


class DataCollector(object):
    """Collects data by running user-specified routines"""
    def __init__(self, name, limit=250, callback, postprocessor=None,
                 callback_args=[], postprocessor_args=[]):
        self.name = name if name else "Unknown Resource"
        self.limit = limit
        self._callback = callback
        self._callback_args = args
        self._postprocessor = postprocessor
        self._data = []

    def __call__(self):
        """Run the callback and postprocessing subroutines and recod result"""
        try:
            result = _callback(*self._callback_args)
            self.data.append(
                self._postprocessor(result) if self._postprocessor else result
            )

            if len(data) > self.limit:
                data.pop(0)

        except Exception as e:
            print("Error: ", e)

    @property
    def data(self, start=0, end=-1):
        return self._data[start:end]
